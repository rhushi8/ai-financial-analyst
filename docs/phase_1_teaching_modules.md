# Phase 1

This document captures the foundation concepts in the order used to design the project. Each module follows the same pattern: simple explanation, technical explanation, why it matters here, a small example, and a common mistake.

## 1. LLMs (Large Language Models)

Simple explanation: A large language model predicts and generates text based on context.

Technical explanation: An LLM (Large Language Model) uses transformer layers and attention to model relationships between tokens and produce the most likely continuation, shaped by prompts and surrounding context.

Why it matters in this project: The LLM (Large Language Model) turns tool output and retrieved evidence into a grounded analyst-style response.

Example: Given stock data for AAPL (Apple Inc. ticker symbol), the model summarizes trend, catalysts, and risk.

Common mistake: Asking the model for facts without giving it real data to work from.

## 2. APIs (Application Programming Interfaces)

Simple explanation: An API (Application Programming Interface) is a standardized way to request data or actions from another system.

Technical explanation: APIs (Application Programming Interfaces) expose endpoints or software development kit (SDK) methods with structured requests and responses, often over HTTP (Hypertext Transfer Protocol).

Why it matters in this project: yfinance, GDELT (Global Database of Events, Language, and Tone), and future external services are accessed through APIs (Application Programming Interfaces) or library wrappers around APIs (Application Programming Interfaces).

Example: Request Apple price history and receive OHLCV (Open, High, Low, Close, Volume) rows.

Common mistake: Assuming every response field always exists.

## 3. Tools

Simple explanation: A tool is a function the artificial intelligence (AI) system can call to do one specific job.

Technical explanation: A tool is a typed callable with defined input and output contracts, clear errors, and deterministic behavior where possible.

Why it matters in this project: Stock lookup, fundamentals, news search, and calculator logic should be tools, not free-form text.

Example: get_stock_price("AAPL", "1mo") returns normalized market data.

Common mistake: Returning messy strings instead of structured outputs.

## 4. Agents

Simple explanation: An agent decides which tool to use and in what order.

Technical explanation: An agent is a control loop that observes the question, selects actions, executes tools, and synthesizes a final answer.

Why it matters in this project: Different finance questions need different tools, so fixed rules alone are too limited.

Example: A comparison question might trigger two fundamentals calls and then a calculator step.

Common mistake: Giving an agent vague, overlapping tools with unclear responsibilities.

## 5. MCP (Model Context Protocol)

Simple explanation: MCP (Model Context Protocol) is a standard protocol for exposing tools and context to artificial intelligence (AI) clients.

Technical explanation: Model Context Protocol (MCP) defines a common way to advertise capabilities, schemas, and callable operations across clients.

Why it matters in this project: It lets the same tools be reused by other MCP (Model Context Protocol)-compatible apps later.

Example: The stock tool can be exposed to your app and a separate assistant client.

Common mistake: Confusing MCP (Model Context Protocol) with a data provider API (Application Programming Interface).

## 6. Embeddings

Simple explanation: Embeddings turn text into numbers that capture meaning.

Technical explanation: An embedding model maps text to a dense vector space where semantically similar texts are close together.

Why it matters in this project: Retrieval depends on semantic similarity, not just exact keywords.

Example: A risk query can match a filing section about regulation or debt.

Common mistake: Using different embedding models for indexing and querying.

## 7. Chunking

Simple explanation: Chunking splits long documents into smaller pieces.

Technical explanation: Chunking creates retrieval-friendly segments with overlap so context is not lost across boundaries.

Why it matters in this project: SEC (United States Securities and Exchange Commission) filings and long reports are too large to search as one block.

Example: A 10-K (annual report filed with the United States Securities and Exchange Commission) is split into 800-token chunks with overlap.

Common mistake: Making chunks too large or too small.

## 8. Vector Databases

Simple explanation: A vector database stores embeddings and finds the closest matches.

Technical explanation: It indexes vectors for approximate nearest-neighbor search using cosine similarity or inner product.

Why it matters in this project: It gives fast semantic lookup over many document chunks.

Example: FAISS (Facebook Artificial Intelligence Similarity Search) returns the top 5 chunks closest to a query embedding.

Common mistake: Not storing metadata like source, date, or section.

## 9. Retrievers

Simple explanation: A retriever fetches the most relevant text for a question.

Technical explanation: A retriever converts the query to an embedding, searches the vector store, and returns matching chunks.

Why it matters in this project: It supplies the evidence that makes answers grounded.

Example: A query about Apple risks retrieves litigation and supply-chain passages.

Common mistake: Trusting only the top result without checking relevance.

## 10. RAG (Retrieval-Augmented Generation)

Simple explanation: Retrieval-Augmented Generation (RAG) means retrieve evidence first, then generate the answer.

Technical explanation: RAG (Retrieval-Augmented Generation) combines a retriever with an LLM (Large Language Model) so output is conditioned on external evidence instead of model memory alone.

Why it matters in this project: It reduces hallucination and improves factual grounding.

Example: A news or filing excerpt is passed into the LLM (Large Language Model) before final synthesis.

Common mistake: Calling it RAG (Retrieval-Augmented Generation) when retrieval is not actually used.

## 11. Prompt Engineering

Simple explanation: Prompt engineering means writing instructions that shape model behavior.

Technical explanation: Good prompts define role, scope, output schema, citation rules, uncertainty language, and refusal behavior.

Why it matters in this project: Finance answers must be structured, transparent, and careful.

Example: The prompt can require sections like thesis, risks, and sources.

Common mistake: Leaving the output format vague.

## 12. Free Finance Data Sources

Simple explanation: These are public or free services that provide finance data.

Technical explanation: This project uses yfinance for market data and GDELT (Global Database of Events, Language, and Tone) for news, plus local documents for retrieval.

Why it matters in this project: The stack stays low-cost and reproducible.

Example: Pull Tesla price history and related headlines without paid APIs (Application Programming Interfaces).

Common mistake: Relying on one data source for every claim.

## 13. Local LLM (Large Language Model) vs Hosted LLM (Large Language Model)

Simple explanation: Local models run on your machine; hosted models run on a provider’s servers.

Technical explanation: Local deployment gives privacy and cost stability; hosted models often provide better raw capability but add latency, cost, and dependency on an external service.

Why it matters in this project: A local stack keeps the project free and portfolio-friendly.

Example: Ollama runs the model locally for answer synthesis.

Common mistake: Choosing a model too large for the available machine.

## 14. LangChain and LangGraph

Simple explanation: These are frameworks for building LLM (Large Language Model) applications and workflows.

Technical explanation: LangChain provides model and tool abstractions; LangGraph gives explicit stateful control over multi-step agent flows.

Why it matters in this project: They help organize tool routing and future agent logic cleanly.

Example: A graph can route a question to stock data, news, or RAG (Retrieval-Augmented Generation).

Common mistake: Using too much framework before validating the core flow.

## 15. Streamlit UI (User Interface)

Simple explanation: Streamlit is a fast way to build an interactive Python app user interface (UI).

Technical explanation: It uses a reactive script model with widgets, session state, and simple rendering of text, tables, and charts.

Why it matters in this project: It gets the finance assistant demo running quickly.

Example: A chat input sends a question and shows answer plus sources.

Common mistake: Putting all business logic directly inside the UI (User Interface) file.

## 16. End-to-End Architecture

Simple explanation: End-to-end architecture connects user input to a grounded answer.

Technical explanation: The system defines clean contracts between UI (User Interface), agent, tools, retrieval, synthesis, and trace metadata.

Why it matters in this project: It keeps the app modular, testable, and easy to extend.

Example: A compare-companies query can combine fundamentals, calculator, and RAG (Retrieval-Augmented Generation) evidence.

Common mistake: Letting components depend on each other through loose, untyped text.

## Post-Phase-7 Additions Mapped To Phase 1

### Prompt engineering for comparison tasks
- Added an explicit comparison prompt mode so synthesis instructions match head-to-head analysis structure.
- Why it matters: comparison answers need side-by-side reasoning constraints, not generic single-subject bullets.
- Teaching point: output-format instructions should adapt to intent, not remain static across task types.

### Entity resolution for formal company names
- Expanded aliases to include formal naming patterns such as Apple Inc and Microsoft Corporation.
- Why it matters: professional phrasing now resolves correctly, improving planner reliability and intent detection.
- Teaching point: language coverage in entity resolution is a foundational system capability, not a minor polish item.

## Required Distinctions

### API (Application Programming Interface) vs Tool
- API (Application Programming Interface): the external access surface.
- Tool: the callable capability the agent uses.

### Tool vs Agent
- Tool: does one specific job.
- Agent: decides which tools to use.

### MCP (Model Context Protocol) vs API (Application Programming Interface)
- MCP (Model Context Protocol): protocol for model-tool interoperability.
- API (Application Programming Interface): a service-specific request interface.

### Embeddings vs Vectors vs Retrieval
- Embeddings: the meaning representation.
- Vectors: the stored numeric values.
- Retrieval: the search step that finds relevant matches.

### Retriever vs RAG (Retrieval-Augmented Generation)
- Retriever: finds relevant context.
- RAG (Retrieval-Augmented Generation): retrieves context and uses it in generation.

### Local LLM (Large Language Model) vs Hosted LLM (Large Language Model)
- Local: free after setup, private, hardware-bound.
- Hosted: easier access, usually paid, provider-managed.

### Rule-Based Flow vs Agentic Flow
- Rule-based: fixed if/else routing.
- Agentic: the model chooses the path dynamically.

### Hallucinated Answer vs Grounded Answer
- Hallucinated: unsupported or invented claim.
- Grounded: claim backed by retrieved or tool-produced evidence.
