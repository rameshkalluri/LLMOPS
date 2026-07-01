# Prompt Engineering (giving clear instructions)

## What is it?
**Prompt engineering** = writing your instructions so the LLM gives you what you want,
reliably. It's the **cheapest, fastest** way to improve results (try it before RAG or
fine-tuning).

> **Analogy:** Briefing a **new intern**. Vague brief → random results. Clear brief with
> an example and a required format → great, consistent work.

---

## The building blocks of a good prompt
1. **Role/persona** — "You are a senior support agent."
2. **Task** — clearly state what to do.
3. **Context** — the data/notes it should use.
4. **Rules/constraints** — "Only answer from the context. If unsure, say 'I don't know'."
5. **Output format** — "Reply as JSON with keys `answer` and `sources`."
6. **Examples** — show 1–3 samples (few-shot).

> **Analogy:** A **recipe card**: ingredients (context), steps (task), and a **photo of
> the finished dish** (example of the output you want).

---

## Core techniques

### Zero-shot
Just ask, no examples. Fine for simple tasks.

### Few-shot (show examples) 🎯
Give a few input→output examples so it copies the pattern.

> **Analogy:** Showing the intern **2–3 solved samples** before handing them the real task.

```text
Classify sentiment as POSITIVE/NEGATIVE.
Review: "I love it!"      → POSITIVE
Review: "Total waste."    → NEGATIVE
Review: "Best purchase."  →
```

### Chain-of-Thought (let it reason) 🧠
Ask it to **think step by step** for math/logic/multi-step tasks.

> **Analogy:** Telling the intern to **show their working** instead of blurting an answer.

### Structured output (JSON) 📦
Demand a strict format so your **code can parse it**.

> **Analogy:** Giving the intern a **form to fill in**, not a free-form essay — so the
> next machine can read it automatically.

```text
Return ONLY valid JSON: {"answer": "...", "confidence": 0-1, "sources": ["..."]}
```

---

## Prompt templates (reusable prompts)
In apps, you don't hardcode prompts — you use **templates** with placeholders you fill at
runtime.

```text
System: You answer only from CONTEXT. If missing, say "I don't know".
CONTEXT: {retrieved_docs}
QUESTION: {user_question}
Answer as JSON: {"answer": "...", "sources": [...]}
```

> **LLMOps tip:** **version your prompts** (store in Git) — a prompt change is a
> deployment and can change quality/cost. You'll test them with eval (Day 4).

---

## Common mistakes ❌
- Vague asks ("write something about X").
- Mixing many tasks in one prompt.
- No output format → unparseable answers.
- Forgetting the "**say I don't know**" rule → more hallucinations.

---

## TL;DR (in plain English)
- Prompt engineering = **clearly briefing the intern**; it's the cheapest quality boost.
- Include **role, task, context, rules, output format, examples**.
- Use **few-shot** (show examples), **chain-of-thought** (step-by-step), and
  **JSON output** (so code can parse it).
- Use **templates** and **version your prompts** in Git.
