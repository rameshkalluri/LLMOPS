# Self-Hosted Model Serving (vLLM, TGI, KServe)

When you don't call a hosted API but run **your own open model** (Llama, Mistral,
fine-tuned models) — usually on **GPUs in GKE**.

> **Analogy:** Instead of ordering food from a restaurant (hosted API), you **run your
> own kitchen with industrial equipment** (GPUs). More control over the menu (model),
> privacy, and cost at scale — but you staff and maintain the kitchen.

---

## Why self-host a model?
- **Data privacy / compliance** — data never leaves your infrastructure.
- **Cost at high volume** — can be cheaper than per-token API pricing.
- **Customization** — run your **fine-tuned/LoRA** models (Day 3).
- **No vendor lock-in / offline** needs.

Trade-off: **you own the GPUs, scaling, uptime, and upgrades.**

---

## The serving engines

### vLLM ⭐ (most popular)
- High-throughput inference server with **PagedAttention** and **continuous batching**
  (packs many requests together efficiently).
- OpenAI-compatible API → easy drop-in.
- *Analogy:* a **super-efficient kitchen** that cooks many orders at once without waste.

### TGI (Text Generation Inference)
- Hugging Face's production server; similar goals (batching, streaming, quantization).

### Ollama
- Dead-simple local/self-host for smaller models; great for dev, less for high-scale prod.

### KServe
- A **Kubernetes-native serving layer** (model servers as standard resources) with
  autoscaling (incl. **scale-to-zero** for models) and canary rollouts.
- *Analogy:* the **restaurant-management system** standardizing how every kitchen
  (model) is opened, scaled, and updated.

---

## Why GPUs (and why it's the hard part)
LLMs need lots of fast memory for their **weights**; GPUs provide it. Key concerns:
- **GPU memory** must fit the model (use **quantization** — 8-bit/4-bit — to shrink it).
- **Cost** — GPUs are expensive; keep utilization high, scale down when idle.
- **Cold starts are heavy** — loading a multi-GB model takes time (keep min replicas warm).

> **Analogy:** The industrial oven (GPU) is pricey and slow to heat up — don't leave many
> idling, but keep **one warm** so the first customer isn't left waiting.

---

## Typical setup on GKE
```
GPU node pool (e.g., NVIDIA L4/A100)
   └── Deployment running vLLM serving your model, requests nvidia.com/gpu: 1
         └── Service + Ingress in front
         └── HPA / KServe autoscaling on load
Your LLM app (Day 4.4) calls this internal model endpoint instead of a hosted API.
```

```bash
# Concept: run vLLM in a container serving an OpenAI-compatible endpoint
# (inside a GPU pod)
python -m vllm.entrypoints.openai.api_server \
  --model mistralai/Mistral-7B-Instruct-v0.2 --port 8000
```

Your app then points its "OpenAI base URL" at this internal service — the rest of your
RAG/agent code is unchanged.

---

## Hosted vs self-hosted (decision)
| | **Hosted API** (OpenAI/Gemini) | **Self-hosted** (vLLM/TGI on GKE) |
|---|---|---|
| Setup effort | Minimal | High (GPUs, ops) |
| Data privacy | Leaves your infra | Stays in your infra |
| Cost model | Per token | Per GPU-hour (better at scale) |
| Best model quality | Often frontier models | Open models (improving fast) |
| Analogy | Order from a restaurant | Run your own kitchen |

> **Start hosted**, move to self-hosted when **privacy, scale-cost, or customization**
> justify the operational load.

---

## TL;DR (in plain English)
- Self-hosting = **run your own model on GPUs** (usually GKE) for **privacy, scale-cost,
  and customization** — at the price of running the "kitchen."
- **vLLM** (efficient batching, OpenAI-compatible) is the popular engine; **TGI** similar;
  **KServe** standardizes serving/autoscaling on Kubernetes; **Ollama** for dev.
- GPUs are the hard/expensive part: **fit weights (quantize), keep utilization high,
  keep one warm** for cold starts.
- Point your app's model URL at the internal serving endpoint — RAG/agent code stays the same.
