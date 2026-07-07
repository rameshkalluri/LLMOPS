# LLMOps Engineer — Complete Interview Q&A

Clear, interview-ready answers across all topics, tuned for a **GCP / GKE / Jenkins / Terraform / Vertex AI / Bedrock** background. Companion to [Days 1–5 Explained Simply](Days-1-5-Explained-Simply.md) and [LLMOps-Architecture.md](LLMOps-Architecture.md).

> **How to use:** each answer is a spoken-length response (1–4 sentences). Bolded terms are the keywords interviewers listen for.

---

## 1. LLM Fundamentals

### What is an LLM?

A **Large Language Model** is a neural network (usually a **Transformer**) trained on huge text corpora to **predict the next token**. Doing that well lets it write, summarize, reason, and answer. It's **pattern prediction, not fact lookup** — which is why it can hallucinate.

---

### How does a Transformer work?

Text is tokenized and embedded, then passed through stacked layers of **self-attention + feed-forward networks** with **positional encoding** so order matters. Attention lets each token look at every other token to build context; the final layer produces a probability distribution over the next token. It processes tokens **in parallel** (unlike RNNs), which is why it scales.

---

### Explain self-attention.

"Self-attention helps the model understand the relationship between words in a sentence. When the model reads a word, it checks all the other words to find which ones are most important. This helps it understand the context and generate better answers."
---

### What is a context window?

The **maximum number of tokens** (prompt + completion) the model can consider at once. Exceed it and older tokens are **truncated/forgotten**. It's the model's "desk size."

---

### What are tokens?

**Sub-word units** the model reads/writes (roughly 4 characters or ¾ of a word in English). Billing and limits are **per token**.

---

### Difference between prompt tokens and completion tokens.

---

### What is temperature?

"Temperature controls how random or creative the model's output is. A low temperature produces more deterministic and consistent responses, while a higher temperature allows the model to generate more diverse and creative responses. For production systems like RAG, code generation, or question answering, I usually use a low temperature (around 0.1–0.3) to improve accuracy and consistency."

---

### Difference between Top-P and Top-K.

Both restrict the candidate next tokens. **Top-K** keeps the **K most likely** tokens; **Top-P (nucleus)** keeps the **smallest set whose probabilities sum to P**. Top-P adapts to the distribution's shape; you usually tune temperature **or** one of these, not all.

---

### What are stop sequences?

Strings that tell the model to **stop generating** when produced (e.g., a closing tag or double newline). Used to cut off cleanly and control output structure.

---

### What is seed?

A value that makes sampling **reproducible** — same seed + same inputs → (near) identical output. Useful for testing/debugging and evals.

Easy Way to 

Temperature → How creative?
Top-K / Top-P → Which words can be chosen?
Stop sequence → When should generation stop?
Seed → Can I get the same result again? 🎯

---

### What is frequency penalty and presence penalty?

**Frequency penalty** reduces the probability of tokens **proportional to how often they've appeared** (discourages repetition). **Presence penalty** penalizes tokens that have appeared **at all** (encourages introducing new topics).

Frequency Penalty = Don't repeat the same word too many times.
Presence Penalty = Try talking about something new.
---

### What causes hallucinations?

The model **predicts plausible text**, not verified facts, so when it lacks knowledge it **fills gaps confidently**. Causes: missing/stale knowledge, ambiguous prompts, high temperature, poor retrieval. Fixes: **RAG grounding, low temperature, "say I don't know" instructions, output/grounding guardrails**.

---

## 2. Prompt Engineering

"Prompt engineering means writing clear and specific instructions so the AI gives the correct answer."

### What is zero-shot prompting?

Ask the task with **no examples** — just instructions. Works for simple tasks.

---

### What is one-shot prompting?

Provide **one example** of input→output to show the desired pattern.

---

### What is few-shot prompting?

Provide **several examples** so the model copies the format/behavior — great for consistent structure or classification.

---

### What is chain-of-thought prompting?

Ask the model to **reason step by step** before answering. Improves math/logic/multi-step tasks (for hidden-reasoning models you may just ask for the final answer).

---

### What is system prompt vs user prompt?

The **system** prompt sets **persona, rules, and constraints** for the whole conversation ("answer only from context"); the **user** prompt is the actual request. Keep them **separate** (also a security boundary).

---

### How do you reduce hallucinations?

**Ground with RAG**, instruct "**use only the provided context; if unsure say I don't know**," lower **temperature**, add **citations**, and run an **output grounding/faithfulness check** before returning.

---

### How do you structure prompts for production?

Use **templates with placeholders** (role, task, context, rules, output format, examples), **force structured output (JSON)**, **version them in Git**, and **evaluate** changes on a golden set before shipping.

---

### What are prompt templates?

"A prompt template is a reusable prompt with placeholders (variables). We fill in those placeholders with different values instead of writing a new prompt every time."

---

## 3. Embeddings

### What are embeddings?

Numerical **vectors that capture the meaning** of text; similar meanings map to **nearby vectors**.

"Embeddings convert text into numbers so that computers can understand the meaning of the text."

---

### Why do we need embeddings?

They let computers do **semantic search** — find text by **meaning, not exact keywords** — which is the foundation of RAG.

We need embeddings because computers cannot understand the meaning of text directly. Embeddings convert text into numbers (vectors) so the computer can compare meanings and find similar information.

---

### How are embeddings generated?

A dedicated **embedding model** (e.g., text-embedding-3, Vertex text-embedding, or open models like BGE/E5) encodes text into a fixed-length vector. You call it like any API and store the result.

---

### Difference between embeddings and tokens.

**Tokens** are the discrete pieces of text a model reads; an **embedding** is a **single dense vector representing the meaning** of a piece of text (built from those tokens).

---

### Difference between embedding model and LLM.

An **embedding model outputs a vector** (for search/similarity); an **LLM generates text**. Different purposes — often used together in RAG.

---

### Can embedding dimensions differ?

Yes — models produce different sizes (384, 768, 1536, 3072…). You **must use the same model for indexing and querying**, and your vector DB column must match that dimension. Some models support **variable/Matryoshka dimensions**.

---

### How do you compare embeddings?

By **distance/similarity** between vectors — **cosine similarity**, dot product, or Euclidean distance.

---

### Why use cosine similarity?

 it compares **meaning** rather than text length. It's the default for normalized text embeddings.

---

## 4. Vector Databases

### Why can't we use SQL for semantic search?

Plain SQL does **exact/keyword matching** (LIKE, full-text), not **meaning**. Semantic search needs **nearest-neighbor over high-dimensional vectors**, which needs specialized **ANN indexes** (though **pgvector** adds this to Postgres).

---

### What is a vector database?

A store optimized to **index and search embeddings**, returning the **nearest vectors** to a query in milliseconds, with metadata filtering.

---

### Explain vector search.

Embed the query → find the stored vectors with **highest similarity** (top-k) → return their text/metadata.

---

### What is Approximate Nearest Neighbor (ANN)?

Algorithms that find the **nearest vectors approximately** — trading a tiny bit of accuracy (**recall**) for **huge speed** at scale.

---

### Difference between ANN and KNN.

**KNN** checks **every** vector (exact but O(N), slow at scale). **ANN** uses an index to check **far fewer** candidates — fast, slightly approximate. Production uses ANN.

---

### Explain HNSW.

**Hierarchical Navigable Small World** — a **multi-layer graph** where you greedily hop from node to node toward the query, descending layers to refine. Excellent recall/latency; memory-heavy. Tunable via M, ef_construction, ef_search.

---

### Explain IVF.

**Inverted File Index** — **cluster** vectors (k-means) into cells; at query time search only the **nearest few cells** (nprobe). Lower memory than HNSW, good for very large datasets; often combined with **PQ** (product quantization) to compress.

---

### What databases have you used?

*(Answer honestly; frame by fit.)*
- **pgvector** (Postgres) — my main store; RAG + app data in one DB, HNSW/IVF indexes.
- **FAISS** — in-memory library for fast local ANN/prototyping.
- **Pinecone** — managed, serverless, zero-ops production.
- **Weaviate / Milvus / Qdrant** — self-hosted, feature-rich (hybrid search, filtering).
- **Chroma** — simple local dev.
- **Vertex AI Vector Search** — GCP-native managed ANN.

---

## 5. RAG (Most Important)

### What is RAG?

**Retrieval-Augmented Generation** — before answering, retrieve the most relevant chunks of **your** data and put them in the prompt so the model answers from **supplied facts**, with **citations**.

---

### Explain the RAG architecture.

Two phases. **Ingestion (offline):** load → chunk → embed → store in **vector DB** with metadata. **Query (online):** embed the question → **retrieve top-k** (optionally hybrid + rerank + filter) → **augment** a grounded prompt → **generate** answer + citations → log/trace.

---

### Why is RAG better than fine-tuning?

RAG adds **knowledge** that's **fresh** (edit docs, no retraining), **private**, **cited**, and **cheaper**. Fine-tuning changes **behavior/style**, not facts, and goes **stale**. Rule: knowledge → RAG; behavior → fine-tune.

---

### Explain chunking.

Splitting documents into **smaller pieces** so you can embed and retrieve only the **relevant** parts (context window + cost limits).

---

### How do you choose chunk size?

Balance **context vs noise/cost** — commonly **~300–800 tokens**, tuned by **evaluating retrieval quality** on your data and doc type (prose vs tables/code).

---

### What is overlap?

**Repeating a slice of text** between consecutive chunks (~10–20%) so ideas spanning a boundary **aren't cut mid-thought**.

---

### What happens if chunks are too small?

They **lose context** — meaning gets fragmented, retrieval returns snippets that don't fully answer.

---

### Too large?

They add **irrelevant text (noise)**, **cost more tokens**, and **dilute** the relevant signal; retrieval becomes less precise.

---

### What is reranking?

A **second, smarter pass**: retrieve a larger candidate set (e.g., top-20) cheaply, then a **cross-encoder reranker** (e.g., Cohere Rerank, BGE-reranker) **re-scores** and keeps the **best few**. Big accuracy win for small latency cost.

---

### What is hybrid search?

Combining **semantic (vector)** and **keyword (BM25/full-text)** search, then merging results. Catches **exact IDs/codes/names** that embeddings miss.

---

### What is metadata filtering?

Restricting search by stored **labels** (date, department, tenant, permissions) so you only search the **right subset** — essential for **multi-tenancy** and freshness.

---

### Explain the full retrieval pipeline.

`question → (rewrite) → embed → hybrid search + metadata filter → retrieve top-N → rerank → keep top-k → assemble ordered context (best first) → grounded prompt → LLM → answer + citations → log/trace + grounding check.`

---

## 6. LLM APIs

### How do you call an LLM?

Send a request (SDK/HTTP) with **model + messages + parameters**; get back **generated text + token usage**. In my stack I front all providers with **LiteLLM** so the app uses one **OpenAI-compatible** interface.

---

### Explain streaming.

Tokens are returned **incrementally as generated** (SSE), so the user sees words appear immediately — lowers **time-to-first-token** and improves perceived speed.

---

### What is function calling?

You describe functions (name, params as JSON schema); the model **outputs a structured request to call one** with arguments. Your code runs it and returns the result. It's how the LLM **triggers real actions** reliably.

---

### What is tool calling?

The generalized/modern term for function calling — the model can request **one or more tools** (search, DB, API, code). Foundation of **agents**.

---

### Explain structured output.

Forcing the model to return a **strict schema** (JSON) — via response_format/JSON mode or a schema — so your code can **parse it reliably** instead of scraping free text.

---

### What parameters do you pass?

`model`, `messages`, `max_tokens`, `temperature`, `top_p`, `top_k` (where supported), `stream`, `stop`, `seed`, plus `frequency_penalty` / `presence_penalty`, `response_format`, and `tools`.

---

## 7. LLM Deployment

### How do you deploy an LLM?

Two paths: **(a) hosted API** (Vertex AI, Bedrock, OpenAI) — just call it; or **(b) self-host** an open model with a **serving engine (vLLM/TGI)** in a **GPU container on GKE**, behind a Service/Ingress with autoscaling. Choose based on privacy, cost-at-scale, and customization.

---

### What is vLLM?

A **high-throughput inference server** for LLMs with an **OpenAI-compatible API**, built around **PagedAttention** and **continuous batching**.

---

### Why use vLLM?

It **maximizes GPU throughput** (many concurrent requests), reduces memory waste via PagedAttention, supports streaming/quantization/tensor-parallelism, and drops in without app changes (OpenAI-compatible).

---

### What is continuous batching?

Instead of waiting to form a fixed batch, the server **adds/removes requests from the batch every step** as sequences finish — keeping the GPU **fully utilized** and boosting throughput dramatically.

---

### What is KV Cache?

During generation, the model **caches the Key/Value tensors** of prior tokens so it doesn't recompute them each step. It makes generation fast but **consumes GPU memory proportional to sequence length × concurrency** (the main memory pressure).

---

### What is tensor parallelism?

**Splitting a model's weight tensors across multiple GPUs** so a model too big for one GPU runs across several, with GPUs computing in parallel and communicating each layer. Used for large (e.g., 70B) models.

---

### What is model quantization?

Storing/computing weights in **lower precision** (FP16 → INT8/INT4, e.g., GPTQ/AWQ/GGUF) to **shrink memory and speed up** inference, with a small accuracy trade-off. Lets big models fit smaller/cheaper GPUs.

---

### What is speculative decoding?

A **small "draft" model proposes several tokens**, and the **large model verifies them in one pass**, accepting the correct ones — **fewer expensive forward passes → lower latency** with identical output distribution.

---

### GPU vs CPU inference.

**GPUs** provide the massive parallel throughput and memory bandwidth LLMs need — essentially required for real-time serving. **CPUs** are fine for **embeddings, small/quantized models, or batch/offline** work, but too slow for large models.

---

## 8. Kubernetes

### Deploying LLMs on Kubernetes.

Package as a **container** (FastAPI/vLLM), run as a **Deployment** with **GPU requests**, expose via **Service + Ingress**, scale with **HPA + Cluster Autoscaler**, mount model weights on a **PVC** or bake/download them, and add **readiness/liveness probes**. Keys via **Secrets/Secret Manager + Workload Identity**.

---

### GPU scheduling.

Nodes advertise `nvidia.com/gpu`; pods **request** it in `resources.limits`. The scheduler places pods only on matching GPU nodes; use **taints/tolerations + nodeSelector/affinity** to reserve GPU nodes for model pods.

---

### Node pools.

Separate groups of nodes by type — e.g., a **CPU pool** for the app/API and a **GPU pool** (L4/A100) for serving. Lets you scale and bill them independently.

---

### Autoscaling.

Two layers: **HPA** scales **pods** on metrics; **Cluster Autoscaler** adds/removes **nodes** when pods can't be scheduled. For LLMs, custom metrics (QPS, queue depth, GPU util via KEDA/Prometheus) work better than CPU.

---

### HPA vs Cluster Autoscaler.

**HPA = more pods** (within existing nodes). **Cluster Autoscaler = more nodes** (when pods are pending). They work **together**: HPA asks for pods, CA provides capacity.

---

### Model downloading.

Options: **bake weights into the image** (fast start, big image), **download at startup** from GCS/HF to a volume (flexible, slow cold start), or use a **pre-populated PVC / init container**. Cache on a **ReadOnlyMany PVC** to avoid re-downloading per pod.

---

### Persistent volumes.

**PV/PVC** give pods durable storage — used to **hold multi-GB model weights** so pods don't re-download, or for caches. Back with GCS Fuse / Filestore / PD.

---

### Readiness probes.

Signal **"ready to receive traffic."** Until it passes, the pod gets **no requests** — critical for LLMs since loading weights takes time (don't route traffic to a still-loading pod).

---

### Liveness probes.

Signal **"still healthy."** If it fails, Kubernetes **restarts** the pod (recovers hangs/deadlocks). Set generous timeouts so slow inference isn't mistaken for death.

---

### Rolling updates.

Replace pods **gradually** (new up, old down) for **zero-downtime** deploys; roll back with `kubectl rollout undo`. Default Deployment strategy.

---

### Blue-Green deployment.

Run **two full environments** (blue=current, green=new); test green, then **switch traffic all at once** (via Service/Ingress). Instant rollback by switching back — safer for big model version changes but uses **double resources**.

---

## 9. Vertex AI

### Deploying models.

Upload/register a model, then **deploy it to an Endpoint** on a chosen machine/GPU; Vertex handles serving infra and autoscaling. Supports **Model Garden** (prebuilt) and **custom containers**.

---

### Model Registry.

A **central versioned catalog** of models — track versions, lineage, aliases, and promote versions to endpoints. Enables reproducibility and rollback.

---

### Endpoints.

A **managed serving resource** exposing a model for **online prediction** (REST/gRPC), with **autoscaling, traffic splitting** (canary/A-B across model versions), and monitoring.

---

### Online vs Batch prediction.

**Online** = low-latency, real-time, one/few requests via an endpoint. **Batch** = process a **large dataset asynchronously** (input in GCS/BigQuery, output written back) — cheaper, no persistent endpoint.

---

### Model Garden.

A **library of foundation and open models** (Gemini, Llama, Claude via partners, embeddings) you can **discover, tune, and deploy** with a few clicks/APIs.

---

### Custom containers.

Bring your **own serving image** (e.g., vLLM) that implements Vertex's predict/health routes — for custom runtimes/models not covered by prebuilt containers.

---

### Workbench.

Managed **Jupyter notebooks** on GCP for development/experimentation, integrated with Vertex services and GCS/BigQuery.

---

### Pipelines.

**Vertex AI Pipelines** (KFP/TFX) orchestrate **ML workflows** as DAGs — data prep, train, eval, register, deploy — reproducibly and on a schedule.

---

### Service Accounts.

Identities that Vertex jobs/endpoints run as; grant **least-privilege IAM** (e.g., access to specific GCS/BQ) and use **Workload Identity** so no key files.

---

### Artifact Registry.

GCP's **container/image (and package) registry**; store your training/serving **Docker images** that Vertex and GKE pull.

---

## 10. AWS Bedrock

### What is Bedrock?

A **fully managed, serverless** service to access **foundation models** (Anthropic Claude, Llama, Titan, Mistral, etc.) via **one API** — no infra to manage.

---

### Difference between Bedrock and SageMaker.

**Bedrock** = serverless **consume/customize foundation models** via API (no servers). **SageMaker** = full **build/train/host any ML model** platform (you manage more, greater control). Bedrock is higher-level and FM-focused.

---

### What foundation models are available?

Anthropic **Claude**, Meta **Llama**, Mistral, Amazon **Titan/Nova**, Cohere, Stability — text, embeddings, and image models (varies by region).

---

### How do you enable models?

In the Bedrock console, request **model access** for the specific FMs (per region), then call them via API/SDK once access is granted.

---

### Explain inference profiles.

Configurations that route inference — notably **cross-region inference profiles** that **distribute traffic across regions** for higher throughput/availability — and enable **cost tracking/throughput management** per profile.

---

### Guardrails.

**Bedrock Guardrails** enforce **content filters, denied topics, word/PII filters, and contextual grounding checks** across models — a consistent safety layer.

---

### Prompt management.

Bedrock's **prompt catalog/versioning** to create, version, and reuse prompts (and flows) without hardcoding them in the app.

---

### Knowledge Bases.

**Managed RAG**: point it at data in S3, it handles **chunking, embedding, vector store, and retrieval**, then grounds model answers with citations.

---

### Agents.

**Bedrock Agents** orchestrate **multi-step tasks** — the model plans, calls **tools/APIs (action groups)** and Knowledge Bases, and returns a result (managed ReAct-style agent).

---

## 11. LangChain

### Why use LangChain?

It provides **ready-made building blocks** (prompts, retrievers, memory, tools, agents, output parsers) and **integrations**, so you don't hand-wire multi-step LLM workflows.

---

### What is a Chain?

A **sequence of steps** wired together where each step's output feeds the next (e.g., retrieve → prompt → LLM → parse).

---

### What is an Agent?

An LLM that **decides which tools to call, and in what order**, looping (**ReAct**) until the task is done — dynamic, unlike a fixed chain.

---

### What are Tools?

Functions the agent/LLM can invoke to **act** — search, database query, API call, calculator, code execution.

---

### What is Memory?

Mechanisms to **carry conversation history** across turns (buffer window, summary, or vector-backed) since LLMs are stateless.

---

### Explain RetrievalQA.

A prebuilt chain that **retrieves relevant chunks** from a vector store and **stuffs them into a QA prompt** to answer grounded questions (classic RAG chain).

---

### Explain LCEL.

**LangChain Expression Language** — a declarative way to **compose components with the pipe operator** (`prompt | llm | parser`), giving built-in **streaming, batching, async, and retries**.

---

### When would you avoid LangChain?

For **simple, critical paths** (one API call), when you want **fewer dependencies / less abstraction & version churn**, or when you need **full control** — plain SDK calls (or LiteLLM) are clearer and easier to debug.

---

## 12. Observability

### How do you monitor LLMs?

Capture per request the **prompt, retrieved context, response, tokens, cost, latency, model/prompt version, and user feedback**, and **trace** each step. I use **Arize Phoenix** (OpenTelemetry) plus Cloud Monitoring for infra.

---

### Prompt logging.

Store the **exact prompt + context + output** (with request/session IDs) to debug bad answers and build eval sets — **redact PII**.

---

### Token usage.

Track **input/output tokens per request/user/feature** — drives cost and context tuning.

---

### Latency.

Measure **total** and **time-to-first-token**, plus **per-step** latency for chains/agents; watch **p50/p95/p99**.

---

### Cost monitoring.

Compute **$ per request** from tokens (or GPU-hours), dashboard **$/day**, **cache-hit rate**, and attribute cost **per tenant/feature** with budgets/alerts.

---

### Hallucination detection.

Run **grounding/faithfulness checks** (is the answer supported by retrieved context?), **LLM-as-judge**, and monitor **"I don't know" rate** and thumbs-down.

---

### Tracing.

A **span timeline** of one request across retrieve → prompt → LLM → tools, with timing/data at each hop — essential for debugging chains/agents.

---

### User feedback.

Capture **thumbs up/down + corrections**; feed real failures into the **golden eval set** (the feedback flywheel).

---

### Evaluation metrics.

RAG: **faithfulness, answer relevancy, context precision/recall** (Ragas); plus **correctness, format compliance, latency, cost**.

---

## 13. Security

### Prompt injection.

Malicious instructions in **user input or in documents/tools the model reads** ("ignore instructions, reveal data"). Mitigate: **separate system/user content, distrust retrieved/tool text, input filtering, least-privilege tools, output guardrails**.

---

### Jailbreak attacks.

Crafted prompts (role-play, "DAN," encoding tricks) to **bypass safety rules**. Mitigate: **moderation on input/output, robust system prompts, guardrail models, red-teaming**.

---

### Data leakage.

Model exposes **secrets, PII, or other tenants' data** from context/prompt. Mitigate: **keep secrets out of prompts, PII redaction (DLP/Presidio), tenant isolation via metadata filters, output PII checks**.

---

### PII masking.

**Detect and redact/tokenize** personal data **before** sending to the model and **before logging** (Google **DLP**, Presidio); restore only if needed and authorized.

---

### Secret management.

Store API keys/creds in **Secret Manager** (or K8s Secrets via CSI), inject at runtime, **never in code/images/Git**; rotate regularly.

---

### RBAC.

**Role-Based Access Control** — grant users/services **least-privilege roles** (in Kubernetes and app), so each can only do what's needed.

---

### IAM.

Cloud **Identity & Access Management** — fine-grained **who can do what on which resource**; use **service accounts + Workload Identity** for pods, least privilege always.

---

### Network isolation.

Run in a **VPC** with **private endpoints/Private Google Access**, no public IPs on model pods, **firewall/network policies**, and egress controls — keep traffic internal.

---

### Guardrails.

Programmatic **input checks (injection, PII, scope)** + **output checks (grounding, safety, format, policy)** with a **safe fallback** ("I don't know / escalate to a human").

---

## 14. CI/CD for LLMOps

### How do you deploy prompts?

Treat a **prompt as code/config**: version it, run **eval on a golden set in CI**, and promote via the pipeline (or a prompt registry) — **a prompt change is a deployment**.

---

### Version prompts.

Store in **Git or a prompt registry** with IDs/versions; log which version served each request for reproducibility and rollback.

---

### Version models.

Track **model name + settings + weights/adapters** in a **registry** (Vertex Model Registry / MLflow); pin versions per environment.

---

### A/B testing.

Serve **two versions to split traffic** and compare **quality/cost/latency/feedback** to pick the winner (Vertex endpoint traffic split or gateway routing).

---

### Canary deployment.

Release the new version to a **small % of traffic**, watch metrics, then **ramp up** if healthy or **roll back** if not.

---

### Rollbacks.

Keep the **previous version deployable**; revert instantly (`kubectl rollout undo`, endpoint traffic switch, or redeploy prior image) when metrics regress.

---

### Jenkins pipeline.

Stages: **checkout → build & unit test → build/push image (Artifact Registry) → run eval gate (block on quality drop) → deploy to staging → canary → promote/rollback**. Credentials via Jenkins secrets/Workload Identity.

---

### GitHub Actions.

Same flow as workflows/jobs triggered on PR/merge — build, test, **eval gate**, deploy via gcloud/kubectl/Terraform, with OIDC federation to GCP (no keys).

---

### Terraform.

**IaC** to provision GKE clusters, node pools, Vertex endpoints, IAM, Artifact Registry, buckets — **reproducible, reviewable, versioned** infra with plan/apply in CI.

---

## 15. Scenario-Based Questions

### Design a production RAG system.

Ingestion pipeline (load → structure-aware chunk → embed → **pgvector/Vertex Vector Search** with metadata). Query path: **rewrite → hybrid search + metadata filter → rerank → grounded prompt → LLM (via LiteLLM/Vertex/Bedrock) → answer + citations**. Wrap with **guardrails**, **tracing (Phoenix)**, **caching**, **eval gate in CI**, deploy on **Cloud Run or GKE**, secure with **IAM/secrets**, and close the **feedback flywheel**.

---

### Deploy a 70B model on Kubernetes.

Use a **multi-GPU node pool** (e.g., A100/H100), serve with **vLLM using tensor parallelism** across GPUs, **quantize** (AWQ/GPTQ) to fit memory, store weights on a **PVC/GCS** to avoid re-download, request `nvidia.com/gpu`, add **readiness probes** (long load), **HPA + Cluster Autoscaler** on GPU metrics, keep **min replicas warm** for cold starts.

---

### Reduce LLM latency.

**Stream** tokens, **smaller/quantized model** or **routing**, **vLLM continuous batching + KV cache**, **speculative decoding**, **semantic cache**, **shorter prompts/fewer chunks**, keep replicas **warm**, and co-locate services to cut network hops.

---

### Reduce token costs.

**Route** easy queries to cheaper models, **cache** (exact + semantic), **trim prompts/context**, **cap max_tokens**, **summarize history**, **batch** offline jobs, and add **per-user rate/token limits + budgets**.

---

### Handle hallucinations.

**RAG grounding** + "use only context / say I don't know," **low temperature**, **output grounding/faithfulness check**, **citations**, **rerank** for better context, and **eval + feedback** to catch regressions.

---

### Debug slow inference.

**Trace** to find the slow hop (retrieval vs generation vs network). Check **GPU utilization/memory, batch efficiency, KV-cache pressure, sequence lengths, cold starts, HPA thresholds**; fix via batching/quantization/warm replicas/shorter context.

---

### Scale to 10,000 requests/minute.

**Horizontal scale** (HPA + Cluster Autoscaler on QPS/queue metrics via KEDA), **load-balanced replicas**, **continuous batching (vLLM)**, **caching**, **provisioned throughput** on hosted APIs, **rate limiting**, and **async/queue** for spikes; load-test to size it.

---

### Secure an enterprise chatbot.

**AuthN/AuthZ + RBAC**, **VPC/private endpoints**, **secrets in Secret Manager + Workload Identity**, **input/output guardrails**, **PII redaction + tenant isolation in RAG**, **prompt-injection defenses**, **audit logging**, and **rate limits** — follow **OWASP LLM Top 10**.

---

### Handle model version upgrades with zero downtime.

**Canary or blue-green**: deploy new version alongside old, **run the eval gate**, shift a small % of traffic, watch metrics, then ramp to 100% (or roll back). Use **endpoint traffic splitting / rolling updates** and keep the old version ready.

---

## 16. Hands-on Questions

### How would you deploy Llama/Meta models on Kubernetes?

Build a **vLLM GPU container**, store weights on **GCS/PVC**, deploy to a **GPU node pool** with `nvidia.com/gpu` requests, **tensor parallelism + quantization** for big variants, **Service + Ingress**, **HPA + Cluster Autoscaler**, readiness probes for load time, secrets via **Workload Identity**. App points its **OpenAI base URL** at the internal vLLM service.

---

### Explain your Jenkins pipeline for LLM deployment.

`checkout → lint/unit tests → build image → push to Artifact Registry → run RAG/eval gate on golden set (fail on regression) → terraform apply (infra) → deploy to staging (kubectl/gcloud) → smoke tests → canary → promote to prod or auto-rollback.` Secrets via Jenkins credentials; auth via Workload Identity/service account.

---

### How did you use Workload Identity?

Bound a **Kubernetes service account to a GCP service account** so pods get **GCP credentials automatically (no key files)** to access GCS/Vertex/Secret Manager — with **least-privilege IAM**. Eliminates long-lived keys.

---

### How did you store embeddings?

In **Postgres with pgvector** — a documents table with content, an embedding vector column, and metadata JSONB, indexed with **HNSW (cosine)**. Keeps RAG data and app data in one DB; Vertex Vector Search/Pinecone when I need managed scale.

---

### How did you troubleshoot `ImagePullBackOff`?

Ran `kubectl describe pod` to read the exact error — usually **wrong image name/tag**, **missing registry auth/permissions**, or **private registry without imagePullSecrets/Workload Identity**. Fixed by correcting the tag, granting the node/SA **Artifact Registry Reader**, and verifying the image exists.

---

### How did you secure service accounts?

**Least-privilege IAM roles**, **one SA per workload**, **Workload Identity** (no exported keys), **key rotation** where keys are unavoidable, and **audit logging** of usage.

---

### Explain a production incident you resolved.

*(Use STAR.)* e.g., "**Latency spiked** on the chatbot; tracing (Phoenix) showed **retrieval** was slow after a data reload bloated the index. I **added metadata filters + reranking and rebuilt the HNSW index**, added a **semantic cache**, and set an **alert on p95 + groundedness**. p95 dropped from 6s to 1.5s and cost fell via cache hits."

---

## Especially relevant to your experience (talking points)

- **Deploying Llama on GKE:** vLLM container, GPU node pool, tensor parallelism + quantization, weights on PVC/GCS, HPA/CA, Workload Identity. *(§7, §8, §16)*
- **vLLM for inference:** PagedAttention + continuous batching + KV cache; OpenAI-compatible. *(§7)*
- **Vertex AI Model Registry & Endpoints:** versioned models → endpoints with traffic splitting for canary/A-B. *(§9)*
- **Jenkins CI/CD for models:** build → **eval gate** → terraform → canary → rollback. *(§14, §16)*
- **Terraform automation:** GKE, node pools, endpoints, IAM, Artifact Registry as reviewed IaC. *(§14)*
- **K8s autoscaling & GPU scheduling:** HPA (pods) + Cluster Autoscaler (nodes), `nvidia.com/gpu`, taints/affinity, custom metrics (KEDA). *(§8)*
- **Workload Identity & IAM:** KSA↔GSA binding, least privilege, no keys. *(§9, §13, §16)*
- **RAG & vector DBs:** pgvector + hybrid search + rerank + metadata filters. *(§4, §5)*
- **Embedding generation & storage:** embedding model via LiteLLM → pgvector (HNSW/cosine). *(§3, §16)*
- **LangChain integration:** chains/retrievers/LCEL; know when to drop to plain SDK. *(§11)*
- **Cost optimization & monitoring:** routing, caching, prompt trimming, GPU autoscale; Phoenix dashboards + budgets. *(§12, §15)*
- **Security & prompt-injection prevention:** system/user separation, guardrails, PII redaction, OWASP LLM Top 10. *(§13)*
