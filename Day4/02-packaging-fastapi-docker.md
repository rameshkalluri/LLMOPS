# Packaging: FastAPI + Docker

Before you can deploy anywhere (Cloud Run or GKE), you must turn your script into a
**web API** and pack it into a **container**.

> **Analogy:** Your notebook is a **home kitchen**. To serve customers you need a
> **service window** (the API) and to standardize it into a **food truck** (the
> container) that runs the same anywhere.

---

## Step 1 — Wrap it in an API (FastAPI)
Expose your RAG/agent as an HTTP endpoint so anything can call it.

```python
# app.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    question: str

@app.get("/health")          # health check (used by Cloud Run & Kubernetes probes)
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(q: Query):
    answer, sources = run_rag(q.question)   # your Day 2/3 logic
    return {"answer": answer, "sources": sources}
```

```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```

> **Analogy:** `/chat` is the **service window** customers order from; `/health` is the
> **"are you open?" sign** that Cloud Run/Kubernetes checks.

---

## Step 2 — Containerize it (Docker)
Package the app + dependencies into an image that runs identically everywhere (ties to
your GCP Day 8 container notes).

```dockerfile
# Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
```

```bash
docker build -t llm-app:1.0 .
docker run -p 8080:8080 -e OPENAI_API_KEY=$OPENAI_API_KEY llm-app:1.0
```

> **Analogy:** The Dockerfile is the **recipe** to build the **food truck**; the image is
> the built truck; a container is the truck **running and serving**.

---

## Step 3 — Push to a registry (Artifact Registry)
Store the image where Cloud Run/GKE can pull it.

```bash
gcloud artifacts repositories create llm --repository-format=docker --location=asia-south1
gcloud auth configure-docker asia-south1-docker.pkg.dev
docker tag llm-app:1.0 asia-south1-docker.pkg.dev/PROJECT/llm/llm-app:1.0
docker push asia-south1-docker.pkg.dev/PROJECT/llm/llm-app:1.0
```

---

## LLM-app specific tips 🔑
- **Never bake API keys into the image** — pass via env vars / secrets (Day 4.4, Day 5).
- Add a **/health** endpoint (Cloud Run + K8s probes rely on it).
- Support **streaming** responses for better UX.
- Set sensible **timeouts** (LLM calls can be slow) and **request size limits**.
- Log request id, tokens, latency (feeds Day 5 observability).

---

## TL;DR (in plain English)
- Turn your app into an **API with FastAPI** (`/chat` = service window, `/health` = open sign).
- **Containerize** with Docker (the food truck that runs anywhere), then **push to
  Artifact Registry**.
- Keep **API keys out of the image**, add **/health**, support **streaming**, set **timeouts**.
- This one container now deploys to **both Cloud Run and GKE**.
