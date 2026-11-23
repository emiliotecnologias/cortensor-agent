Adding `fixbrief-agent` for Cortensor Hackathon #5 under MIT (`openminion==0.1.24`).

FixBrief is a multilingual (EN/ES/PT/AR) phone-repair brief agent: deterministic READ_ONLY tools collect facts from sources (bundled field notes or public URLs), and the OpenMinion Agent returns a schema-validated `RepairBrief` (typed output, forced first tool call, durable sessions, approval-gated write tool). Every brief carries a `generated_by` provenance label, runs are persisted to SQLite with a JSON receipt, and 25 offline tests cover extraction, glossary, rendering, storage, CLI, and SDK wiring.

Links:
- Standalone repository: https://github.com/emiliotecnologias/cortensor-agent
- Demo video (real terminal session, H.264 MP4): https://github.com/emiliotecnologias/cortensor-agent/raw/main/demo-video.mp4
- Demo transcript: https://github.com/emiliotecnologias/cortensor-agent/blob/main/outputs/demo_transcript.txt
- SDK findings & feedback: `apps/fixbrief-agent/BUILDING_BLOCKS_TESTED.md`, `apps/fixbrief-agent/WHAT_WE_LEARNED.md`

Checks run:
- `pytest tests/ -q`: 25 passed (fully offline)
- Live model run receipt: `outputs/live_model_run_receipt.json` (provider/model/session/stats)
- Echo provider correctly fails typed-output validation (exit 2) — asserted in tests so demo mode can never masquerade as a model run

— Emilio Tecnologías (AI-assisted development disclosed in README)
