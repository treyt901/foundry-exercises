# Part 2 — Start the Prompt Lab

**The Prompt Lab starts automatically when you open this page.** Give it a few
seconds — when the small terminal shows **✅ Prompt Lab is running**, it's ready.
If the preview panel looks blank at first, wait a moment and click its
**refresh** icon (the very first start can take 20–40 seconds).

{🔄 Restart the Prompt Lab}(bash lab.sh restart)

### A quick tour

The Prompt Lab has **three challenge tabs**. For each challenge you'll see:

- **The brief** (left): the scenario, what your prompt must do, and the
  **rubric** it will be graded on.
- **The editors** (right): depending on the challenge you'll write a **system
  prompt**, a **user prompt**, or both. Whatever you don't write is provided
  and shown read-only.
- **▶ Run & grade my prompts**: runs your prompts against *your* deployment,
  then has the model grade them against the rubric.

### How the grading works

Each run makes two kinds of calls to your deployment:

1. **Your prompts are executed** — for Challenge 1 your system prompt even
   faces a sneaky off-topic test message.
2. **A grader call** scores the *prompts themselves* (0–100) against the
   rubric and writes you feedback: what worked, and **specific edits to make
   your prompt better**.

Score **70 or higher** to pass a challenge, then record it with the
challenge page's **CHECK IT** button. You can run and refine as often as you
like — **only your best score is kept**.

> ⚠️ If a banner says the app isn't configured, go back one page and finish
> your `.env`, then press **Restart the Prompt Lab** above.

Ready? On to Challenge 1. ➡️
