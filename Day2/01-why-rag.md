# Why RAG?

## The problem RAG solves
An LLM only knows:
1. What it learned during training (a **frozen snapshot**, now outdated), and
2. What's in the **prompt right now**.

It does **not** know your **private company data**, and it **makes things up** when
unsure.

> **Analogy:** A smart intern who **graduated last year** (stale knowledge), has **never
> seen your company's files** (no private data), and **won't admit when they don't know**
> (hallucination). Not safe to answer customers alone!

---

## What RAG does
**RAG = Retrieval-Augmented Generation.** Before answering, the system **retrieves** the
most relevant pieces of *your* documents and **puts them in the prompt** so the model
answers from **facts you supplied**.

> **Analogy:** An **open-book exam**. Instead of answering from memory, the intern is
> handed the **exact relevant pages** and told: "answer using **only** these, and cite them."

```
Question ─► find relevant docs ─► stuff them into the prompt ─► LLM answers from them
```

---

## Why companies love RAG
- **Uses private/internal data** without retraining the model.
- **Always fresh** — update the documents, not the model.
- **Fewer hallucinations** — answers are grounded in real text.
- **Citations** — you can show *where* the answer came from (trust + audits).
- **Cheaper & faster than fine-tuning** for knowledge.

---

## RAG vs Fine-tuning (knowledge vs behavior)
| | **RAG** | **Fine-tuning** |
|---|---|---|
| Adds | **Knowledge / facts** | **Style / format / behavior** |
| Update cost | Edit documents (easy) | Retrain (harder) |
| Freshness | Instant | Stale until retrained |
| Analogy | **Open-book exam** | **Sending the intern to a course** |

> Rule of thumb: need the model to **know something** → **RAG**. Need it to **behave/sound
> a certain way** → fine-tune (Day 3).

---

## When RAG is the right tool ✅
- Q&A over docs, policies, manuals, tickets, wikis.
- Customer support bots grounded in your knowledge base.
- Anything needing **current** or **private** facts + **citations**.

## When RAG is NOT enough ❌
- Pure style/formatting behavior → fine-tuning.
- Real-time actions (book a ticket) → **tools/agents** (Day 3).
- Giant analytics questions → a database/BigQuery, not RAG.

---

## TL;DR (in plain English)
- LLMs have **stale + no private knowledge** and **hallucinate**.
- **RAG = open-book exam**: retrieve your relevant docs → put them in the prompt → answer
  from facts, with **citations**.
- It's **fresh, private-data-friendly, cheaper than fine-tuning**, and reduces made-up answers.
- Use RAG for **knowledge**; use fine-tuning for **behavior/style**.
