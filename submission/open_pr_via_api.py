#!/usr/bin/env python3
"""Open the Hackathon #5 PR via the GitHub API (no local clone needed).

STATUS: PREPARED, NOT RUN. Two security notices flagged (1) the Ollama
binary archive and (2) a local clone of cortensor/community-projects
during development. This script avoids both: it never clones or runs
git inside the upstream repo — it creates a branch + files + PR on the
fork purely through `gh api`. Run only after owner approval.

Usage:
    python3 submission/open_pr_via_api.py            # dry-run (default)
    python3 submission/open_pr_via_api.py --execute  # actually open the PR
"""

from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORK = "emiliotecnologias/community-projects"
UPSTREAM = "cortensor/community-projects"
BRANCH = "dev-emiliotecnologias"
APP_DIR = "apps/fixbrief-agent"
TITLE = "[Hackathon #5] feat(apps): add fixbrief-agent (v0.1.0, MIT, OpenMinion 0.1.24)"

# Files mirrored into the PR (relative to repo root). Generated outputs
# (receipt, transcript, briefs) are added when present.
BASE_FILES = [
    ".env.example", ".gitignore", "BUILDING_BLOCKS_TESTED.md", "LICENSE",
    "PROJECTS.yml", "README.md", "RELEASE.md", "STATUS.md",
    "WHAT_WE_LEARNED.md", "demo.sh", "pyproject.toml", "record_demo.py",
    "requirements.txt",
    "samples/iphone-black-screen.md", "samples/redmi-boot-loop.md",
    "samples/samsung-not-charging.md",
    "src/fixbrief/__init__.py", "src/fixbrief/__main__.py",
    "src/fixbrief/agent.py", "src/fixbrief/cli.py",
    "src/fixbrief/config.py", "src/fixbrief/facts.py",
    "src/fixbrief/fallback.py", "src/fixbrief/glossary.py",
    "src/fixbrief/models.py", "src/fixbrief/render.py",
    "src/fixbrief/sources.py", "src/fixbrief/store.py",
    "tests/test_brief_offline.py", "tests/test_facts.py",
    "tests/test_glossary.py", "tests/test_sdk_wiring.py",
    "tests/test_sources.py",
]
OPTIONAL_FILES = [
    "outputs/live_model_run_receipt.json",
    "outputs/demo_transcript.txt",
]


def gh_api(args: list[str], payload: dict | None = None) -> dict:
    cmd = ["gh", "api", *args]
    result = subprocess.run(
        cmd,
        input=json.dumps(payload) if payload is not None else None,
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"gh api failed: {result.stderr[:800]}")
    return json.loads(result.stdout) if result.stdout.strip() else {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true",
                        help="Actually create branch/files/PR (default: dry-run)")
    args = parser.parse_args()

    files = [f for f in BASE_FILES if (ROOT / f).exists()]
    files += [f for f in OPTIONAL_FILES if (ROOT / f).exists()]
    missing = [f for f in BASE_FILES if not (ROOT / f).exists()]
    print(f"files to mirror: {len(files)} (missing: {missing or 'none'})")
    for f in files:
        print(f"  {APP_DIR}/{f}")
    print(f"fork: {FORK}  branch: {BRANCH}  upstream: {UPSTREAM}")
    print(f"PR title: {TITLE}")

    if not args.execute:
        print("\nDRY-RUN only. Re-run with --execute after owner approval.")
        return 0

    main_ref = gh_api([f"repos/{FORK}/git/ref/heads/main"])
    sha = main_ref["object"]["sha"]
    print(f"fork main sha: {sha}")
    try:
        gh_api([f"repos/{FORK}/git/refs", "-X", "POST"],
               {"ref": f"refs/heads/{BRANCH}", "sha": sha})
        print(f"created branch {BRANCH}")
    except RuntimeError as exc:
        print(f"branch may already exist: {exc}")

    for rel in files:
        content = (ROOT / rel).read_bytes()
        gh_api(
            [f"repos/{FORK}/contents/{APP_DIR}/{rel}", "-X", "PUT"],
            {
                "message": f"feat(apps): add fixbrief-agent {rel}",
                "content": base64.b64encode(content).decode(),
                "branch": BRANCH,
            },
        )
        print(f"uploaded {APP_DIR}/{rel}")

    body = (ROOT / "submission" / "PR_BODY.md").read_text(encoding="utf-8")
    pr = gh_api(
        [f"repos/{UPSTREAM}/pulls", "-X", "POST"],
        {"title": TITLE, "body": body, "head": f"emiliotecnologias:{BRANCH}",
         "base": "main"},
    )
    print(f"PR opened: {pr.get('html_url')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
