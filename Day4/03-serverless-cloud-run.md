# Serverless Deploy: Cloud Run

## The easy path
**Cloud Run** runs your container serverless — no servers or clusters to manage, it
**auto-scales (to zero)**, and gives you an **HTTPS URL**. For most LLM apps that just
**call a hosted model API** (OpenAI/Anthropic/Gemini), this is the simplest production home.
(Ties to your GCP **Day 7** notes.)

> **Analogy:** A **fully-serviced pop-up shop**. You bring your food truck (container);
> the mall opens it when customers arrive and closes it when they leave. You **pay only
> while serving**.

---

## Deploy in one command
```bash
gcloud run deploy llm-app \
  --image=asia-south1-docker.pkg.dev/PROJECT/llm/llm-app:1.0 \
  --region=asia-south1 --allow-unauthenticated \
  --set-secrets=OPENAI_API_KEY=openai-key:latest \
  --memory=1Gi --cpu=1 --timeout=300 --concurrency=20
```

- `--set-secrets` pulls the API key from **Secret Manager** (not baked in the image).
- `--timeout=300` — LLM calls can be slow; give headroom.
- `--concurrency` — how many requests one instance handles at once.

---

## Why Cloud Run fits many LLM apps
- **Scale to zero** — no traffic, ~no cost (great for spiky/low usage).
- **Auto-scales up** on traffic spikes.
- **Managed HTTPS + custom domains**.
- **Minimal ops** — no cluster to patch.

> Reduce cold starts (Day 7 GCP notes) with `--min-instances=1` for latency-sensitive apps.

---

## Where Cloud Run falls short for LLMs ❌
- **GPUs** — limited; if you **self-host a big open model** needing GPUs, GKE is the
  typical home (Day 4.4/4.5). *(Cloud Run has some GPU support, but heavy model serving
  usually lives on GKE.)*
- **Long-lived / stateful** workloads, complex networking, sidecars, custom operators →
  Kubernetes.
- **Fine-grained control** over nodes/scheduling → GKE.

> **Rule of thumb:** App **calls a hosted LLM API** → **Cloud Run**. App **hosts its own
> GPU model** or needs full control → **GKE** (next note).

---

## Cloud Run vs GKE (quick recap)
| | **Cloud Run** | **GKE** |
|---|---|---|
| Manage | Just the container | Cluster + workloads |
| Scale to zero | ✅ | Usually no |
| GPUs / self-host models | Limited | ✅ Full |
| Ops effort | Low | Higher |
| Analogy | Serviced pop-up | Your own workshop |

---

## TL;DR (in plain English)
- **Cloud Run = serverless container hosting**: auto-scales to zero, HTTPS included,
  minimal ops — ideal when your app **calls a hosted LLM API**.
- Deploy with one `gcloud run deploy`; pull API keys from **Secret Manager**, raise the
  **timeout**, tune **concurrency**.
- Choose **GKE** instead when you need **GPUs/self-hosted models**, complex networking,
  or full control.
