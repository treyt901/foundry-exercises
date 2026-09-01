#!/usr/bin/env python3
"""Codio assessment checker for the Prompt Lab challenges.

Usage (from the Codio "Advanced Code Test" assessments):
    python3 .guides/secure/check_challenge.py <challenge id>

The Prompt Lab (app.py) saves each challenge's best grade to
results/challenge_<id>.json. This script passes (exit 0) when that grade
meets the pass score, and otherwise prints the student's current score and
the grader's refinement feedback so they know what to do next.
"""

import json
import sys
from pathlib import Path

# This file lives at .guides/secure/check_challenge.py — the project root is
# two directories up, wherever Codio runs the assessment from.
ROOT = Path(__file__).resolve().parents[2]


def fail(*lines):
    print("\n".join(lines))
    sys.exit(1)


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        fail("Checker error: expected a challenge number (1, 2 or 3).")
    challenge_id = int(sys.argv[1])

    try:
        with open(ROOT / "challenges.json", encoding="utf-8") as fh:
            config = json.load(fh)
    except (OSError, json.JSONDecodeError):
        fail("Checker error: challenges.json could not be read.")
    pass_score = config.get("pass_score", 70)

    result_path = ROOT / "results" / f"challenge_{challenge_id}.json"
    if not result_path.exists():
        fail(
            f"No graded attempt found for Challenge {challenge_id} yet.",
            "Open the Prompt Lab, write your prompt(s), and press",
            "'Run & grade my prompts' first — then come back and check again.",
        )

    try:
        with open(result_path, encoding="utf-8") as fh:
            record = json.load(fh)
    except (OSError, json.JSONDecodeError):
        fail(
            f"The saved result for Challenge {challenge_id} could not be read.",
            "Run & grade the challenge again in the Prompt Lab, then re-check.",
        )

    total = record.get("total", 0)
    if record.get("challenge_id") != challenge_id:
        fail("Checker error: the saved result is for a different challenge.")

    if total >= pass_score:
        print(f"✅ Challenge {challenge_id} passed with {total}/100 (needed {pass_score}).")
        for strength in record.get("strengths", [])[:2]:
            print(f"   • {strength}")
        sys.exit(0)

    print(f"Not there yet: your best score is {total}/100 (you need {pass_score}).")
    improvements = record.get("improvements", [])
    if improvements:
        print("The grader suggested:")
        for tip in improvements:
            print(f"   • {tip}")
    print("Refine your prompt in the Prompt Lab, run & grade again, then re-check.")
    sys.exit(1)


if __name__ == "__main__":
    main()
