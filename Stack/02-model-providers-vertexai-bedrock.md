# Vertex AI & Bedrock — the Model Providers

These are the **kitchens that actually cook the dish** — the services that run the LLM
and do the **inference** (Day 4 term: turning your prompt into an answer). LiteLLM (the
waiter) routes orders to them.

> **Analogy:** You have **two kitchens** — Google's (**Vertex AI**) and Amazon's
> (**Bedrock**). Both can cook; each has its own **specialty dishes** (models). The waiter
> (LiteLLM) decides which kitchen handles each order, and can **send it to the other if
> one is busy** (fallback).

**Where they fit:** Day 1 (the model you call), Day 4 (inference/serving). They're the
**backends behind LiteLLM**.

---

## Vertex AI (Google Cloud)
Google's managed AI platform. For LLMs you mainly use it for **Gemini** models (and other
hosted/garden models), plus embeddings and, if needed, fine-tuning and vector search.

- **Models:** Gemini family (e.g., `gemini-1.5-pro`, `gemini-1.5-flash`), embeddings.
- **Auth:** Google Cloud service account / ADC (ties to your GCP IAM notes).
- **Ties to your GCP notes:** Vertex AI is the ML platform from GCP Day 9.
- **Via LiteLLM:** `model="vertex_ai/gemini-1.5-pro"`.

> **Analogy:** The **Google kitchen** — great all-rounder, deep GCP integration (IAM,
> logging, Vector Search).

---

## Bedrock (AWS)
Amazon's managed service offering models from **multiple vendors** through one API.

- **Models:** Anthropic **Claude**, Meta **Llama**, Mistral, Amazon **Titan/Nova**, Cohere.
- **Auth:** AWS IAM credentials / roles.
- **Via LiteLLM:** `model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0"`.

> **Analogy:** The **Amazon kitchen** — a food court of chefs (many model vendors) behind
> one counter.

---

## Why use BOTH? (this is the point of your stack)

| Reason | How having two providers helps |
|---|---|
| **Resilience / uptime** | One is down or rate-limited → **fall back** to the other |
| **Best model per task** | Route to Gemini or Claude depending on strengths/cost |
| **Cost optimization** | Send cheap tasks to a cheaper model/provider (Day 5.4) |
| **No vendor lock-in** | Not trapped in one cloud's pricing/roadmap |
| **Compliance / region** | Use whichever meets data-residency needs |

> LiteLLM makes this practical: your app calls an **alias** (`smart-model`), and routing
> rules decide **Vertex AI vs Bedrock** underneath.

---

## Hosted providers vs self-hosting (recap Day 4.5)
Both Vertex AI and Bedrock are **hosted** — *they* run the GPUs and inference; you just
call an API. (Self-hosting with vLLM/TGI on GKE is the alternative when you need full
control/privacy — see Day 4.5.) Your stack is **hosted-API**, which is simpler to operate.

---

## Practical tips
- Keep **model choices behind LiteLLM aliases** — never hardcode `vertex_ai/...` or
  `bedrock/...` in app logic.
- Store **GCP and AWS credentials as secrets** (Secret Manager / env), not in code.
- Track **per-provider cost + latency** in Arize Phoenix to inform routing.
- Define **fallback order** (e.g., primary Gemini, fallback Claude) and test it.
- Mind **region + data residency** for each provider.

---

## TL;DR (in plain English)
- **Vertex AI (Google)** and **Bedrock (AWS)** are the **kitchens** that run the model and
  do the **inference**; LiteLLM routes to them.
- **Vertex AI** = Gemini + deep GCP integration; **Bedrock** = one API to Claude/Llama/
  Titan/etc.
- Using **both** gives **resilience, best-model-per-task, cost routing, and no lock-in** —
  orchestrated by LiteLLM aliases + fallbacks.
- They're **hosted** providers (they own the GPUs); keep creds in secrets and track
  cost/latency per provider.
