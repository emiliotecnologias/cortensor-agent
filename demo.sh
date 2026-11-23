#!/usr/bin/env bash
# FixBrief demo: real commands, real output.
# Prereqs: .venv with requirements installed; for the model steps,
# Ollama running with qwen2.5:1.5b pulled (free, local, no key).
set -euo pipefail
cd "$(dirname "$0")"

.venv/bin/fixbrief --version
.venv/bin/python -m pytest tests/ -q
.venv/bin/fixbrief setup --provider ollama --model qwen2.5:1.5b
.venv/bin/fixbrief doctor
.venv/bin/fixbrief brief --device "iPhone 12" --symptom "black screen" \
  --sample iphone-black-screen.md --offline
.venv/bin/fixbrief brief --device "Samsung Galaxy A54" \
  --symptom "not charging" --sample samsung-not-charging.md \
  --lang es --provider ollama --model qwen2.5:1.5b --session demo-session
.venv/bin/fixbrief followup --session demo-session \
  --message "In one sentence, what is the most likely cause?" \
  --provider ollama --model qwen2.5:1.5b
.venv/bin/fixbrief history
cat outputs/live_model_run_receipt.json
