"""Fail-closed static validation and isolated localhost Playwright QA."""
from __future__ import annotations

import functools
import http.server
import re
import threading
from contextlib import contextmanager
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

from .contracts import WorkflowError
from .storage import digest, write_json

ALLOWED_SUFFIXES = {".html", ".css", ".js", ".svg", ".txt"}


def safe_relative(name):
    if not isinstance(name, str) or not name or any(ord(c) < 32 or c in '\\:*?"<>|' for c in name):
        raise WorkflowError(f"Unsafe site path: {name!r}")
    path = PurePosixPath(name)
    if path.is_absolute() or any(p in (".", "..") or p.startswith(".") for p in path.parts) or str(path) != name:
        raise WorkflowError(f"Unsafe site path: {name!r}")
    if any(part.endswith((".", " ")) or re.match(r"^(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", part, re.I) for part in path.parts):
        raise WorkflowError(f"Non-portable Windows/SiteGround path: {name!r}")
    if path.suffix not in ALLOWED_SUFFIXES:
        raise WorkflowError(f"Unsupported static file extension (use lowercase): {name}")
    return path


def validate_build(result):
    names, total = set(), 0
    for item in result["files"]:
        path = safe_relative(item["path"])
        canonical = str(path).casefold()
        if canonical in names:
            raise WorkflowError("Duplicate/case-colliding site path")
        names.add(canonical)
        total += len(item["content"].encode("utf-8"))
        if path.suffix == ".svg" and re.search(r"<\s*(script|foreignObject)|\bon\w+\s*=|(?:href\s*=\s*['\"])(?!#)", item["content"], re.I):
            raise WorkflowError("SVG contains active or external content")
    if not any(item["path"] == "index.html" for item in result["files"]):
        raise WorkflowError("Build must contain the exact SiteGround entry filename index.html")
    if total > 1500000:
        raise WorkflowError("Site exceeds the 1.5 MB source/asset budget")
    file_names = {item["path"] for item in result["files"]}
    provenance = {item["path"] for item in result["asset_provenance"]}
    assets = {name for name in file_names if Path(name).suffix == ".svg"}
    if assets - provenance or provenance - file_names:
        raise WorkflowError("Asset provenance is missing or refers to nonexistent files")
    return result


def site_manifest(site):
    site = Path(site)
    result = {}
    if site.is_symlink():
        raise WorkflowError("Site directory must not be a symlink")
    for path in sorted(site.rglob("*")):
        if path.is_symlink():
            raise WorkflowError("Symlinks are not allowed in generated sites")
        if path.is_file():
            name = path.relative_to(site).as_posix()
            safe_relative(name)
            result[name] = digest(path.read_bytes())
    return result


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags, self.ids, self.links, self.resources, self.errors = [], [], [], [], []
        self.text = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        self.tags.append((tag, attrs))
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if any(key.lower().startswith("on") for key in attrs):
            self.errors.append("Inline event handler is not allowed")
        if tag in ("iframe", "form", "object", "embed", "base"):
            self.errors.append(f"Unsupported active/server-dependent element: {tag}")
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag in ("script", "img", "source", "video", "audio") and attrs.get("src"):
            self.resources.append(attrs["src"])
        if tag == "link" and attrs.get("rel", "").lower() == "stylesheet":
            self.resources.append(attrs.get("href", ""))
        if tag == "img" and "alt" not in attrs:
            self.errors.append("Image missing alt attribute")
        if attrs.get("srcset"):
            self.errors.append("Use simple local src assets, not srcset, in v1")
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.errors.append("Meta refresh is not allowed")

    handle_startendtag = handle_starttag

    def handle_data(self, text):
        self.text.append(text)


def review_content(site, max_chars=30000):
    """Provide complete readable copy, not CSS/JS bundles, to the vision reviewer."""
    class CopyParser(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.ignored = 0
            self.parts = []
        def handle_starttag(self, tag, attrs):
            if tag in ("script", "style"):
                self.ignored += 1
            if not self.ignored:
                for key, value in attrs:
                    if key in ("alt", "aria-label") and value:
                        self.parts.append(value)
        def handle_endtag(self, tag):
            if tag in ("script", "style"):
                self.ignored = max(0, self.ignored - 1)
        def handle_data(self, data):
            if not self.ignored and data.strip():
                self.parts.append(data.strip())
    site = Path(site).resolve()
    pages, size = [], 0
    for path in sorted(site.rglob("*.html")):
        parser = CopyParser(); parser.feed(path.read_text(encoding="utf-8"))
        text = " ".join(" ".join(parser.parts).split())
        size += len(text)
        if size > max_chars:
            raise WorkflowError("Readable site copy exceeds visual-review budget; split the review into page tasks")
        pages.append({"page": path.relative_to(site).as_posix(), "copy": text})
    return {"pages": pages, "source_paths": [str((site / name).resolve()) for name in site_manifest(site)]}


def local_target(site, current, href):
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        raise WorkflowError(f"Remote resource not allowed: {href}")
    relative = unquote(parsed.path)
    if "\\" in relative or "\x00" in relative:
        raise WorkflowError("Invalid local URL")
    path = (site / relative.lstrip("/") if relative.startswith("/") else current.parent / relative).resolve()
    if not path.is_relative_to(site.resolve()):
        raise WorkflowError("Local link escapes site directory")
    if path.is_dir():
        path = path / "index.html"
    return path, unquote(parsed.fragment)


def static_audit(site, plan):
    site = Path(site).resolve()
    errors, docs = [], {}
    manifest = site_manifest(site)
    if "index.html" not in manifest:
        errors.append("Missing exact index.html entry file for case-sensitive static hosting")
    if not manifest:
        return {"passed": False, "errors": ["Empty site"], "manifest": {}, "pages": []}
    for name in manifest:
        path = site / name
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".html":
            doc = Document(); doc.feed(text); docs[path] = doc
            errors += [f"{name}: {e}" for e in doc.errors]
            tags = doc.tags
            if sum(tag == "h1" for tag, _ in tags) != 1:
                errors.append(f"{name}: require exactly one H1")
            for required in ("title", "main", "html"):
                if not any(tag == required for tag, _ in tags):
                    errors.append(f"{name}: missing {required}")
            if not any(tag == "html" and attrs.get("lang") for tag, attrs in tags):
                errors.append(f"{name}: HTML language missing")
            for meta in ("viewport", "description"):
                if not any(tag == "meta" and attrs.get("name", "").lower() == meta and attrs.get("content", "").strip() for tag, attrs in tags):
                    errors.append(f"{name}: missing {meta} meta")
            if not any(tag == "meta" and attrs.get("name", "").lower() == "robots" and "noindex" in attrs.get("content", "").lower() for tag, attrs in tags):
                errors.append(f"{name}: draft must have robots noindex")
            if len(set(doc.ids)) != len(doc.ids):
                errors.append(f"{name}: duplicate HTML IDs")
            if re.search(r"lorem ipsum|\bTODO\b|\bTBD\b|your (?:business|company) name|\[APPROVED_PREVIEW_URL\]", " ".join(doc.text), re.I):
                errors.append(f"{name}: placeholder copy detected")
            for resource in doc.resources:
                try:
                    target, _ = local_target(site, path, resource)
                    if not target.is_file():
                        errors.append(f"{name}: missing resource {resource}")
                except WorkflowError as exc:
                    errors.append(f"{name}: {exc}")
        if path.suffix == ".css":
            if re.search(r"@import\b|url\(\s*['\"]?(?:https?:|//|data:)", text, re.I):
                errors.append(f"{name}: remote CSS dependency/import")
            for resource in re.findall(r"url\(\s*['\"]?([^'\")]+)", text):
                try:
                    target, _ = local_target(site, path, resource.strip())
                    if not resource.startswith("#") and not target.is_file():
                        errors.append(f"{name}: missing CSS asset {resource}")
                except WorkflowError as exc:
                    errors.append(f"{name}: {exc}")
    for path, doc in docs.items():
        for href in doc.links:
            if not href or href == "#" or href.lower().startswith(("javascript:", "data:", "file:")):
                errors.append(f"{path.name}: empty or unsafe link {href!r}")
                continue
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                if href != plan["cta_href"]:
                    errors.append(f"{path.name}: outgoing link is not the approved CTA: {href}")
                continue
            try:
                target, fragment = local_target(site, path, href)
                if not target.is_file():
                    errors.append(f"{path.name}: broken link {href}")
                elif fragment and target in docs and fragment not in docs[target].ids:
                    errors.append(f"{path.name}: missing anchor {href}")
            except WorkflowError as exc:
                errors.append(str(exc))
    if not any(plan["cta_href"] in doc.links for doc in docs.values()):
        errors.append("Verified primary CTA not present")
    return {"passed": not errors, "errors": errors, "manifest": manifest,
            "pages": [p.relative_to(site).as_posix() for p in docs],
            "total_bytes": sum((site / name).stat().st_size for name in manifest)}


class LocalHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def list_directory(self, path):
        self.send_error(403, "Directory listing disabled")
        return None

    def translate_path(self, path):
        target = Path(super().translate_path(path))
        root = Path(self.directory).resolve()
        if not target.resolve().is_relative_to(root) or target.is_symlink():
            return str(root / "__blocked__")
        return str(target)


@contextmanager
def serve(site):
    site_manifest(site)  # Reject symlinks before exposing files.
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(LocalHandler, directory=str(Path(site).resolve())))
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=3)


def browser_audit(site, plan, output):
    site = Path(site).resolve()
    output = Path(output).resolve(); output.mkdir(parents=True, exist_ok=True)
    result = {"passed": False, "errors": [], "screenshots": [], "checks": [],
              "scope": "Chromium responsive/functionality baseline; not a full accessibility, contrast, Lighthouse, or cross-browser audit"}
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        result["errors"].append("Playwright unavailable; install the qa extra and Chromium")
        return result
    try:
        with serve(site) as origin, sync_playwright() as pw:
            browser = pw.chromium.launch()
            try:
                context = browser.new_context(service_workers="block", reduced_motion="reduce")
                def route(request_route):
                    request = request_route.request
                    parts = urlsplit(request.url)
                    if request.url.startswith(origin + "/") and request.method in ("GET", "HEAD"):
                        request_route.continue_()
                    else:
                        result["errors"].append(f"Blocked unexpected network request: {parts.scheme}://{parts.netloc}{parts.path}")
                        request_route.abort()
                context.route("**/*", route)
                pages = sorted(Path(site).rglob("*.html"))
                for file in pages:
                    relative = file.relative_to(site).as_posix()
                    for label, width, height in (("mobile", 390, 844), ("tablet", 768, 1024), ("desktop", 1440, 1000)):
                        page = context.new_page()
                        page.set_viewport_size({"width": width, "height": height})
                        prefix = f"{relative} [{label}]"
                        page.on("pageerror", lambda exc, p=prefix: result["errors"].append(f"{p}: JS error: {exc}"))
                        page.on("console", lambda msg, p=prefix: result["errors"].append(f"{p}: console error: {msg.text}") if msg.type == "error" else None)
                        page.on("response", lambda response, p=prefix: result["errors"].append(f"{p}: HTTP {response.status}: {response.url}") if response.status >= 400 else None)
                        response = page.goto(origin + "/" + relative, wait_until="networkidle", timeout=20000)
                        if response is None or response.status != 200:
                            result["errors"].append(f"{prefix}: page did not load")
                        page.evaluate("document.fonts.ready")
                        if page.evaluate("document.documentElement.scrollWidth > innerWidth + 1"):
                            result["errors"].append(f"{prefix}: horizontal overflow")
                        snapshot = page.evaluate("""() => ({title: document.title, h1: [...document.querySelectorAll('h1')].map(x=>x.innerText), unnamed: [...document.querySelectorAll('button,a')].filter(x => x.getBoundingClientRect().width && !((x.innerText || x.getAttribute('aria-label') || x.getAttribute('title') || x.querySelector('img[alt]')?.alt || '').trim())).length})""")
                        if not snapshot["title"].strip() or not any(x.strip() for x in snapshot["h1"]):
                            result["errors"].append(f"{prefix}: empty title or H1")
                        if snapshot["unnamed"]:
                            result["errors"].append(f"{prefix}: unnamed links/buttons")
                        primary = page.locator("a")
                        visible_cta = primary.evaluate_all("(els, href) => els.some(x => x.getAttribute('href') === href && x.getBoundingClientRect().width > 0)", plan["cta_href"])
                        if not visible_cta:
                            result["errors"].append(f"{prefix}: no visible primary CTA")
                        # Tab through the actual page without triggering external contact actions.
                        page.keyboard.press("Tab")
                        if page.evaluate("document.activeElement === document.body"):
                            result["errors"].append(f"{prefix}: no keyboard-focusable navigation")
                        screenshot = output / f"{relative.replace('/', '-')}-{label}.png"
                        page.screenshot(path=str(screenshot), full_page=True, animations="disabled")
                        result["screenshots"].append(str(screenshot))
                        if relative == "index.html" and label == "mobile":
                            for check in plan["interaction_checks"]:
                                try:
                                    page.locator(check["click_selector"]).click(timeout=3000)
                                    page.locator(check["visible_selector"]).wait_for(state="visible", timeout=3000)
                                    result["checks"].append({"name": check["name"], "passed": True})
                                    page.screenshot(path=str(output / f"interaction-{len(result['checks'])}.png"), full_page=True)
                                    result["screenshots"].append(str(output / f"interaction-{len(result['checks'])}.png"))
                                except Exception as exc:
                                    result["errors"].append(f"{prefix}: interaction {check['name']}: {exc}")
                                    result["checks"].append({"name": check["name"], "passed": False})
                        page.close()
                context.close()
            finally:
                browser.close()
    except Exception as exc:
        result["errors"].append(f"Browser QA could not complete: {exc}")
    result["passed"] = not result["errors"] and bool(result["screenshots"])
    write_json(output / "browser-report.json", result)
    return result
