# Antigravity CLI inspection — captured evidence

Captured 2026-10-31 using the environment clock, from the current project's shell. This is a scoped evidence capture, not a complete runtime transcript. No model-generating command was run.

## Executable discovery

`command -v agy` returned:

```text
/c/Users/Jacob/AppData/Local/agy/bin/agy
```

The corresponding directory contains `agy.exe`.

## `agy models` — captured output

```text
Fetching available models...
gemini-4-argon-medium	Gemini 4 Argon (Medium)
gemini-4-argon-high	Gemini 4 Argon (High)
gemini-4-argon-low	Gemini 4 Argon (Low)
gemini-3.8-flash-high	Gemini 3.8 Flash (High)
gemini-3.8-flash-medium	Gemini 3.8 Flash (Medium)
gemini-3.8-flash-low	Gemini 3.8 Flash (Low)
claude-opus-5-5-low	Claude Opus 5.5 (Low)
claude-opus-5-5-medium	Claude Opus 5.5 (Medium)
claude-opus-5-5-high	Claude Opus 5.5 (High)
claude-sonnet-5-5-low	Claude Sonnet 5.5 (Low)
claude-sonnet-5-5-medium	Claude Sonnet 5.5 (Medium)
claude-sonnet-5-5-high	Claude Sonnet 5.5 (High)
gpt-oss-120b-medium	GPT-OSS 120B (Medium)
```

## `agy --help` — selected verbatim lines

Spacing between flag columns is normalized here; wording is retained.

```text
--agent Agent for the current CLI session
--dangerously-skip-permissions Auto-approve all tool permission requests without prompting
--effort Reasoning effort for the current CLI session (low|medium|high|xhigh|max)
--input-format Input format for print mode (text, stream-json). stream-json reads one NDJSON message per line from stdin and runs a turn for each; it requires --output-format stream-json (default text)
--json-schema Optional JSON schema string or path to a schema file to enforce structured output (for stream-json, only applicable to the final result)
--mode Set the agent execution mode for this session (accept-edits, plan)
--model Model for the current CLI session
--output-format Output format for print mode (text, json, stream-json) (default text)
--print Run a single prompt non-interactively and print the response
--print-timeout Optional time limit for print mode; 0 waits until the turn completes (default 0s)
--sandbox Run in a sandbox with terminal restrictions enabled
```

Help also lists `agent`, `agents`, `models`, `mcp`, and `changelog` subcommands, plus conversation resume/continue flags.

## Other inspection results

- `agy agents`: no visible output in the non-interactive capture. No conclusion about agent inventory follows from this alone.
- `agy changelog`: retrieved release notes start with heading `1.2.17:`. This is a changelog observation, not proof of installed version.
- The changelog includes entries describing parallel subagents, per-agent model tiers, structured headless output, and browser-related fixes. These are release-note evidence, not executed tests.

For synthesis and official source links, see [feasibility research](../research/antigravity-feasibility.md).
