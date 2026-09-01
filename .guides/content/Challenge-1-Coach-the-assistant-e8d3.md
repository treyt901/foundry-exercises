# Challenge 1 — Coach the assistant

> ⚠️ If a banner on the left says the app isn't configured, go back to the **Set up your endpoint** page near the start of this guide, finish your `.env`, then press **Restart the Prompt Lab** below.

{🔄 Restart the Prompt Lab}(bash lab.sh restart)

**Skill: writing a system prompt.** A *system prompt* is the standing instruction a model receives before any user says anything. It's how an app turns a general-purpose model into *its* assistant: it sets the role, the rules, and the personality.

### Your job

The panel beside this page already shows **Challenge 1**. Write a system prompt that turns the model into a support assistant for **Bluff City Bikes**. A good system prompt usually covers:

- **Role** — *"You are …"* Who is the assistant? Give it a name and a job.
- **Scope** — what it should help with, and what to do when asked anything  else (decline politely, steer back to the shop).
- **Tone** — how it should sound for this audience.
- **Rules** — concrete, checkable output constraints (length, closing line…).

### The twist 👀

Your prompt is tested with **two** messages — a normal customer question, and an off-topic request designed to lure the assistant away from its job. Vague scope instructions ("be helpful about bikes") tend to fail that second test; explicit guardrails ("if asked about anything unrelated to the shop, politely decline and offer to help with…") tend to pass it.

### Pass it

Press **▶ Run & grade my prompts**, read the feedback, refine, repeat. When the scorecard shows **PASSED (70+)**, this challenge is done — your best score is saved automatically and counts toward your grade when you mark the assignment complete.
