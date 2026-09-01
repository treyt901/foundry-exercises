# Challenge 3 — Structured output

**Skill: a system prompt that does ALL the work.** Real applications rarely show a model's raw chat reply to anyone — they need output a *program* can read. That usually means JSON, and in a real app the *system prompt* enforces it: the user's message just triggers the job and hands over the data, while the system prompt carries the role, the schema, and the hard rules (*"You are a data-extraction assistant. Output ONLY a raw JSON object…"*).

### Your job

The panel beside this page shows **Challenge 3**. A short user prompt is **already filled in for you** — you can tweak it, but it shouldn't need to carry any rules. Your work is the **system prompt**. Bluff City Bikes wants incoming customer emails turned into records with exactly these keys:

```json
{
  "customer_name": "…",
  "product": "…",
  "issue": "…",
  "sentiment": "positive | neutral | negative",
  "urgency": "low | medium | high"
}
```

Your prompts are tested against **three** customer messages (shown in the brief): a straightforward one, one with **missing details** — every key must still appear, using `null` — and one **full of numbers** trying to bait the wrong data types into your fields. Your system prompt has to hold up on all three.

### What usually goes wrong (and how to prompt against it)

| Symptom | The fix, in your system prompt |
| --- | --- |
| Reply starts with "Sure! Here's the JSON…" | "Output ONLY the JSON object — no explanations, no greetings." |
| JSON wrapped in ``` fences | "Do not use markdown code fences." |
| Made-up values for missing info | "If a field cannot be determined, use null." |
| Wrong or extra keys | List the exact keys and allowed values, and say "no other keys". |
| Blank values (`""`) | "Never leave a value empty — extract the information or use null." |
| Wrong type or category (`"urgency": 2`, `"urgency": "ASAP"`) | "Every value must be text; sentiment and urgency must be exactly one of the allowed words." |

Watch the **automatic format check** under your results — one line per test message, telling you objectively whether the JSON parsed, whether every key was present, and whether any value was blank, the wrong type, or outside the allowed list.

### Pass it

When the scorecard shows **PASSED (70+)**, you're done — your best score is saved automatically.
