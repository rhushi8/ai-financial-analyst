# Finance AI Analyst

End-to-end AI financial analyst system with a free/mostly-free stack, built for portfolio demos and interview walkthroughs.

## Problem Statement
Build a grounded AI financial analysis assistant that can answer market questions with transparent evidence, explicit tool usage, and UI-friendly structured outputs.

## What Is Implemented (Phases 1 to 7)
- Phase 1: foundation architecture, modular package layout, and local run loop.
- Phase 2: typed finance tools (price, fundamentals, calculator, news) with traceability.
- Phase 3: retrieval-augmented generation pipeline with chunking, embeddings, and FAISS persistence.
- Phase 4: LangGraph orchestration for intent planning and multi-tool routing.
- Phase 5: richer Streamlit experience with diagnostics, source visibility, and interaction polish.
- Phase 6: grounding quality calibration, cautionary wording on weak evidence, and quality-focused tests.
- Phase 7: deployment and operations assets (Docker, Streamlit config, smoke and evaluation scripts).

## Runtime Capabilities
- Company name and ticker resolution.
- Indian market entities and index coverage (NIFTY, SENSEX, major NSE equities).
- Planner-driven tool orchestration (price, fundamentals, news, retrieval) with modes: `rule`, `hybrid`, `llm`.
- Price, fundamentals, comparison, and risk/news summaries.
- Generic market-ideas flow for prompts like "what to buy/sell now" with explicit disclaimer and confidence.
- Live market/fundamental data via yfinance.
- Live free news via GDELT with graceful fallback behavior.
- RAG grounding from local markdown, text, and PDF documents with metadata-aware retrieval, filtering, deduplication, and optional reranking.
- Local LLM synthesis via Ollama with deterministic fallback.
- Structured answer schema for dashboard rendering: summary, recommendation, views, citations, latency, warnings.
- Dashboard renders chart-ready price series and structured tabs (overview/news/risks/sources/technical).

## Architecture

Data flow:

`user query -> planner -> tool selection -> tool execution -> retrieval -> synthesis -> structured response -> UI`

Core modules:
- `src/finance_ai/agents/planner.py`: intent planning and fallback strategy.
- `src/finance_ai/agents/router.py`: explicit execution pipeline and partial-result handling.
- `src/finance_ai/rag/retriever.py`: metadata filtering, dedup, and retrieval ranking.
- `src/finance_ai/schemas/agent.py`: typed response contract shared by agent and UI.
- `src/finance_ai/tools/india_market.py`: India market scanner for broad buy/sell idea prompts.

India market scanner details:
- Uses a static India reference universe with sectors and index memberships.
- Builds market breadth snapshot (advancers/decliners/flat) and 1-month index trend snapshot.
- Produces ranked idea candidates with action buckets and rationale.
- Always includes educational-use disclaimer (not investment advice).
- Includes India-focused retrieval documents in `docs/example_india` for macro, sector, and company context grounding.
- `app/streamlit_app.py`: dashboard UI rendering structured fields directly.

## Tech Stack
- Python 3.11+
- Streamlit
- LangChain + LangGraph
- yfinance
- sentence-transformers
- FAISS
- pydantic + pydantic-settings
- Ollama (optional but recommended)

## Quickstart

### 1) Create and activate a virtual environment
Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install package

```powershell
pip install -e ".[dev]"
```

### 3) Configure environment
Copy `.env.example` to `.env` and adjust as needed.

Useful options:
- `FINANCE_AI_AGENT_PLANNER_MODE=hybrid`
- `FINANCE_AI_ENABLE_RERANK=false`
- `FINANCE_AI_RERANK_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2`

### 4) Optional local model setup

```powershell
ollama pull qwen2.5:7b-instruct
```

### 5) Run app

```powershell
streamlit run app/streamlit_app.py
```

### 6) Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The unit tests are deterministic and mock external network services for stability.

### 7) Run scenario evaluation

```powershell
.\.venv\Scripts\python.exe scripts/run_eval.py
```

## Deployment

### Docker

```powershell
docker build -t finance-ai-analyst .
docker run --rm -p 8501:8501 --env-file .env finance-ai-analyst
```

### Streamlit Cloud or local host
- Entry point: `app/streamlit_app.py`
- Ensure optional Ollama dependency is available if you want model synthesis.

## MCP Server

The project now includes an MCP-compatible stdio JSON-RPC server that exposes the same finance tools used by the app.

### Start MCP server

```powershell
finance-ai-mcp
```

### Exposed tools
- `get_stock_price`
- `get_fundamentals`
- `search_news`
- `calculate_financial_metric`
- `route_query`

### Supported methods
- `initialize`
- `tools/list`
- `tools/call`

This enables external MCP clients to reuse the tool layer and orchestration flow without coupling directly to Streamlit.

## Continuous Integration

GitHub Actions workflow runs on push and pull request with:
- linting on Python 3.11
- tests on Python 3.11 and 3.12
- a small MCP smoke call (`tools/list`)

Workflow file: `.github/workflows/ci.yml`

## Project Structure
- `app/`: Streamlit UI
- `src/finance_ai/`: agents, tools, rag, prompts, llm, utils
- `docs/`: teaching modules and sample retrieval docs
- `tests/`: unit and integration tests
- `scripts/`: evaluation and smoke scripts
- `.streamlit/`: app runtime config

## Teaching Modules
- `docs/phase_1_teaching_modules.md`
- `docs/phase_2_teaching_modules.md`
- `docs/phase_3_teaching_modules.md`
- `docs/phase_4_teaching_modules.md`
- `docs/phase_5_teaching_modules.md`
- `docs/phase_6_teaching_modules.md`
- `docs/phase_7_teaching_modules.md`

## Current Limitations
- Planner remains heuristic (deterministic + rules) rather than full model-native planning.
- News quality depends on free GDELT endpoint stability.
- Retrieval reranking is lightweight and does not yet use a cross-encoder reranker.
- This project is production-oriented but still tuned for local/demo operation.
