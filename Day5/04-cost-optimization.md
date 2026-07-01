# Cost Optimization

LLM apps can get expensive fast (you pay per token, per call, per GPU-hour). Here's how to
keep the bill sane **without wrecking quality**.

> **Analogy:** Every question to the intern costs money (per word). Don't send the
> **top expert** for a **yes/no question**, don't re-ask what you already answered, and
> don't hand over the **entire filing cabinet** when one page will do.

---

## 1. Right-size the model 🎯
Use the **cheapest model that passes eval** for each task; reserve big models for hard tasks.

- **Model routing / cascade:** try a small/cheap model first; **escalate** to a bigger one
  only if needed (low confidence, complex query).
- *Analogy:* the **junior handles easy tickets**; escalate to the **senior** only when stuck.

---

## 2. Caching 💾
Don't pay twice for the same work.
- **Exact cache** — identical request → return the stored answer.
- **Semantic cache** — *similar* question (by embedding) → reuse the answer.
- **Prompt/prefix caching** — some providers cache repeated prompt prefixes cheaply.

> **Analogy:** Keep an **FAQ sheet**: if someone asks a question you've answered (or a
> close paraphrase), read from the sheet instead of paying the intern again.

- Watch: cache **freshness** (invalidate when docs change) and **personalization** (don't
  serve one user's private answer to another).

---

## 3. Shrink the prompt ✂️
Tokens = money, both directions.
- Retrieve **fewer/tighter chunks** (good chunking + re-ranking — Day 2).
- Trim boilerplate; **summarize** long chat history (Day 3 memory).
- Cap **`max_tokens`**; ask for concise output.

> **Analogy:** Hand over the **relevant page**, not the whole binder — and ask for a
> **short answer**, not an essay.

---

## 4. Batching & concurrency
- **Batch** offline/bulk jobs; self-hosted **vLLM** batches many requests efficiently (Day 4.5).
- Tune server **concurrency** so instances are well-utilized (fewer idle machines).

---

## 5. Control self-hosting (GPU) costs
- **Autoscale** GPU pods; **scale down / delete idle GPU pools** (they're pricey — GCP Day 8).
- **Quantize** models (4/8-bit) to fit smaller/cheaper GPUs.
- Keep **one warm** replica for latency, not ten idle ones.

---

## 6. Governance & visibility
- **Rate limits + token caps per user** (also a DoS defense — Day 5.3).
- **Budgets + alerts** (GCP Day 1 mindset) and per-feature cost dashboards (Day 5.1).
- Attribute cost by **user/tenant/feature** to find the expensive ones.

---

## Cost cheat-sheet

| Lever | Saves by | Analogy |
|---|---|---|
| Smaller model / routing | Cheaper per call | Junior vs senior |
| Caching (exact/semantic) | Avoids repeat calls | FAQ sheet |
| Shorter prompts/outputs | Fewer tokens | One page, short answer |
| Batching | Better utilization | Cook many orders at once |
| GPU autoscale/quantize | Less idle/big hardware | Right-size the kitchen |
| Rate/token limits | Caps runaway use | Portion control |

---

## TL;DR (in plain English)
- **Right-size the model** and **route** easy tasks to cheap models, hard ones to big models.
- **Cache** (exact + semantic) so you don't pay twice; watch freshness & privacy.
- **Shrink prompts/outputs** (fewer chunks, summarize history, cap max_tokens).
- For self-hosting, **autoscale/quantize GPUs and kill idle pools**; add **rate/token
  limits, budgets, and per-tenant cost visibility.**
