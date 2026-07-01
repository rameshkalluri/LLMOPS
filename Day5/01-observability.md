# Observability

## Why LLM apps need special observability
Normal apps log requests and errors. LLM apps also need to see the **prompt, the
response, the retrieved context, tokens, and cost** — because quality problems hide in
**what the model actually saw and said**.

> **Analogy:** Regular monitoring watches whether the **shop is open and the till works**.
> LLM observability is like **CCTV over the intern's desk** — you can replay exactly what
> question came in, what notes they used, and what they answered, to understand **why** a
> bad answer happened.

---

## What to capture (per request)
- **Inputs**: user question, system prompt, **retrieved chunks** (for RAG).
- **Output**: the model's answer (and any tool calls).
- **Tokens & cost**: input/output tokens, $ per request.
- **Latency**: total + time-to-first-token; per-step for chains/agents.
- **Metadata**: model + version, prompt version, user/session id, request id.
- **Feedback**: thumbs up/down, corrections.

---

## Tracing (follow one request through every step) 🔍
A **trace** shows the full journey: retrieve → prompt → LLM → tool → parse, with timing
and data at each hop. Essential for **chains and agents** (Day 3).

> **Analogy:** A **package-tracking timeline** showing every stop and how long each took —
> so you find **where** it went wrong or slow.

- Tools: **Langfuse**, **LangSmith**, **Arize Phoenix** (LLM-specific), plus **Cloud
  Monitoring/Logging** and Prometheus/Grafana for infra metrics.

---

## Metrics dashboards 📊
Track over time:
- **Quality:** eval scores, groundedness, thumbs-up rate, "I don't know" rate.
- **Cost:** tokens/request, $/day, cache-hit rate.
- **Latency:** p50/p95 response time, time-to-first-token.
- **Reliability:** error rate, timeout rate, guardrail trigger rate.

> **The LLMOps golden signals:** **Quality, Cost, Latency, Reliability** (+ user feedback).

---

## The feedback flywheel 🔁
Capture user feedback and real failures → add them to your **golden eval set** (Day 4) →
improve prompts/RAG/fine-tuning → measure again.

> **Analogy:** Every customer complaint becomes a **new flashcard** for the intern's next
> training review. Production makes the product smarter over time.

---

## Practical tips
- Add a **request id** end-to-end for correlation.
- **Redact PII** in logs (privacy — Day 5.3).
- Sample heavy traffic if full tracing is costly.
- Alert on **symptoms users feel** (latency, errors, low groundedness), not noise.

---

## TL;DR (in plain English)
- LLM observability = **CCTV over the intern's desk**: capture prompt, context, response,
  tokens, cost, latency, and feedback.
- Use **tracing** to follow a request through every step (vital for chains/agents).
- Dashboard the **golden signals**: quality, cost, latency, reliability.
- Feed real failures/feedback back into your **eval set** — the feedback flywheel.
