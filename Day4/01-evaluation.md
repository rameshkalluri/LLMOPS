# Evaluation (the heart of LLMOps)

## Why eval matters most
LLM outputs are **non-deterministic** and there's no single "correct" string. Without
measurement, you're **flying blind** — you can't tell if a prompt change, new model, or
RAG tweak made things **better or worse**.

> **Analogy:** Evaluation is the intern's **performance review**. Without it, you *feel*
> they're doing fine but have **no proof** — and you can't tell if last week's change
> helped or hurt.

---

## Offline vs Online eval
- **Offline** — test against a **fixed "golden" dataset** before shipping (like unit tests).
- **Online** — measure **real production** traffic (user feedback, thumbs up/down, success
  rates) after shipping.

> **Analogy:** Offline = a **mock exam** before the real thing; online = **on-the-job
> reviews** from real customers.

---

## The golden dataset 🏅
A curated set of **questions + ideal answers** (and, for RAG, the expected source docs).
Run it whenever you change anything.

> **Analogy:** A **standard exam paper with an answer key** you re-give after every change
> to catch **regressions**.

- Start small (20–50 realistic cases), grow it over time from real user questions/failures.

---

## What to measure

### RAG quality metrics (e.g., Ragas)
- **Faithfulness / groundedness** — is the answer supported by the retrieved context?
  (Catches hallucination.)
- **Answer relevancy** — does it actually address the question?
- **Context precision/recall** — did retrieval fetch the right chunks?

> **Analogy:** Did the intern **stick to the provided pages** (faithfulness), **answer
> the actual question** (relevancy), and did the librarian **fetch the right pages**
> (context metrics)?

### General quality
- **Correctness** vs the reference answer, **format** compliance, **tone/safety**.

---

## LLM-as-a-judge ⚖️
Use a **strong LLM to grade** your app's outputs against criteria/reference answers, at
scale. Cheaper/faster than human review for most checks.

> **Analogy:** A **senior examiner** grades hundreds of papers using a rubric — far
> faster than doing it all by hand.

- Keep **some human review** for calibration; judges can be biased/inconsistent.

---

## Practical eval flow
```
Golden set → run app on each question → score with metrics (Ragas / LLM-judge)
          → compare vs previous version → ship only if scores hold/improve
```

```python
# Concept: Ragas
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
result = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision])
print(result)
```

---

## LLMOps mindset
- **Version** prompts, models, and eval sets together.
- Make eval a **CI gate** (Day 5): block deploys that drop scores.
- Track **cost + latency** alongside quality (a "better" answer that's 5× pricier may lose).

---

## TL;DR (in plain English)
- Eval = the intern's **performance review**; without it you can't tell if changes help.
- Use a **golden dataset** (offline) + **real feedback** (online) to catch regressions.
- For RAG, measure **faithfulness, answer relevancy, context precision/recall** (e.g., Ragas).
- **LLM-as-a-judge** grades at scale; version everything and make eval a **deploy gate**.
