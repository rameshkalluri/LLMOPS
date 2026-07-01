# Agents & Tools

## Tools = giving the LLM hands 🔧
By itself, an LLM can only **produce text**. **Tools** let it **do things**: search the
web, query a database, call an API, run code, look up your RAG store.

> **Analogy:** The intern is smart but stuck at a desk with no phone. **Tools are the
> phone, calculator, and computer** you give them so they can actually **act**, not just
> talk.

---

## Function / tool calling (how it works)
You describe the available tools (name, purpose, inputs). The model, when useful,
**outputs a request to call a tool** with arguments; your code runs it and returns the
result; the model uses that result to answer.

```
User: "What's 15% tip on my $80 bill, and is table 5 free?"
Model → calls calculator(80*0.15) → 12
Model → calls booking_api(check, table=5) → "free"
Model → "A 15% tip is $12, and table 5 is available."
```

> **Analogy:** The intern says "I need the **calculator** for this part and the
> **booking system** for that part," uses them, then gives you one clean answer.

---

## What is an Agent? 🤖
An **agent** is an LLM that **decides which tools to use, in what order**, looping until
the task is done — instead of following a fixed script.

> **Analogy:** A **fixed chain** is a worker following a **printed checklist**. An
> **agent** is a worker who **figures out the steps themselves**: "first I'll look this
> up, then calculate, then book." More flexible — and less predictable.

### The ReAct loop (Reason + Act)
```
Think → choose a tool → Act (run it) → observe result → Think again → ... → Final answer
```

---

## Agents vs Chains (choose carefully)

| | **Chain (fixed steps)** | **Agent (decides steps)** |
|---|---|---|
| Control | High, predictable | Lower, flexible |
| Cost/latency | Lower (few calls) | Higher (loops = many calls) |
| Reliability | Easier to test | Harder (can loop/wander) |
| Analogy | Printed checklist | Improvising worker |
| Use when | You know the steps | Steps vary per request |

> **LLMOps advice:** Prefer the **simplest thing that works**. Use a **chain** when the
> steps are known; reach for an **agent** only when the task truly needs dynamic
> decisions. Agents are powerful but **harder to control, cost more, and can loop**.

---

## Guardrails for agents (important) 🚧
- **Limit tool permissions** (least privilege — like Day 2 IAM): a tool that can only
  *read* can't delete your database.
- **Cap iterations** (max steps) to prevent infinite loops.
- **Validate tool inputs/outputs**; sandbox any code execution.
- **Log every step** (tool calls + args) for debugging and audit (Day 5).
- Beware **prompt injection** via tool results/web pages (Day 5 security).

---

## TL;DR (in plain English)
- **Tools = hands** for the LLM (search, DB, APIs, code); **function calling** is how it
  requests them.
- An **agent** = an LLM that **decides which tools to use and loops** (ReAct: think → act →
  observe) until done.
- **Chains** are predictable/cheap; **agents** are flexible but costlier and harder to
  control — use the simplest that works.
- Guard agents: **least-privilege tools, max-step limits, input/output validation,
  full logging.**
