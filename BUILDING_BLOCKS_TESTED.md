# Building Blocks Tested — FixBrief on OpenMinion 0.1.24

Environment: Linux x86_64, Python 3.12, `openminion==0.1.24` (PyPI),
project-local `OPENMINION_HOME`. Providers exercised: `echo` (SDK demo
provider) and `ollama` (`qwen2.5:1.5b`, local, no credentials).
<!-- MODEL-RUN-SECTION: updated after the recorded Ollama run -->

## What was tested

| Building block | How FixBrief uses it | Result |
|---|---|---|
| Python SDK install | `pip install openminion==0.1.24` | ✅ Works (see rough edge 1) |
| `config init` | `openminion config init --provider echo/ollama` into project-local home | ✅ Works; `Agent(config_path=...)` picks it up |
| Decorated tools (`@tool`) | 2× `READ_ONLY` + 1 bare write tool, run-scoped | ✅ Works; functions stay plain callables (unit-testable) |
| `forced_tools` | `forced_tools=["get_source_facts"]` | ⚠️ No-op under `echo` (see finding 2); verified with real model in demo |
| Typed output (`output_type`) | `output_type=RepairBrief` (pydantic) | ✅ Correctly rejects echo replies with `AgentOutputValidationError` |
| Sessions | `session_id` + follow-up turn | ✅ Session/run IDs returned in `AgentRunResult` |
| Approval callback | Write tool gated by `approval_callback(tool, args, id) -> bool` | ✅ Signature confirmed in SDK source; `READ_ONLY` tools skip prompts under default policy |
| Provider errors | `ProviderError` → CLI exit 1 | ✅ Taxonomy documented in `API_COMPATIBILITY.md`; mapped in CLI |
| Turn timeout | `TurnTimeoutError` → CLI exit 3 | ✅ Mapped in CLI |
| Run receipts | `result.stats` / `result.metadata` → JSON receipt | ✅ Rich metadata (tokens, tool counts, durations) |

## Findings (what worked, what broke, rough edges)

### 1. Install needs a disk-backed temp dir in small-tmpfs containers (environment, not SDK bug)
`pip install openminion` failed with `OSError(28, 'No space left on
device')` when `/tmp` was a 512 MB tmpfs, because pip stages large
wheels (SQLAlchemy, cryptography) there. Setting `TMPDIR` and
`PIP_CACHE_DIR` to a workspace path fixed it. Worth a one-line note in
the install docs for container/CI users.

### 2. `echo` + `forced_tools` executes zero tools
With the echo provider, `agent.run(...)` returned
`stats={'tool_calls': 0, ...}` even with `forced_tools=["lookup_order"]`
— echo just echoes the prompt. This is consistent with the docs
("demo mode does not call a model"), but it means **forced-tool
verification is impossible in demo mode**. A test double that actually
invokes forced tools with canned args would make SDK wiring testable
without a model. FixBrief's test suite asserts the honest failure
instead: echo + `output_type` raises `AgentOutputValidationError`
(exit code 2), so echo output can never be mistaken for a model brief.

### 3. Ollama default timeout (60 s) is too low for CPU inference
The generated `agents.json` sets `providers.ollama.timeout_seconds=60`.
On CPU-only hardware a 1.5B model needs longer for multi-step tool
loops. FixBrief patches it to 300 s in its project config. Consider
raising the Ollama default or documenting the knob next to the provider
setup flow.

### 4. Decorated tools remain directly callable — excellent for testing
`@tool(...)` returns the original function, so tool logic can be unit
tested without booting the runtime (`get_source_facts("sample", ...)`
in pytest). This is a genuine strength of the 0.1 SDK surface.

### 5. Structured-output compatibility helps weak models
Per `API_COMPATIBILITY.md`, one schema-valid JSON object wrapped in
provider prose is accepted during 0.1.x. That tolerance is what makes
typed output viable with small local models that add chatter around
JSON. FixBrief relies on it (and still validates with pydantic).

### 6. Sandbox proxy env breaks httpx twice (environment findings, worked around)
Two real failures hit during development in a proxied sandbox:
(a) `NO_PROXY` containing bracketed IPv6 (`[::1]`) makes httpx raise
`InvalidURL: Invalid port: ':1]'` when building proxy patterns — this
would break any httpx-based provider call. FixBrief strips bracketed
entries (`normalize_no_proxy`) before SDK runs. (b) A TLS-intercepting
egress proxy signs with a local CA present in the system bundle /
`SSL_CERT_FILE` but not in certifi, so default httpx verification
fails with `CERTIFICATE_VERIFY_FAILED`. FixBrief's fetcher prefers
`SSL_CERT_FILE`/system bundle. Builders behind corporate proxies will
hit both; the SDK could normalize these once in its HTTP layer.

### 7. Approval callback contract is discoverable only in source
The callback signature `(tool_name, args, approval_id) -> bool` is not
in the PyPI README examples; it was confirmed in
`openminion/api/agent.py`. A 5-line example in `examples/sdk/` would
save every builder this archaeology. FixBrief denies the write tool by
default and only allows `save_brief_markdown` with `--yes`.

## Reproduce

```bash
.venv/bin/python -m pytest tests/ -q          # 25 offline tests
.venv/bin/fixbrief setup --provider echo      # credential-free config
.venv/bin/fixbrief brief --device "Samsung Galaxy A54" \
  --symptom "not charging" --sample samsung-not-charging.md \
  --provider echo                             # exits 2 (validation), by design
.venv/bin/fixbrief setup --provider ollama --model qwen2.5:1.5b
.venv/bin/fixbrief brief --device "Samsung Galaxy A54" \
  --symptom "not charging" --sample samsung-not-charging.md --lang es
cat outputs/live_model_run_receipt.json       # provider/model/session/stats
```
