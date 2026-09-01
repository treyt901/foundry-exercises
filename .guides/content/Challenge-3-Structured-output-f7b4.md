# Challenge 3 — Structured output

**Skill: system + user prompts working together.** Real applications rarely
show a model's raw chat reply to anyone — they need output a *program* can
read. That usually means JSON, and it takes both prompts pulling in the same
direction:

- The **system prompt** defines the job and the hard rules
  (*"You are a data-extraction assistant. Output ONLY a raw JSON object…"*).
- The **user prompt** states the task and hands over the data to process.

### Your job

Open the **Challenge 3** tab. Bluff City Bikes wants incoming customer emails
turned into records with exactly these keys:

```json
{
  "customer_name": "…",
  "product": "…",
  "issue": "…",
  "sentiment": "positive | neutral | negative",
  "urgency": "low | medium | high"
}
```

Write both prompts. The customer message shown in the brief is appended to
your user prompt automatically.

### What usually goes wrong (and how to prompt against it)

| Symptom | The fix, in your prompt |
| --- | --- |
| Reply starts with "Sure! Here's the JSON…" | "Output ONLY the JSON object — no explanations, no greetings." |
| JSON wrapped in ``` fences | "Do not use markdown code fences." |
| Made-up values for missing info | "If a field cannot be determined, use null." |
| Wrong or extra keys | List the exact keys and allowed values, and say "no other keys". |

Watch the **automatic format check** under your results — it tells you
objectively whether your JSON parsed, and which keys were missing or extra.

### Pass it

When your best score is **70+**:

{Check It!|assessment}(test-1098273465)
