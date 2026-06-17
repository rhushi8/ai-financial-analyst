# AI Financial Analyst

A grounded, agentic AI assistant that answers stock-market questions with **evidence-backed, source-cited analysis** instead of hallucinated numbers. It plans which tools to call, gathers live market data, news, and documents, scores how well its own answer is supported, and returns a structured **BUY / HOLD / SELL** view with citations and a confidence level.

## Problem Statement
Large language models answer financial questions fluently but unreliably — they hallucinate prices, ratios, and news, and give no signal of how well-supported an answer actually is. When the output informs a money decision, that mix of confident tone and unverifiable content is unacceptable. The problem this project addresses: deliver natural-language financial analysis that stays grounded in real, current data and is transparent about the evidence and confidence behind every claim.

## Key features
- **Planner-driven orchestration** — classifies intent (price, fundamentals, news, comparison, market ideas) and routes to the right tools; runs in `rule`, `hybrid`, or `llm` mode with a deterministic fallback so it never hard-fails.
- **Parallel tool execution** — live price & fundamentals (yfinance), free news (GDELT), and an India market scanner (NIFTY / SENSEX) run concurrently.
- **RAG over documents** — chunking + sentence-transformer embeddings + FAISS persistence, with metadata filtering, deduplication, and optional reranking.
- **Grounding & confidence** — scores how well evidence supports the answer, calibrates a confidence value, softens wording when evidence is weak, and attaches source citations.
- **Stock comparison engine** — side-by-side momentum, P/E, beta, market cap, and dividend yield → a weighted BUY/HOLD decision with bull and bear cases.
- **Structured, typed output** — a Pydantic `AnalystAnswer` (summary, recommendation, confidence, citations, warnings, latency, tool traces) rendered in a Streamlit dashboard.
- **MCP server** — exposes the same finance tools over JSON-RPC for external agent clients.

## How it works
```
user query → planner → tool selection → tool execution → RAG retrieval → grounded synthesis → grounding/quality check → structured response → UI
```
The LLM never answers from memory alone — it is guided by the planner, tool outputs, retrieved context, and a grounding check before anything reaches the user.

## Tech stack
Python · Streamlit · LangChain (RAG) · FAISS · sentence-transformers · yfinance · GDELT · Ollama (local LLM) · Pydantic · pytest · Docker · GitHub Actions

## Quickstart
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows (use source .venv/bin/activate on macOS/Linux)
pip install -e ".[dev]"
copy .env.example .env              # then adjust settings
streamlit run app/streamlit_app.py
```
Optional local model for synthesis: `ollama pull qwen2.5:7b-instruct`
Run the test suite: `pytest -q`

## Project structure
- `app/` — Streamlit UI
- `src/finance_ai/` — agents (planner, router), tools, rag, llm, schemas, utils
- `tests/` — deterministic unit/integration tests (external services mocked)
- `scripts/` — evaluation & smoke scripts
- `docs/` — sample retrieval documents and design notes
- `Dockerfile`, `.github/workflows/ci.yml` — containerization & CI

## Notes & limitations
- The planner is heuristic (rules + deterministic fallback), not full model-native planning.
- News quality depends on the free GDELT endpoint; the system degrades gracefully if it is unavailable.
- Educational / portfolio project — **not investment advice.**
