# Phase 2 Teaching Modules

This document explains the tool layer that powers the finance assistant. The goal in Phase 2 is to make the system do useful work with live data, while keeping outputs structured and testable.

## 1. Tool Layer

Simple explanation: Tools are focused functions that do one job for the assistant.

Technical explanation: A tool is a callable capability with a well-defined input schema, output schema, and error behavior.

Why it matters in this project: Finance questions need reliable actions like price lookup, fundamentals lookup, news search, and calculation.

Example: get_stock_price("AAPL", "1mo") returns normalized market data.

Common mistake: Returning raw text blobs instead of structured data.

## 2. Free Data Sources

Simple explanation: These are public or free services that provide finance data.

Technical explanation: Phase 2 uses yfinance for market and fundamentals data, plus a placeholder news source that is replaced later by GDELT (Global Database of Events, Language, and Tone) or another free feed.

Why it matters in this project: The app stays low-cost and reproducible.

Example: Pull recent Tesla prices without paying for a market data API (Application Programming Interface).

Common mistake: Building around a paid API (Application Programming Interface) before checking free alternatives.

## 3. yfinance

Simple explanation: yfinance is a Python wrapper for Yahoo Finance data.

Technical explanation: It retrieves historical OHLCV (Open, High, Low, Close, Volume) data and company metadata, but the returned data frame structure can be tricky, especially with single-ticker versus multi-ticker output.

Why it matters in this project: It provides live or near-live stock data for price and fundamentals tools.

Example: Download one month of AAPL (Apple Inc. ticker symbol) history and extract close, high, low, and volume.

Common mistake: Assuming the output shape is always the same.

## 4. Stock Price Tool

Simple explanation: This tool answers questions about recent price movement.

Technical explanation: It fetches historical bars, computes current price, change, range, and average volume, then returns a typed response model.

Why it matters in this project: Many user questions are simple trend or movement questions.

Example: “What is Tesla’s latest stock trend?”

Common mistake: Reporting trend without showing the time window used.

## 5. Fundamentals Tool

Simple explanation: This tool gives company valuation and health metrics.

Technical explanation: It reads metadata like market cap, PE (Price-to-Earnings) ratio, dividend yield, beta, and 52-week range from the finance source.

Why it matters in this project: Users often ask valuation or risk questions, not just price questions.

Example: “What is Apple’s PE (Price-to-Earnings) ratio and market cap?”

Common mistake: Treating a single metric as the full investment thesis.

## 6. Calculator Tool

Simple explanation: The calculator performs numeric finance calculations.

Technical explanation: It computes derived metrics like percentage change, implied price from a PE (Price-to-Earnings) multiple, and dividend income.

Why it matters in this project: Some user questions require arithmetic, not retrieval.

Example: Calculate percentage change from 100 to 120.

Common mistake: Making the LLM (Large Language Model) do arithmetic when a deterministic tool can do it exactly.

## 7. News Tool

Simple explanation: The news tool searches for recent relevant headlines.

Technical explanation: In early Phase 2 it can be a placeholder, but the interface is defined so later GDELT (Global Database of Events, Language, and Tone) integration is easy.

Why it matters in this project: Market moves often need context from headlines.

Example: Search for recent news about Nvidia.

Common mistake: Returning fake or invented articles.

## 8. Schemas

Simple explanation: Schemas define the shape of inputs and outputs.

Technical explanation: Pydantic models validate tool requests, tool responses, and agent answers so data stays predictable across the app.

Why it matters in this project: The UI (User Interface), agent, tools, and tests all depend on stable contracts.

Example: StockPriceResponse always includes ticker, current_price, retrieved_at, and error.

Common mistake: Passing dictionaries around without validation.

## 9. Tool Trace

Simple explanation: Tool trace records which tools were used and what happened.

Technical explanation: It captures tool name, inputs, outputs, duration, success flag, and error details for transparency and debugging.

Why it matters in this project: Finance answers should be explainable and auditable.

Example: The app can show that it called get_stock_price in 320 milliseconds (ms).

Common mistake: Hiding intermediate steps from the user.

## 10. Rule-Based Routing

Simple explanation: The system chooses tools using simple if/else logic.

Technical explanation: Query intent is detected with heuristics, then the router calls the appropriate tool before synthesizing a structured response.

Why it matters in this project: It is the simplest reliable way to prove tool usage before adding a more complex agent.

Example: A price question routes to the stock tool, a PE (Price-to-Earnings) question routes to the fundamentals tool.

Common mistake: Calling this an agent without showing the routing logic.

## 11. Structured Output

Simple explanation: The response should come back in a predictable format.

Technical explanation: The agent returns a schema with thesis, key metrics, risks, sources, confidence, and trace data.

Why it matters in this project: The UI (User Interface) can render consistent sections and the tests can validate behavior.

Example: A price answer includes current price, change, range, and source.

Common mistake: Returning only a single paragraph when the UI (User Interface) needs separate fields.

## 12. Error Handling

Simple explanation: The app should fail gracefully when data is missing.

Technical explanation: Each tool returns a typed response with an error field instead of throwing raw exceptions into the UI (User Interface).

Why it matters in this project: Finance APIs (Application Programming Interfaces) can fail or return partial data.

Example: Invalid ticker input returns an error message and empty metrics.

Common mistake: Letting tool errors crash the whole chat response.

## 13. Testing Live Data

Simple explanation: Tests check that tools and routing behave correctly.

Technical explanation: Unit tests validate schema shape, calculator math, intent routing, and real yfinance responses.

Why it matters in this project: Live data integrations can break quietly unless you test them.

Example: A test checks that AAPL (Apple Inc. ticker symbol) price lookup returns a positive current price.

Common mistake: Testing only mock objects and never validating the live path.

## 14. UI (User Interface) Transparency

Simple explanation: The UI (User Interface) should show what the system did, not just the final answer.

Technical explanation: The Streamlit app displays tool calls, metrics, and sources alongside the answer.

Why it matters in this project: Transparency makes the app feel trustworthy and interview-ready.

Example: Show the stock tool call and source in an expander.

Common mistake: Hiding the data flow behind a single paragraph.

## Post-Phase-7 Additions Mapped To Phase 2

### Tool runtime hardening (yfinance)
- Added a dedicated requests session with retries and explicit timeout defaults for yfinance calls.
- Why it matters: prevents indefinite hangs during rate limits or network stalls.
- Teaching point: tool reliability starts at transport-level controls, not only exception handling.

### Ticker validation expanded for global exchanges
- Replaced simplistic length checks with regex-based ticker validation that supports suffixes such as .NS and .BO.
- Why it matters: Indian market tools and stock tools now use consistent ticker acceptance rules.
- Teaching point: validation rules should match real exchange symbol formats, not approximate heuristics.

### Dead-code cleanup in price fetching path
- Removed duplicated/unreachable empty-data guard in get_stock_price.
- Why it matters: improves readability and avoids confusion about runtime invariants.
- Teaching point: duplicate guards often indicate partially merged refactors and should be collapsed.

### Cache semantics upgraded
- File cache now stores version and timestamp metadata, enforces TTL on disk, and invalidates legacy unsafe entries.
- Why it matters: stale responses no longer survive process restarts indefinitely.
- Teaching point: cache correctness (freshness, invalidation) is more important than cache hit rate.

## Phase 2 Distinctions

### API (Application Programming Interface) vs Tool
- API (Application Programming Interface) is the external interface.
- Tool is the specific callable capability the assistant uses.

### Tool vs Agent
- Tool executes one job.
- Agent selects tools and combines their outputs.

### Live Data vs Mock Data
- Live data comes from a real source like yfinance.
- Mock data is fixed test data used only when live calls are not needed.

### Structured Response vs Free-Form Text
- Structured response is schema-based and easy to render.
- Free-form text is harder to test and harder for the UI (User Interface) to consume.
