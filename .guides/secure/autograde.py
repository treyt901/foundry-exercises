#!/usr/bin/env python3
"""Assignment-level auto-grade script for Foundry Exercises.

Codio runs this when a student clicks "Mark as complete". It combines:
  * Part 1 quiz points, read from the CODIO_AUTOGRADE_ENV JSON that Codio
    passes in (all remaining assessments in this project are the quiz), and
  * Part 2 challenge results, read from the results/challenge_<id>.json
    files the Prompt Lab writes (10 points per challenge at pass_score+),
then posts the combined percentage to CODIO_AUTOGRADE_V2_URL with a
markdown feedback report.

Wire-up (one time, in the course): assignment Settings -> Grading ->
"Run custom assessment script on assignment completion" ->
    python3 .guides/secure/autograde.py

Codio treats a non-zero exit as grade 0, so this script always exits 0 and
posts the best grade it can compute. Run with --dry-run to print instead of
post (for instructor testing; students marking complete never see this).
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHALLENGE_POINTS = 10


def load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None


def quiz_points():
    """Earned/total assessment points from Codio's autograde env JSON.

    Returns (points, total_points, note). Handles the env var holding either
    the JSON itself or a path to a JSON file, and falls back gracefully when
    the expected keys are missing so a format drift can't zero anyone's grade.
    """
    raw = os.environ.get("CODIO_AUTOGRADE_ENV", "")
    data = None
    if raw:
        if os.path.exists(raw):
            data = load_json(raw)
        else:
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                data = None
    if not isinstance(data, dict):
        return None, None, "quiz points unavailable - graded on the challenges only"

    stats = (data.get("assessments") or {}).get("stats") or {}
    points, total = stats.get("points"), stats.get("totalPoints")
    if isinstance(points, (int, float)) and isinstance(total, (int, float)) and total > 0:
        return float(points), float(total), None
    return None, None, "quiz points unavailable - graded on the challenges only"


def challenge_results(pass_score, challenges):
    """One row per challenge: (id, title, best total or None, earned points)."""
    rows = []
    for challenge in challenges:
        cid = challenge["id"]
        record = load_json(ROOT / "results" / f"challenge_{cid}.json") or {}
        total = record.get("total") if record.get("challenge_id") == cid else None
        earned = CHALLENGE_POINTS if isinstance(total, (int, float)) and total >= pass_score else 0
        rows.append((cid, challenge["title"], total, earned))
    return rows


def build_feedback(rows, pass_score, quiz_earned, quiz_total, quiz_note):
    lines = ["### Foundry Exercises — grade report", ""]
    if quiz_note:
        lines.append(f"*Part 1 quiz:* {quiz_note}")
    else:
        lines.append(f"*Part 1 quiz:* **{quiz_earned:g} / {quiz_total:g}** points")
    lines += ["", "*Part 2 challenges* (pass a challenge with a Prompt Lab score of "
              f"{pass_score}+ to earn its {CHALLENGE_POINTS} points):", ""]
    for cid, title, total, earned in rows:
        if total is None:
            status = "no graded attempt in the Prompt Lab"
        else:
            status = f"best Prompt Lab score {total}/100"
        lines.append(f"- **Challenge {cid} — {title}:** {earned}/{CHALLENGE_POINTS} points ({status})")
    lines += ["", "Re-open the assignment, improve your work, and mark it complete "
              "again to update this grade."]
    return "\n".join(lines)


def post_grade(grade, feedback):
    url = os.environ.get("CODIO_AUTOGRADE_V2_URL") or os.environ.get("CODIO_AUTOGRADE_URL")
    if not url:
        print("No CODIO_AUTOGRADE_*_URL in the environment - not posting.")
        return False
    payload = urllib.parse.urlencode(
        {"grade": grade, "format": "md", "feedback": feedback}
    ).encode()
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, data=payload), timeout=30) as resp:
                resp.read()
            return True
        except Exception as exc:  # noqa: BLE001 - keep retrying, never crash
            print(f"Posting grade failed (attempt {attempt + 1}/3): {exc}")
    return False


def main():
    config = load_json(ROOT / "challenges.json") or {}
    pass_score = config.get("pass_score", 70)
    challenges = config.get("challenges", [])

    quiz_earned, quiz_total, quiz_note = quiz_points()
    rows = challenge_results(pass_score, challenges)

    earned = sum(r[3] for r in rows)
    possible = CHALLENGE_POINTS * len(rows)
    if quiz_note is None:
        earned += quiz_earned
        possible += quiz_total
    grade = round(100 * earned / possible) if possible else 0

    feedback = build_feedback(rows, pass_score, quiz_earned, quiz_total, quiz_note)
    print(f"Computed grade: {grade} ({earned:g}/{possible:g} points)")

    if "--dry-run" in sys.argv:
        print(feedback)
    else:
        post_grade(grade, feedback)
    sys.exit(0)  # never fail the submission


if __name__ == "__main__":
    main()
