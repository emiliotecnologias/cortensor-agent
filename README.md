# FixBrief Agent — Multilingual Repair-Brief Agent on OpenMinion

**Cortensor Hackathon #5 entry** · Built with the OpenMinion 0.1 Python SDK (`openminion==0.1.24`) · MIT

FixBrief turns a device + symptom into a validated, structured
troubleshooting brief in English, Spanish, Portuguese, or Arabic. It is
built for phone-repair technicians and guide writers who need the same
repeatable workflow every time: collect facts from sources, structure
them, and render a brief a human can act on.

## Design rule: the model never fetches anything

Deterministic Python tools collect and structure facts (fetch a URL or
load a bundled note, extract causes/steps/tools/warnings, look up exact
glossary terms). The model only reasons over those facts and returns a
schema-validated `RepairBrief`. Every brief carries a `generated_by`
provenance label — `openminion:<provider>/<model>` for a model-backed
run, `deterministic-fallback` when no model was used — so the two can
never be confused.

## Workflow

```
device + symptom + sources
        │
        ▼
┌──────────────────────────────┐   get_source_facts (READ_ONLY, forced first)
│ OpenMinion Agent             │──► fetch / load ──► extract facts (pure Python)
│  output_type=RepairBrief     │──► lookup_term (EN/ES/PT/AR glossary)
│  session_id per run          │──► save_brief_markdown (write, approval-gated)
└──────────────────────────────┘
        │
        ▼
validated brief (JSON + Markdown) ──► SQLite history + run receipt
```

## Quick start

Requires Python 3.11+. The recorded demo uses a **free local model**
(Ollama, no account, no API key).

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install -e .

# 1) Free local model (no credentials):
ollama serve &                  # if not already running
ollama pull qwen2.5:1.5b

# 2) Project-local OpenMinion config (never touches ~/.openminion):
.venv/bin/fixbrief setup --provider ollama --model qwen2.5:1.5b
.venv/bin/fixbrief doctor

# 3) Model-backed brief from a bundled offline source:
.venv/bin/fixbrief brief --device "Samsung Galaxy A54" \
  --symptom "not charging" --sample samsung-not-charging.md --lang es

# 4) Same session, follow-up turn (session continuity):
.venv/bin/fixbrief followup --message "Summarize the top cause in one sentence."

# 5) History:
.venv/bin/fixbrief history
```

No model handy? The deterministic offline path runs anywhere:

```bash
.venv/bin/fixbrief brief --device "iPhone 12" --symptom "black screen" \
  --sample iphone-black-screen.md --offline
```

Live sources work too (public URLs only; the tool fetches, the model doesn't):

```bash
.venv/bin/fixbrief brief --device "Redmi Note 12" --symptom "boot loop" \
  --url "https://example.com/repair-notes" --provider ollama
```

## Providers

| Provider | Credential | Notes |
|---|---|---|
| `ollama` (default) | none | Free, local. Demo recorded with `qwen2.5:1.5b`. |
| `echo` | none | SDK demo provider. Plumbing only — **not** a model run. |
| `openrouter`, `openai`, `groq`, `cerebras`, `anthropic`, `gemini` | API key via env | Set the env var named in `.env.example`, then `fixbrief setup --provider <name>`. |
| `cortensor-portal` | `CORTENSOR_API_KEY` | Hosted Cortensor inference; access is coordinated with the hackathon team (optional per the brief). |

Provider failures, validation failures, and turn timeouts map to stable
exit codes (`1` provider, `2` validation, `3` timeout, `4` usage),
mirroring the SDK's `ProviderError` / `AgentOutputValidationError` /
`TurnTimeoutError` taxonomy. `--fallback` emits a clearly labeled
deterministic brief instead of failing.

## OpenMinion building blocks used

- Run-scoped decorated tools (`@tool(min_scope="READ_ONLY", idempotent=True)` ×2, one bare write tool)
- `forced_tools` — verifiable first tool call
- Typed output — `output_type=RepairBrief` (pydantic)
- Durable sessions — `session_id` + follow-up turn
- Approval callback — write tool denied unless `--yes`
- Provider abstraction — same agent code across ollama/echo/hosted providers
- Run receipts — `AgentRunResult` stats/metadata persisted to `outputs/live_model_run_receipt.json`

See `BUILDING_BLOCKS_TESTED.md` for what worked, what broke, and exact
reproduction notes, and `WHAT_WE_LEARNED.md` for product feedback.

## Tests

```bash
.venv/bin/python -m pytest tests/ -q
```

21 tests, fully offline (fact extraction, glossary, fallback briefs,
rendering, SQLite store, CLI, and SDK wiring against the echo provider).

## Demo

`demo-video.mp4` is rendered from a real terminal session by
`record_demo.py` (no staged footage): setup, doctor, tests, offline
brief, model-backed brief with Ollama, session follow-up, and history.
The full text transcript is in `outputs/demo_transcript.txt`.

## Honest limits

- Fact extraction is heuristic (section parsing + signal patterns). It
  is conservative and testable, but it is not semantic understanding.
- A 1.5B local model is the weakest link: briefs are grounded in tool
  facts and schema-validated, but wording quality scales with the model.
  Any OpenAI-compatible provider can be swapped in without code changes.
- Bundled samples are original field notes written for this project,
  covering three common faults. They demonstrate the workflow; they are
  not a substitute for board-level schematics.
- Arabic glossary terms are Modern Standard Arabic starter terms.

## License

MIT. AI-assisted development disclosure: this project was built with AI
assistance; all code, tests, and demo output in this repository were
executed and verified locally by the submitter.

— Emilio Tecnologías
