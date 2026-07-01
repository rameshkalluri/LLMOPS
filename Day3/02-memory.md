# Memory (multi-turn conversations)

## The problem: LLMs are forgetful
From Day 1: LLMs are **stateless** — each API call is independent. They only "remember"
what's **in the prompt right now**. Ask a follow-up and the model has **no idea** what
"it" refers to.

> **Analogy:** An intern with **no memory of the last sentence** unless you **re-hand them
> the notes** each time. "Book **it** for me" → "book *what*?"

---

## The fix: send the history back each turn
"Memory" in LLM apps means **including past messages** in each new request.

```
Turn 3 prompt = [system] + [turn1 user/assistant] + [turn2 user/assistant] + [turn3 user]
```

> **Analogy:** Before each question, you **replay the meeting minutes** so the intern is
> caught up — then ask the new question.

---

## Memory strategies (as chats grow long)

| Strategy | How it works | Analogy |
|---|---|---|
| **Full history** | Send every message | Re-reading the **entire transcript** (accurate, expensive) |
| **Windowed (last N)** | Keep only recent turns | Remember the **last few minutes** |
| **Summary memory** | Summarize old turns, keep the summary | Keep the **meeting minutes**, not every word |
| **Summary + window** | Summary of old + verbatim recent | Minutes **+** last few sentences (common choice) |

> Why not always full history? The **context window fills up** and **cost rises** with
> every turn. Summarize to stay small.

---

## Long-term memory (across sessions)
For remembering a user **across days**, store facts/preferences in a database or
**vector store** and retrieve them when relevant — basically **RAG over past
conversations**.

> **Analogy:** A **CRM/notebook** about the customer the intern checks before each chat
> ("prefers email, on the Pro plan").

---

## Practical tips (LLMOps)
- Cap history size (tokens) → protects cost + context window.
- Keep the **system message** pinned at the top every turn.
- Store conversation state **outside** the model (DB, cache) — the model won't hold it.
- Watch for **context bloat**: more history = slower + pricier + can dilute focus.

---

## TL;DR (in plain English)
- LLMs are **stateless**; "memory" = **re-sending past messages** in each request.
- Manage growth with **windowed** or **summary** memory (or both) to control **cost +
  context window**.
- **Long-term/cross-session** memory = store facts and **retrieve them (RAG)** when needed.
- Keep conversation state **outside** the model and cap its size.
