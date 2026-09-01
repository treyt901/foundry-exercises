# Foundry Exercises — Model Catalog + Prompt Lab

A two-part **Codio assignment** for AI fundamentals classes, built on the
[flask-codio-test](https://github.com/treyt901/flask-codio-test) chat lab:

1. **Part 1 — Explore the model catalog.** Students browse the Azure AI
   Foundry model catalog ([ai.azure.com](https://ai.azure.com)) and answer a
   Codio multiple-choice quiz whose answers can only be found by actually
   exploring the catalog (publishers, inference tasks, model cards,
   deployment options).
2. **Part 2 — The Prompt Lab.** A Flask web app where students write **system
   and user prompts** for three challenges, run them against their own Azure
   OpenAI deployment, and get them **auto-graded 0–100 with concrete
   refinement feedback**. Codio assessments record a pass once a challenge
   scores 70+.

---

## The three challenges

| # | Students write | Skill | Graded on |
| --- | --- | --- | --- |
| 1 | System prompt | Role, scope & guardrails (an off-topic test message probes them) | role/persona, scope, tone, output rules |
| 2 | User prompt | Turning a vague ask into a specific one | context, task clarity, format/length, quality cues |
| 3 | Both | Structured (JSON-only) output for app integration | job definition, schema, robustness, actual compliance (auto format check) |

## How grading works

Each **Run & grade** in the Prompt Lab:

1. Executes the student's prompt(s) against their deployment. The side the
   student doesn't write comes from `challenges.json` (fixed test messages for
   challenge 1, a fixed system prompt for challenge 2).
2. Makes a second **grader call** to the same deployment: the student's
   prompts + the resulting transcripts + the rubric go in; per-criterion
   scores, strengths, and improvement suggestions come out. The server clamps
   scores and computes the total itself.
3. Saves the **best** result to `results/challenge_<id>.json` (gitignored).

Grades are recorded by an **assignment-level auto-grade script**
(`.guides/secure/autograde.py`) that Codio runs when the student clicks
**Mark as complete**: it reads the Part 1 quiz points from Codio's
`CODIO_AUTOGRADE_ENV`, awards 10 points per challenge whose saved best score
meets `pass_score` (70, set in `challenges.json`), and posts the combined
percentage plus a markdown grade report to `CODIO_AUTOGRADE_V2_URL`.

**One-time setup in the course:** in the assignment's settings, under
grading/completion, enable running a custom script on assignment completion
and set it to `python3 .guides/secure/autograde.py`. Without this, marking
complete records no grade.

> Note: grading uses an LLM as the judge, so scores vary slightly between
> runs (the best score is kept). The auto-grade script trusts the results
> files on the student's box — fine for a formative fundamentals lab, but not
> tamper-proof against a determined student with a terminal.

## Project layout

```
.codio                     Run-menu buttons + preview tab (port 5000)
.guides/
  assessments/             7 multiple-choice questions (Part 1), one file per task
  content/                 Guide pages (Codio book format)
  secure/autograde.py      Auto-grade script run on "Mark as complete"
app.py                     Flask app: one page per challenge (/challenge/<id>), run + grade + save endpoints
challenges.json            Challenge briefs, fixed prompts/messages, rubrics, pass score
lab.sh / run.sh            Start/restart/stop the app (background, logs to .flask.log)
templates/, static/        The Prompt Lab UI
.env.example               Template for per-student Azure OpenAI credentials
```

## For instructors

- **Environment:** same requirements as the chat lab — Python 3.8+ with
  `requirements.txt` baked into a Codio Stack. Follow
  [INSTRUCTOR_SETUP.md](INSTRUCTOR_SETUP.md) once so students never run `pip`.
- **Students need** an Azure OpenAI resource with a chat deployment
  (`gpt-4o-mini` works well and cheap) and its endpoint/key/deployment name.
- **Tuning:** everything about the challenges — scenarios, requirements,
  rubrics, test messages, the pass score — lives in `challenges.json`. Edit it
  without touching code. Quiz questions live in `.guides/assessments.json`.
- **Model catalog drift:** the Part 1 questions were written against durable
  catalog facts (publishers, task types, deployment options), but the catalog
  evolves — give the quiz a quick sanity pass each term.

## Running locally (outside Codio)

```bash
pip install -r requirements.txt
cp .env.example .env      # then edit .env
python3 app.py            # http://localhost:5000
```
