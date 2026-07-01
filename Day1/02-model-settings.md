# Model Settings (the knobs)

When you call an LLM, a few **settings** control how it behaves. Learning these is like
learning the **knobs on a stove** — small turns change the result a lot.

---

## Temperature = how creative/random 🎲
Controls randomness. **Low = focused & repeatable; high = creative & varied.**

> **Analogy:** A **spice dial**. Low temperature = plain, predictable dish (same every
> time). High temperature = experimental, surprising flavors (different each time).

| Temperature | Behavior | Use for |
|---|---|---|
| **0 – 0.3** | Deterministic, factual | Extraction, classification, code, RAG answers |
| **0.4 – 0.7** | Balanced | General chat, summaries |
| **0.8 – 1.2** | Creative, varied | Brainstorming, marketing, stories |

> Rule: for **LLMOps/production accuracy**, keep temperature **low** (0–0.3).

---

## Top-p (nucleus sampling) = vocabulary width
Instead of considering all possible next words, the model considers only the **top
slice** whose probabilities add up to `p`.

> **Analogy:** Ordering from a menu. **top-p = 0.9** means "only consider the dishes
> that make up the **top 90%** of what's popular" — ignore the weird 10% tail.

- Usually tune **either** temperature **or** top-p, not both. Low top-p = safer.

---

## Max tokens = answer length cap ✂️
Limits how long the **output** can be.

> **Analogy:** Telling the intern "**answer in at most one page.**" Protects you from
> huge, expensive replies.

- Remember: output tokens **cost money** and count against the context window.

---

## Messages & Roles (system / user / assistant) 🎭
Chat models take a list of messages with roles:
- **system** — the **standing instructions / persona** ("You are a helpful support
  agent. Only answer from the provided docs.").
- **user** — what the person says.
- **assistant** — the model's previous replies (for multi-turn context).

> **Analogy:** The **system message** is the intern's **job description taped to their
> desk** — it sets the rules for the whole conversation. The **user** messages are the
> tasks handed to them.

---

## Other common settings
- **stop sequences** — text that tells the model to stop.
- **frequency/presence penalty** — discourage repetition / encourage new topics.
- **seed** — (where supported) make outputs more reproducible.
- **streaming** — get tokens as they're generated (better UX, lower time-to-first-token).

---

## TL;DR (in plain English)
- **Temperature = creativity dial** (low = factual/repeatable; high = creative). Keep it
  **low** for production accuracy.
- **Top-p** = how much of the "vocabulary tail" to allow; tune it **or** temperature.
- **Max tokens** = a length cap (saves money; watch the context window).
- **System message** = the intern's **job description**; use it to set rules & persona.
- Use **streaming** for snappier UX.
