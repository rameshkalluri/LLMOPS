# Guardrails & Safety

## What are guardrails?
**Guardrails** are checks around the model that keep inputs and outputs **safe, on-topic,
and correct** — before and after the LLM runs.

> **Analogy:** The intern is capable but naive. Guardrails are the **office rules + a
> supervisor**: screen weird requests at the door (input), and **check the answer before
> it's sent to the customer** (output).

---

## Input guardrails (before the LLM) 🚪
Run checks on the **user's message** first:
- **Moderation** — block hate/violence/self-harm/etc. (provider moderation APIs).
- **Prompt-injection detection** — catch "ignore your instructions…" attempts (Day 5.3).
- **PII detection** — spot/redact personal data before it's sent or logged.
- **Topic/scope check** — is this even something our bot should answer?

> **Analogy:** The **bouncer** at the door — screen out trouble before it reaches the intern.

---

## Output guardrails (after the LLM) ✅
Check the **model's answer** before returning it:
- **Grounding/faithfulness check** — is the answer supported by retrieved context?
  If not → don't send it (or say "I don't know").
- **Format validation** — is the JSON valid? Re-ask if not.
- **Safety/toxicity + PII** — moderate the output; redact leaked personal data.
- **Policy checks** — no financial/medical/legal advice if disallowed, etc.

> **Analogy:** The **supervisor proofreads** the intern's reply — checks it's on the
> provided facts, safe, and in the right format — **before it goes out**.

---

## Grounding check (RAG's key guardrail)
For RAG, verify each claim traces back to the retrieved chunks. Low support → suppress or
flag the answer.

> **Analogy:** "Show me **which page** says that." No page? Then don't state it as fact.

---

## Fallback behavior (fail safe) 🛟
When a guardrail trips or confidence is low:
- Say **"I don't know / let me connect you to a human."**
- Ask a **clarifying question**.
- Return a **safe canned response** — never a risky guess.

> **Analogy:** A well-trained intern who says **"let me check with my manager"** instead
> of confidently making something up.

---

## Tools
- Provider **moderation APIs** (OpenAI/Google) for toxicity/safety.
- **NeMo Guardrails**, **Guardrails AI** for structured rule enforcement.
- **PII**: Google DLP, Presidio.
- Your own **LLM-as-a-judge** checks (Day 4) as a guardrail.

---

## LLMOps tips
- Log **every guardrail trigger** (Day 5.1) — it's a quality/security signal.
- Guardrails add **latency/cost** — keep them lightweight; run cheap checks first.
- Test guardrails with **red-team prompts** in your eval set.

---

## TL;DR (in plain English)
- Guardrails = **bouncer at the door (input)** + **supervisor proofreading (output)**.
- **Input:** moderation, prompt-injection detection, PII, scope checks.
- **Output:** grounding/faithfulness, format validation, safety/PII, policy checks.
- On failure, **fail safe** ("I don't know" / hand to a human), and **log every trigger**.
