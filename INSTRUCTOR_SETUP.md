# Instructor Setup — make the environment bulletproof for students

**The problem this solves:** the default box for this project ships with
**Python 3.6.9**, which is too old for the Azure OpenAI SDK (and Flask 3). Also,
in Codio, **software you install in your own project does _not_ automatically
reach students** — you have to bake it into a **custom Stack** and point the
assignment at that Stack. Do that once and students never run `pip` at all.

The goal: students open the assignment, open the Guide and start the Prompt Lab, and it
just works — no dependency installs, no version errors.

---

## Overview

1. Get **Python 3.10+** onto the box.
2. Install the app's dependencies.
3. **Create a custom Stack** (a snapshot with everything baked in).
4. Point the **assignment at that Stack**.

Steps 1–2 are done once, in your own copy of the project. Steps 3–4 are what
make it persist for students.

---

## Step 1 — Get Python 3.10+ on the box

**Option A (recommended): use a newer Codio base stack.**
Codio provides base stacks that already include a modern Python. When creating
the project/assignment (or via **Project ▸ Stack ▸ Change**), pick a base stack
built on **Ubuntu 20.04/22.04** (these ship Python 3.8–3.11). Then you can skip
straight to Step 2 and just `pip install`. This avoids compiling anything.

**Option B: add Python 3.10 to the current box** (if you must stay on the old
base). In the Codio terminal:

```bash
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3.10 python3.10-venv python3.10-distutils
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
```

Verify:

```bash
python3.10 --version   # should print Python 3.10.x
```

`run.sh` automatically prefers the newest Python it can find (3.12 → 3.8), so it
will pick up `python3.10` even if the system `python3` is still 3.6.

---

## Step 2 — Install the dependencies

Using whichever modern Python you now have (examples use `python3.10`; use
`python3` instead if your base stack is already modern):

```bash
cd ~/workspace
python3.10 -m pip install -r requirements.txt
```

Confirm it imports cleanly:

```bash
python3.10 -c "import flask, openai, dotenv; print('all good')"
```

**(Optional but recommended) lock exact versions** so the stack is perfectly
reproducible:

```bash
python3.10 -m pip freeze > requirements.lock.txt
```

Do a full dry run before baking: create your `.env`, then `bash run.sh`, open
the preview, and send a test message.

---

## Step 3 — Bake it into a custom Stack

This is the step that makes your setup persist for students.

1. In the IDE menu bar: **Project ▸ Stack ▸ Create New** (creates a new Stack,
   or a new version of one, from the current box).
2. Give it a name like `foundry-prompt-lab`.
3. Wait for the snapshot to finish.

> Anything you installed in Steps 1–2 is captured in this snapshot: the Python
> version, all pip packages, everything. Students launched from this Stack get
> it pre-installed.

---

## Step 4 — Point the assignment at the Stack

1. Open the assignment in your course (**Course ▸ Assignment ▸ Settings**, or the
   assignment's **Configure** view).
2. Set its **Stack** to the one you created (`foundry-prompt-lab`).
3. Publish / re-publish the assignment.

New student instances now start from that Stack. Existing student boxes created
before the change keep the old stack — reset/republish if needed.

---

## Verifying the student experience

Open the assignment as a student (or use Codio's **Preview as student**), then:

1. Do **not** install anything.
2. Open the Guide, open the Guide and start the Prompt Lab.
3. You should see `Dependencies already installed.` followed by
   `Running on http://0.0.0.0:5000`, and the preview should load.

If you see `Installing dependencies...` instead, the packages weren't captured
in the Stack — re-check Step 2 ran under the same Python `run.sh` picks, then
re-bake (Step 3).

---

## Why not just pin everything in requirements.txt?

Pinning helps, but on Python 3.6.9 **no** pin works — even the last old
`openai==0.28` needs Python 3.7.1+, and un-pinned installs fall back to an
ancient unrelated `openai==0.10.5` that drags in `pandas`, which also dropped
3.6. The only real fixes are a newer Python plus baking the environment into a
Stack. Baking also means the student install is offline and instant, so a flaky
network can't break their start.
