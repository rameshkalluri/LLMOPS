# What is an LLM?

## The one-line idea
A **Large Language Model (LLM)** is a program that **predicts the next word** (token)
over and over, so well that it can write, answer, summarize, and reason.

> **Analogy:** It's a **super-powered autocomplete**. Your phone suggests the next word;
> an LLM does this so well — having read most of the internet — that it can write whole
> essays, code, and answers.

---

## Tokens = the LLM's "words" 🍕
LLMs don't read letters or whole words — they read **tokens** (word-pieces). Roughly
**1 token ≈ 4 characters ≈ ¾ of a word** in English.

> **Analogy:** A token is a **slice of pizza**. A sentence is cut into slices; the model
> eats and produces text **slice by slice**. You are **billed per slice** (see cost note).

- "Hello world" ≈ 2 tokens; a paragraph ≈ 100 tokens; this page ≈ a few hundred.
- **Both your input and the model's output cost tokens.**

---

## Context window = the LLM's desk 🪟
The **context window** is how many tokens the model can "see at once" — your prompt +
its answer must fit inside it.

> **Analogy:** A **desk of a fixed size**. You can only spread out so many papers
> (tokens) at once. Bring too many and the **oldest ones fall off the edge** — the
> model "forgets" them.

- Small window = a small desk (fits a chat); large window = a huge table (fits a book).
- Key insight: **LLMs are stateless** — they don't remember past chats unless you
  **put that history back on the desk** every time (this is why we add memory on Day 3).

---

## How it "thinks" (very simply)
1. Your text → split into **tokens**.
2. Model predicts the **most likely next token**, adds it, repeats.
3. Stops when it predicts an "end" token or hits the limit.

It's **pattern prediction**, not database lookup — which is why it can be fluent but
**wrong**.

---

## Hallucination = confident guessing 😅
A **hallucination** is when the model states something **false but confident**, because
it's predicting plausible text, not checking facts.

> **Analogy:** A student who **didn't study** but **answers every exam question
> confidently** — sometimes right, sometimes made up, always sure of themselves.

**How we fix it (preview):**
- **RAG (Day 2)** — give it the real documents to read first.
- **Prompting (today)** — tell it "say 'I don't know' if unsure."
- **Guardrails/eval (Day 5, Day 4)** — check outputs.

---

## Base vs Instruct/Chat models
- **Base model** — raw autocomplete (just continues text).
- **Instruct / Chat model** — fine-tuned to **follow instructions** and chat (what you
  usually use, e.g., GPT-4o, Claude, Gemini).

---

## TL;DR (in plain English)
- An LLM = **super-autocomplete** that predicts text **token by token**.
- **Token** = a word-piece (a pizza slice); **you pay per token**, in and out.
- **Context window** = the model's **desk**; it only sees what fits, and **forgets the rest**.
- LLMs **predict**, they don't look up facts → they **hallucinate**; RAG + prompting + eval fix this.
- Use **instruct/chat** models for apps.
