# Phase 4 Teaching Modules

This phase upgrades the system from mostly rule-based routing to an agentic orchestration flow with explicit state transitions and multi-tool execution.

## 1. Agentic Orchestration

Simple explanation: Instead of one large if/else function, the system runs a graph of steps.

Technical explanation: A LangGraph state machine plans intent, executes the required tool nodes, and then finalizes a grounded answer.

Why it matters in this project: It keeps complex finance query handling modular, debuggable, and extensible.

Example: A news query can run both search_news and rag_retriever before synthesis.

Common mistake: Calling code “agentic” while still hardcoding all logic in one monolithic branch.

## 2. Agent State

Simple explanation: Agent state is the shared memory passed between graph nodes.

Technical explanation: The state includes query, resolved entities, intent, tool traces, metrics, risks, sources, evidence lines, and confidence.

Why it matters in this project: Every node reads and writes the same structured state, so behavior is transparent and testable.

Example: The news node appends article evidence and sources, then the finalize node synthesizes from that state.

Common mistake: Letting nodes return ad-hoc fields that break downstream assumptions.

## 3. Intent Planning

Simple explanation: The system chooses a route based on query intent.

Technical explanation: The intent planner classifies into price, fundamentals, rag (Retrieval-Augmented Generation), news, compare, or unknown based on query keywords plus entity resolution.

Why it matters in this project: Finance questions vary; one fixed path cannot handle all query styles.

Example: “Compare Apple and Microsoft” routes to compare node only when two entities are detected.

Common mistake: Ignoring ambiguity and forcing every query into the same tool path.

## 4. Multi-Tool Execution

Simple explanation: Some queries need multiple tools, not just one.

Technical explanation: The compare path runs fundamentals and price for each company, while the news path runs news retrieval and optional rag (Retrieval-Augmented Generation) grounding.

Why it matters in this project: Real analyst answers usually combine valuation, price behavior, and contextual evidence.

Example: A compare answer includes market cap, PE (Price-to-Earnings) ratio, current price, and recent change side by side.

Common mistake: Returning an answer after the first tool call even when more context is needed.

## 5. Real News Integration

Simple explanation: News is now fetched from a free live source.

Technical explanation: The search_news tool calls the GDELT (Global Database of Events, Language, and Tone) DOC (Document) API (Application Programming Interface) in artlist mode, parses headline metadata, and returns structured articles.

Why it matters in this project: “Latest news” questions now use real external data, not placeholders.

Example: Query Nvidia headlines and parse article titles, uniform resource locators (URLs), and seen dates.

Common mistake: Depending on paid news APIs (Application Programming Interfaces) in a free-stack project.

## 6. News plus RAG (Retrieval-Augmented Generation) Blending

Simple explanation: News and local retrieval can complement each other.

Technical explanation: The news node pulls live articles and then calls rag (Retrieval-Augmented Generation) retrieval for additional grounding from local finance notes.

Why it matters in this project: This improves answer quality when live news is sparse or incomplete.

Example: If GDELT (Global Database of Events, Language, and Tone) returns few results, local risk notes still provide grounded evidence.

Common mistake: Using only one context source and leaving obvious blind spots.

## 7. Structured Finalization

Simple explanation: Final answer is assembled in a dedicated finalize step.

Technical explanation: The finalize node merges evidence and tool summaries, then generates thesis text via local LLM (Large Language Model) synthesis with deterministic fallback.

Why it matters in this project: It keeps output format consistent across all intent paths.

Example: Even if one tool fails, finalize can still build a cautious, grounded response.

Common mistake: Formatting output inside each tool node differently.

## 8. Reliability and Fallbacks

Simple explanation: The agent should degrade gracefully when dependencies fail.

Technical explanation: The news tool captures network failures; synthesis falls back when Ollama is unavailable; the rag (Retrieval-Augmented Generation) service falls back to simple embeddings.

Why it matters in this project: Portfolio projects should demonstrate robust behavior, not brittle demos.

Example: If GDELT (Global Database of Events, Language, and Tone) is unavailable, response still includes retriever evidence and clear caveats.

Common mistake: Crashing the full response pipeline on one upstream API (Application Programming Interface) error.

## 9. Testing Phase 4

Simple explanation: Tests verify graph routing behavior and multi-tool execution.

Technical explanation: Tests assert company-name resolution, rag (Retrieval-Augmented Generation) path triggering, compare path with two entities, and news path traces.

Why it matters in this project: Agentic systems can silently regress without route-level tests.

Example: News test validates that tool trace includes search_news or retrieval context.

Common mistake: Only testing final text and ignoring tool trace correctness.

## 10. Phase 4 Distinctions

### Rule-Based Routing vs Agent Graph
- Rule-based routing is a single procedural branch tree.
- Agent graph uses explicit nodes, state, and transitions.

### Single-Tool Answer vs Multi-Tool Answer
- Single-tool answers rely on one source.
- Multi-tool answers combine complementary evidence.

### Live News vs Local Retrieval
- Live news gives near-real-time signals.
- Local retrieval gives stable, curated context.

### Planning vs Finalization
- Planning chooses the route.
- Finalization composes the answer from accumulated evidence.

## Post-Phase-7 Additions Mapped To Phase 4

### New market_general intent behavior
- Added a dedicated market_general intent for broad macro queries with no resolved company entity.
- Updated routing to prefer search_news for global macro, and include India market tools only when India context is explicit.
- Teaching point: intent design must preserve semantic scope (global vs region-specific).

### Compare intent now enforces news coverage
- Compare planning now always sets requires_news=true and ensures search_news is in the tool sequence.
- LLM planner outputs for compare are normalized post-plan so news cannot be accidentally omitted.
- Teaching point: critical context requirements should be enforced as planner invariants, not left to model discretion.

### Compare-path concurrency depth
- Upgraded compare routing from dual-company parallelism to deeper per-company tool concurrency.
- Why it matters: price, fundamentals, and news can execute concurrently for each side.
- Teaching point: there are multiple layers of parallelism in orchestration (entity-level and tool-level).

### Comparison scoring expanded and normalized
- Comparison decisioning now scores across momentum, valuation, volatility, dividend yield, and market cap.
- Final side scores are normalized by total available metric weight to avoid bias from missing fields.
- Teaching point: model comparisons should degrade gracefully when only partial metric overlap exists.

### Formal-name entity resolution coverage
- Added aliases for professional naming patterns such as Apple Inc, Microsoft Corporation, Alphabet Inc, Meta Platforms, and Amazon.com.
- Why it matters: enterprise-style user phrasing now resolves to the correct ticker instead of falling through to unknown intent.
- Teaching point: resolver quality depends on real-world language coverage, not only casual aliases.

### Structured synthesis contract enforcement
- Synthesis now expects machine-readable recommendation JSON and extracts recommendation+rationale deterministically.
- Parser now takes the first valid recommendation block to avoid ambiguous late-block overrides.
- Teaching point: agent reliability improves when generation outputs strict, parseable contracts.

### Comparison-aware synthesis prompt mode
- Prompt builder now supports is_comparison mode with explicit head-to-head bullet guidance.
- Compare synthesis asks for alternating company bullets to improve direct comparability and reduce single-company drift.
- Teaching point: prompt structure should mirror task structure, especially for comparative reasoning.
