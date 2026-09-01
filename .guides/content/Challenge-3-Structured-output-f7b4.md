# Challenge 3 — Structured output

**Skill: a system prompt that does ALL the work.** Real applications rarely
show a model's raw chat reply to anyone — they need output a *program* can
read. That usually means JSON, and in a real app the *system prompt* enforces
it: the user's message just triggers the job and hands over the data, while
the system prompt carries the role, the schema, and the hard rules
(*"You are a data-extraction assistant. Output ONLY a raw JSON object…"*).

### Your job

The panel beside this page shows **Challenge 3**. A short user prompt is
**already filled in for you** — you can tweak it, but it shouldn't need to
carry any rules. Your work is the **system prompt**. Bluff City Bikes wants
incoming customer emails turned into records with exactly these keys:

```json
{
  "customer_name": "…",
  "product": "…",
  "issue": "…",
  "sentiment": "positive | neutral | negative",
  "urgency": "low | medium | high"
}
```

The customer message shown in the brief is appended to the user prompt
automatically — your system prompt has to work for *any* message that could
arrive there, not just this one.

### What usually goes wrong (and how to prompt against it)

| Symptom | The fix, in your system prompt |
| --- | --- |
| Reply starts with "Sure! Here's the JSON…" | "Output ONLY the JSON object — no explanations, no greetings." |
| JSON wrapped in ``` fences | "Do not use markdown code fences." |
| Made-up values for missing info | "If a field cannot be determined, use null." |
| Wrong or extra keys | List the exact keys and allowed values, and say "no other keys". |

Watch the **automatic format check** under your results — it tells you
objectively whether your JSON parsed, and which keys were missing or extra.

### Pass it

When the scorecard shows **PASSED (70+)**, you're done — your best score is
saved automatically.
