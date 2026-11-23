# Cortensor Hackathon #5 — Submission Pack (FixBrief Agent)

Hackathon: https://dorahacks.io/hackathon/2418/detail
Deadline: **18 Dec 2026** (build period 16 Oct–18 Dec 2026; DoraHacks
event window ends 19 Dec 2026 07:59 UTC — submit well before).
Prize pool: $1,150 in $COR equivalent (1st $500 / 2nd $300 / 3rd $200 /
4th $100 / 5th $50; each 50% liquid upfront + 50% one-month staking lock).

## Verified brief (from the official DoraHacks page, crawled 2026-10-15)

- Objective: "Submit an agent or agent-powered application that uses
  the OpenMinion 0.1 Python SDK as a meaningful part of its runtime;
  completes one useful, repeatable workflow; shows a real model-backed
  run in a short demo; and identifies the OpenMinion building blocks
  tested, including any bugs or rough edges found."
- How to participate: build with the documented 0.1 Python SDK; "Submit
  a PR. Link your public project and submission materials in a pull
  request to the dedicated Hackathon #5 repository"; "Include a 1–5
  minute video showing the agent running and its result."
- Submission checklist: public source repository + README with setup
  and run instructions; short explanation of the OpenMinion SDK
  workflow; one working example + 1–5 min demo video; Building Blocks
  Tested note; What We Learned note.
- Evaluation: working functionality 25% · meaningful SDK usage 20% ·
  reproducibility/demo 20% · building-block findings 25% · relevance
  to Cortensor builder workflows 10%.
- Terms (exact quote): "Cortensor may require identity or eligibility
  checks for prize distribution." No SSN/W-9 requirement is stated
  anywhere in the brief; prizes are paid in $COR to a winner-designated
  address. **Flag for owner: verify at prize-claim time that any
  identity check stays wallet/passport-level; if SSN/W-9 is demanded,
  stop the claim (owner hard rule).**
- Portal/Gemma4 optional: "Portal is optional for qualification";
  "Participants without access will not be penalized."
- AI-assisted development is allowed; participants must be able to
  explain and demonstrate what they built.

## Submission repository (verified from live PRs)

The dedicated Hackathon #5 repository is **cortensor/community-projects**:
live PRs #93–#102 (e.g. "[Hackathon #5] feat(apps): add
minionbench-ops") add projects under `apps/<project>/` with README,
STATUS, RELEASE, PROJECTS.yml, BUILDING_BLOCKS_TESTED, WHAT_WE_LEARNED,
and links to a standalone repo + demo video. FixBrief follows the same
layout under `apps/fixbrief-agent/`.

## DoraHacks BUIDL form text

**Project name:** FixBrief Agent — Multilingual Repair-Brief Agent on OpenMinion

**Tagline:** Device + symptom in, validated EN/ES/PT/AR repair brief out — deterministic tools collect facts, the OpenMinion agent reasons over them.

**Description:**
FixBrief is a Python agent built on the OpenMinion 0.1.24 SDK that
completes one repeatable workflow for phone-repair technicians: turn a
device + symptom (+ public sources or bundled field notes) into a
schema-validated troubleshooting brief in English, Spanish, Portuguese,
or Arabic. Deterministic READ_ONLY tools fetch/load sources and extract
causes, steps, tools, and warnings; the agent (forced first tool call,
typed `RepairBrief` output, durable sessions, approval-gated write
tool) structures the brief and persists it to SQLite with a JSON run
receipt. The recorded demo runs a free local model (Ollama
qwen2.5:1.5b, no API key); any OpenAI-compatible provider — including
Cortensor Portal — is a one-command swap. Every brief is labeled with
its provenance (`openminion:<provider>/<model>` vs
`deterministic-fallback`), and 21 offline tests cover extraction,
glossary, rendering, storage, CLI, and SDK wiring.

**OpenMinion SDK workflow:** run-scoped `@tool` functions
(`get_source_facts`, `lookup_term`, approval-gated
`save_brief_markdown`), `forced_tools`, `output_type` typed output,
`session_id` continuity with follow-up turns, `approval_callback`,
`ProviderError`/`TurnTimeoutError`/`AgentOutputValidationError`
handling mapped to CLI exit codes, project-local `agents.json` via
`config init`.

**Links:**
- Standalone repository: TODO_REPO_URL
- Community-projects PR: TODO_PR_URL
- Demo video (1–5 min): TODO_VIDEO_URL
- Building Blocks Tested: BUILDING_BLOCKS_TESTED.md (in repo + PR)
- What We Learned: WHAT_WE_LEARNED.md (in repo + PR)

**Team:** Emilio Tecnologías (solo). AI-assisted development disclosed
in README.

## PR details (cortensor/community-projects)

- Branch: `dev-emiliotecnologias` (per repo workflow: dev-{userid})
- Title: `[Hackathon #5] feat(apps): add fixbrief-agent (v0.1.0, MIT, OpenMinion 0.1.24)`
- Body: project summary + links (standalone repo, DoraHacks BUIDL,
  demo video) + checks run (`pytest` 21 passed; live Ollama receipt).
- Files: `apps/fixbrief-agent/**` (code, samples, tests, docs,
  outputs/receipt + transcript; demo video linked from standalone repo).

## Owner actions still needed (not done by agent)

1. Create the DoraHacks BUIDL entry and paste the form text above
   (requires DoraHacks account login).
2. If the project wins: designate the $COR payout address and complete
   the 50% staking-lock step; verify any identity check does not demand
   SSN/W-9 (stop if it does).
3. Optional: request Cortensor Portal access to add a hosted-model run.
