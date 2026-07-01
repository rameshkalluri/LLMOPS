# Calling LLM APIs & Cost

## How you actually use an LLM
You send an HTTP request (or use an SDK) with your **messages + settings**; you get back
**generated text** (and usage info: token counts).

```python
# OpenAI-style example (concept — providers are similar)
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are concise. Answer in one sentence."},
        {"role": "user", "content": "What is LLMOps?"},
    ],
    temperature=0.2,
    max_tokens=100,
)
print(resp.choices[0].message.content)
print(resp.usage)   # prompt_tokens, completion_tokens, total_tokens
```

> **Analogy:** It's like **texting the intern**: you send the job + rules; they text back
> the answer, and a **meter** tells you how many "slices" (tokens) it took.

---

## Tokens = money 💸
You are billed for **input tokens + output tokens** (usually output is pricier).

```
cost ≈ (input_tokens  × input_price)  +  (output_tokens × output_price)
```

> **Analogy:** A **taxi meter**: you pay for the **distance in (your prompt)** and the
> **distance out (its answer)**. Long prompts and long answers = bigger fare.

**Ways to cut cost:**
- Use a **smaller/cheaper model** for easy tasks (route hard ones to a big model — Day 5).
- **Trim prompts**; don't stuff unnecessary context.
- **Cap `max_tokens`**; ask for concise answers.
- **Cache** repeated questions (Day 5).

---

## Counting tokens before you send
Use a tokenizer (e.g., `tiktoken`) to estimate size/cost up front.

```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
print(len(enc.encode("How many tokens is this?")))  # -> token count
```

> **Analogy:** **Weighing your parcel before posting** so you know the postage.

---

## Latency (speed) ⏱️
- **Bigger models = slower**; long outputs = slower.
- **Streaming** improves *perceived* speed (words appear as generated → low
  **time-to-first-token**).
- For chains/agents (Day 3), latency **adds up** across steps.

> **Analogy:** Streaming is like a waiter bringing dishes **as they're ready** instead of
> making you wait for the whole meal.

---

## Reliability basics (LLMOps mindset)
- APIs can **rate-limit** or fail → add **retries with backoff** and **timeouts**.
- Handle **bad/oversized outputs** gracefully (validate JSON; re-ask if invalid).
- Keep **API keys in secrets** (env vars / Secret Manager), never in code/Git.

---

## TL;DR (in plain English)
- Call the LLM with **messages + settings**; you get text + **token usage**.
- **Tokens = money** (input + output); cut cost with smaller models, shorter prompts,
  `max_tokens`, and caching.
- **Count tokens** ahead with a tokenizer; use **streaming** for snappier UX.
- Production basics: **retries, timeouts, JSON validation, secret-managed API keys**.
