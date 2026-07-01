# Fine-Tuning Basics

## What is fine-tuning?
**Fine-tuning** continues training a pre-trained model on **your examples** so it
permanently learns a **behavior, style, or format**.

> **Analogy:** The intern already speaks the language (pre-training). Fine-tuning is a
> **specialized course** where they practice **your specific tasks** with **hundreds of
> worked examples** until it becomes second nature — no need to re-explain every time.

---

## When to fine-tune ✅ (and not ❌)
✅ Good reasons:
- A **consistent output style/format** you can't reliably get from prompting.
- **Domain tone/jargon** (legal, medical, brand voice).
- **Shorter prompts** — bake instructions into the model → cheaper per call.
- Specialized **classification/extraction** at high accuracy.

❌ Poor reasons:
- "So it knows our documents" → use **RAG** (facts change; fine-tuning bakes them in stale).
- You only have a handful of examples → prompt/RAG instead.

---

## The dataset is everything 📋
Fine-tuning quality = **data quality**. You need many **example input→output pairs** in
the exact shape you want the model to produce.

```jsonl
{"messages": [{"role":"system","content":"You are a support agent."},
              {"role":"user","content":"My order is late."},
              {"role":"assistant","content":"I'm sorry! Here's your tracking link..."}]}
{"messages": [ ... another example ... ]}
```

> **Analogy:** A **flashcard deck** of "here's the situation → here's the ideal answer."
> Garbage cards → garbage learning. Clean, consistent cards → a reliable specialist.

- Typically **hundreds to thousands** of high-quality, **consistent** examples.
- Split into **train** and **validation** sets to check it's learning, not memorizing.

---

## Full fine-tuning vs LoRA/PEFT 🎛️
Retraining **all** billions of weights is expensive. **PEFT** (Parameter-Efficient
Fine-Tuning), especially **LoRA**, trains **small add-on adapters** instead.

> **Analogy:** Instead of **rebuilding the whole car engine**, LoRA **bolts on a small
> tuning chip**. Far cheaper/faster, and you can **swap adapters** for different tasks.

| | **Full fine-tune** | **LoRA / PEFT** |
|---|---|---|
| Cost/compute | High | **Low** |
| Speed | Slow | Fast |
| Output | New full model | Small **adapter** files |
| Analogy | Rebuild the engine | Bolt-on tuning chip |

---

## How you do it (two paths)
1. **Hosted fine-tuning APIs** (OpenAI, Vertex AI, etc.) — upload JSONL, they train &
   host it. Easiest.
2. **Open models yourself** (Llama, Mistral) — LoRA/QLoRA with libraries (PEFT,
   Axolotl); host via **vLLM/TGI on GKE GPUs** (Day 4).

---

## LLMOps for fine-tuning
- **Version** datasets + resulting models (like code).
- **Evaluate** the fine-tuned model vs the base (Day 4) — don't assume it's better.
- Watch for **overfitting** (great on train, bad on new inputs) and **catastrophic
  forgetting** (loses general skills).
- Plan **retraining** as data evolves.

---

## TL;DR (in plain English)
- **Fine-tuning = a training course** that permanently teaches the model **behavior/style**
  (not facts — that's RAG).
- Success depends on a **clean, consistent dataset** of input→output examples (hundreds+).
- **LoRA/PEFT** = cheap "bolt-on tuning chip" vs rebuilding the whole model; swappable adapters.
- Use **hosted APIs** for ease, or **LoRA on open models + vLLM/TGI on GKE** for control;
  always **version + evaluate**.
