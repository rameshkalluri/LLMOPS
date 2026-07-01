# Day 4 — Evaluation, Deployment & Serving on GKE / Kubernetes

Notes for Day 4 of the [LLMOps 5-Day Learning Plan](../LLMOps-5-Day-Learning-Plan.md).

> **Big-picture analogy:** The intern does great work in the practice room. Today we (1)
> give them a **performance review** (evaluation), (2) put them in a **real office with a
> phone line** (API + container), and (3) decide **which building** they work in — a
> **serviced pop-up (Cloud Run)** or **your own workshop with heavy machinery (GKE /
> Kubernetes)** where companies run bigger, GPU-powered LLM systems.

## Topics
1. [Evaluation](01-evaluation.md) — how to measure LLM/RAG quality (Ragas, LLM-as-judge).
2. [Packaging: FastAPI + Docker](02-packaging-fastapi-docker.md) — turn the app into an API in a container.
3. [Serverless Deploy: Cloud Run](03-serverless-cloud-run.md) — the easy path.
4. [Deploying on GKE / Kubernetes](04-deploying-on-gke-kubernetes.md) — **how companies deploy LLM apps** (manifests, HPA, GPUs).
5. [Self-Hosted Model Serving](05-model-serving-vllm-kserve.md) — vLLM, TGI, KServe on GPU nodes.

## Day 4 Goals
- [ ] Measure quality with an eval set + metrics (faithfulness, relevancy).
- [ ] Wrap the app in FastAPI and containerize it with Docker.
- [ ] Deploy to Cloud Run (serverless).
- [ ] Deploy the same container to **GKE** with Deployment + Service + Ingress + HPA.
- [ ] Understand how to self-host open models on GPUs (vLLM/TGI/KServe).
