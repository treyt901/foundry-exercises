# Wrap up 🎉

You've covered the two halves of working with AI models on Azure:

### What you practiced

- **Part 1 — choosing a model.** The Foundry **model catalog** organizes models
  by publisher, task, and deployment option, and every model card tells you
  what the model is for and how it can be hosted.
- **Part 2 — instructing a model.**
  - A **system prompt** sets role, scope, tone, and rules — and needs explicit
    guardrails to survive off-topic requests (Challenge 1).
  - A **user prompt** works when it brings context, one clear task, format
    constraints, and quality cues (Challenge 2).
  - **Both together** can make a model produce machine-readable output that a
    real application could parse (Challenge 3).

- **Refinement is the real skill.** Nobody writes the perfect prompt on
  attempt one — you iterated with feedback, which is exactly how prompt
  engineering works in practice.

### Record your grade

Check that all three challenges show **PASSED** in the Prompt Lab, then click
**Mark as complete** — that submits the assignment and records your quiz and
challenge scores as your grade. (You can re-open the assignment, improve, and
mark it complete again to update your grade.)

### Troubleshooting

| Problem | Fix |
| --- | --- |
| Banner says values are missing | Open `.env` (see the setup page near the start), fill in every value, then **Restart**: {🔄 Restart}(bash lab.sh restart) |
| "Azure OpenAI request failed" | Check your endpoint URL and key, and that `AZURE_OPENAI_DEPLOYMENT` matches your deployment name exactly. |
| Preview panel is blank | Wait for **✅ Prompt Lab is running** in the terminal, then click **refresh** in the preview panel. |
| "The grader reply could not be parsed" | Occasional model hiccup — press **Run & grade** again. |
| Grade report says "no graded attempt" | Run & grade that challenge in the Prompt Lab first, then mark complete again. |

### Stop the app

All done? {🛑 Stop the Prompt Lab}(bash lab.sh stop)

Nice work — you can now both **pick the right model** and **get the most out
of it**.
