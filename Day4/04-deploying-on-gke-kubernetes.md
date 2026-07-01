# Deploying LLM Apps on GKE / Kubernetes (how companies do it)

This is the **real-world production pattern** many companies use to run LLM apps. It
builds on your GCP **Day 8 (GKE)** notes, applied to an LLM service.

> **Big-picture analogy:** Cloud Run is renting a **serviced pop-up**. **Kubernetes is
> running your own workshop**: you decide how many workers (pods), how customers get in
> (Service/Ingress), how to add staff at rush hour (HPA), and you can install **heavy
> machinery (GPUs)** for self-hosted models. More control and power — more responsibility.

---

## Why companies choose GKE for LLM apps
- **GPUs** for self-hosted open models (Llama, Mistral) via vLLM/TGI (Day 4.5).
- **Full control**: networking, sidecars, service mesh, custom autoscaling, multi-service platforms.
- **One platform** for many microservices (retriever, API, workers, vector DB).
- **Data residency / compliance** — keep everything in your own cluster/VPC.
- Reuse existing **Kubernetes tooling, CI/CD, and on-call** practices.

---

## The mental model (recap from GCP Day 8)
```
Cluster
 ├── Control plane (Google-managed brain)
 └── Nodes (VMs; can be CPU or GPU pools)
        └── Pods (your running containers: the LLM API)
Service   → stable internal address + load balancing across pods
Ingress   → public HTTPS entry, routes to Services
HPA       → adds/removes pods based on load
ConfigMap → non-secret config     Secret → API keys
```

> **Analogy:** **Pods** = workers; **Deployment** = the manager keeping N workers alive
> and upgrading them safely; **Service** = the front-desk phone number; **Ingress** = the
> building's main entrance; **HPA** = auto-hiring at rush hour.

---

## Step 0 — Create a cluster & connect
```bash
# Autopilot (Google manages nodes) — simplest for CPU LLM API apps
gcloud container clusters create-auto llm-cluster --region=asia-south1
gcloud container clusters get-credentials llm-cluster --region=asia-south1
```

---

## Step 1 — Store secrets (API keys) 🔑
Never bake keys into images. Create a Kubernetes Secret (or use **Secret Manager +
Workload Identity** — see security note below).
```bash
kubectl create secret generic llm-secrets \
  --from-literal=OPENAI_API_KEY=sk-...redacted...
```

---

## Step 2 — Deployment (the pods running your API)
`deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-app
spec:
  replicas: 3                      # 3 copies for availability + throughput
  selector:
    matchLabels: { app: llm-app }
  template:
    metadata:
      labels: { app: llm-app }
    spec:
      containers:
        - name: llm-app
          image: asia-south1-docker.pkg.dev/PROJECT/llm/llm-app:1.0
          ports:
            - containerPort: 8080
          env:
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef: { name: llm-secrets, key: OPENAI_API_KEY }
          resources:
            requests: { cpu: "500m", memory: "512Mi" }   # guaranteed
            limits:   { cpu: "1",    memory: "1Gi" }      # ceiling
          readinessProbe:                  # "ready for traffic?" (uses /health)
            httpGet: { path: /health, port: 8080 }
            initialDelaySeconds: 10
          livenessProbe:                   # "still alive?" restart if not
            httpGet: { path: /health, port: 8080 }
            initialDelaySeconds: 20
```

> **Analogy:** "Always keep **3 workers**; each needs at least this much desk space
> (requests); don't let any hog more than this (limits); check they're **ready** before
> sending customers, and **restart** any that pass out (probes)."

---

## Step 3 — Service (stable address + load balancing)
`service.yaml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: llm-app
spec:
  type: ClusterIP          # internal; Ingress will expose it publicly
  selector: { app: llm-app }
  ports:
    - port: 80
      targetPort: 8080
```

> **Analogy:** Pods come and go (new IPs); the **Service is the permanent front-desk
> number** that always reaches whoever's on duty.

---

## Step 4 — Ingress (public HTTPS front door)
`ingress.yaml`:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: llm-ingress
  annotations:
    kubernetes.io/ingress.class: "gce"    # GKE provisions a Google load balancer
spec:
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: llm-app
                port: { number: 80 }
```

> **Analogy:** The **main entrance + signage** routing visitors (`/chat`, `/health`) to
> the right desk. GKE Ingress creates a real **Google Cloud Load Balancer** (your GCP Day
> 4 notes).

---

## Step 5 — Autoscaling (HPA) 📈
LLM traffic is spiky; scale pods on CPU (or custom metrics like queue depth / requests).
`hpa.yaml`:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: llm-hpa
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: llm-app }
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource: { name: cpu, target: { type: Utilization, averageUtilization: 60 } }
```

> **Analogy:** **Auto-hire more workers** (up to 20) when lines get long, send them home
> (down to 3) when quiet.

---

## Step 6 — Apply it all & watch
```bash
kubectl apply -f deployment.yaml -f service.yaml -f ingress.yaml -f hpa.yaml
kubectl get pods
kubectl get ingress          # get the public IP once provisioned
kubectl logs deployment/llm-app
```

---

## Step 7 — Update safely (rolling update / rollback)
```bash
kubectl set image deployment/llm-app llm-app=.../llm-app:1.1   # rolling update, zero downtime
kubectl rollout status deployment/llm-app
kubectl rollout undo deployment/llm-app                        # roll back if broken
```

> **Analogy:** Retrain workers **one at a time** so the shop never closes; if the new
> training backfires, **revert instantly**.

---

## GPU note (for self-hosted models — detail in Day 4.5)
If you host your **own** model, add a **GPU node pool** and request GPUs in the pod:
```bash
gcloud container node-pools create gpu-pool --cluster=llm-cluster --region=asia-south1 \
  --machine-type=g2-standard-8 --accelerator=type=nvidia-l4,count=1 --num-nodes=1
```
```yaml
        resources:
          limits:
            nvidia.com/gpu: 1        # this pod needs 1 GPU
```

> **Analogy:** Installing **heavy machinery (a GPU rig)** in one part of the workshop and
> assigning the model-serving worker to that station.

---

## Company-grade extras (what "handled by companies" really includes)
- **Workload Identity** — pods act as a GCP service account, no key files (GCP Day 2/8).
- **Secret management** — Secret Manager + CSI driver instead of raw K8s Secrets.
- **Namespaces** for `dev`/`staging`/`prod`; **RBAC** least privilege.
- **Ingress + TLS certs**, WAF/Cloud Armor, rate limiting at the edge.
- **Observability** — Cloud Monitoring/Logging, Prometheus/Grafana, Langfuse (Day 5).
- **GitOps CI/CD** — Argo CD / Cloud Build deploy manifests; **eval gate** before rollout (Day 5).
- **Cost control** — right-size requests/limits, autoscale nodes, **delete idle GPU pools**.
- **Regional cluster** for HA (GCP Day 8).

---

## Cloud Run vs GKE — when companies pick which
| Situation | Pick |
|---|---|
| App just **calls a hosted LLM API**, spiky traffic, small team | **Cloud Run** |
| **Self-hosting** open models on **GPUs** | **GKE** |
| Many microservices, service mesh, custom networking | **GKE** |
| Strict data residency / run everything in-VPC | **GKE** |
| Want minimal ops & scale-to-zero | **Cloud Run** |

---

## TL;DR (in plain English)
- Companies run LLM apps on GKE with the standard set: **Deployment** (N pods),
  **Service** (stable address), **Ingress** (public HTTPS LB), **HPA** (autoscale),
  **Secrets/ConfigMaps**, and **probes** for health.
- Deploy with `kubectl apply`; update via **rolling updates** (rollback if broken).
- For **self-hosted models**, add a **GPU node pool** and request `nvidia.com/gpu`.
- Production-grade means adding **Workload Identity, RBAC, TLS, observability, GitOps
  CI/CD with an eval gate, and cost controls**.
- **Rule of thumb:** hosted-API app → **Cloud Run**; GPU/self-hosted or complex platform → **GKE**.
