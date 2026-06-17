# Phase 3 Teaching Modules

This document explains the retrieval pipeline that turns long finance documents into usable evidence for the assistant.

## 1. RAG (Retrieval-Augmented Generation) Pipeline

Simple explanation: RAG (Retrieval-Augmented Generation) means retrieve useful context first, then generate the answer.

Technical explanation: The system embeds documents, stores them in a vector index, retrieves the most relevant chunks for a query, and then passes those chunks to the model for synthesis.

Why it matters in this project: It lets the assistant answer from documents and research instead of relying only on the model’s memory.

Example: A risk question about Apple can pull passages from a filing note before the response is written.

Common mistake: Calling something RAG (Retrieval-Augmented Generation) when retrieval is never actually used.

## 2. Document Ingestion

Simple explanation: Ingestion means loading source documents into the system.

Technical explanation: The app reads Markdown, plain text, or Portable Document Format (PDF) files, preserves metadata, and prepares them for splitting and embedding.

Why it matters in this project: The assistant needs real finance content to search through.

Example: Load a sample Tesla note and an Apple risk note from the docs folder.

Common mistake: Skipping metadata like source path or title.

## 3. Chunking Strategy

Simple explanation: Chunking breaks long documents into smaller pieces that are easier to search.

Technical explanation: The splitter uses windowed segments with overlap so neighboring context is retained across boundaries.

Why it matters in this project: Long filings or notes are too large to embed as a single block.

Example: Split a note into 800-character chunks with 150-character overlap.

Common mistake: Making chunks so large that retrieval becomes vague.

## 4. Embeddings

Simple explanation: Embeddings turn text into vectors that capture meaning.

Technical explanation: A sentence encoder maps each chunk and query into a dense numeric space where semantic similarity can be measured.

Why it matters in this project: Relevant chunks are found by similarity, not just exact keyword matches.

Example: A query about supply chain risk retrieves passages mentioning China or concentration risk.

Common mistake: Using different embedding models for indexing and querying.

## 5. Sentence-Transformers

Simple explanation: Sentence-transformers are models made for turning sentences and passages into embeddings.

Technical explanation: They produce dense vectors that work well for semantic search and retrieval tasks.

Why it matters in this project: They give better retrieval quality than manual keyword matching.

Example: Use BAAI/bge-small-en-v1.5 as a local semantic embedding model.

Common mistake: Assuming the embedding model is the same thing as the chat model.

## 6. Vector Database

Simple explanation: A vector database stores embeddings and finds the closest matches.

Technical explanation: FAISS (Facebook Artificial Intelligence Similarity Search) indexes vectors for nearest-neighbor search over many chunks.

Why it matters in this project: It makes document search fast and scalable.

Example: Search for Apple risk passages inside a local FAISS (Facebook Artificial Intelligence Similarity Search) index.

Common mistake: Not storing source metadata alongside the vectors.

## 7. Retriever

Simple explanation: The retriever fetches the most relevant chunks for a question.

Technical explanation: It embeds the query, searches the index, and returns top-scoring document chunks.

Why it matters in this project: It is the piece that provides evidence to the model.

Example: A risk question returns the Apple risk note and related passages.

Common mistake: Trusting only the top chunk without checking quality.

## 8. Retrieval Quality

Simple explanation: Retrieval quality means the right documents come back for the right question.

Technical explanation: Good retrieval balances recall and precision so the returned chunks are relevant and useful.

Why it matters in this project: Bad retrieval creates bad answers even if the model is strong.

Example: A Tesla trend query should retrieve Tesla notes, not unrelated Apple content.

Common mistake: Ignoring retrieval evaluation and only testing the final answer.

## 9. Grounded Answers

Simple explanation: A grounded answer is tied to retrieved evidence.

Technical explanation: The synthesis step should reference document chunks or tool outputs instead of guessing from model memory.

Why it matters in this project: Grounding reduces hallucination and increases trust.

Example: The assistant says Apple faces supply chain risk because the retrieved note mentions China concentration.

Common mistake: Letting the model invent reasons without evidence.

## 10. Metadata

Simple explanation: Metadata is extra information about each chunk.

Technical explanation: Metadata stores source path, title, chunk index, and other fields that help trace results back to their origin.

Why it matters in this project: You need sources for transparency and debugging.

Example: A retrieved chunk can show it came from docs/example_filings/apple_risk_note.md.

Common mistake: Saving only the text and losing provenance.

## 11. Save and Load Index

Simple explanation: You can store the vector index on disk and reuse it later.

Technical explanation: FAISS (Facebook Artificial Intelligence Similarity Search) supports saving and reloading the built index along with document metadata.

Why it matters in this project: It avoids rebuilding the index every time the app starts.

Example: Save the local vector store to data/vectorstore and load it on startup.

Common mistake: Rebuilding embeddings every run when the documents have not changed.

## 12. Testing RAG (Retrieval-Augmented Generation)

Simple explanation: Tests check that the pipeline loads documents and retrieves the right content.

Technical explanation: The test suite validates ingestion, chunking, vector store construction, and semantic retrieval behavior.

Why it matters in this project: Retrieval failures are often silent unless explicitly tested.

Example: Ask for Apple risk information and verify Apple or risk text appears in the top results.

Common mistake: Assuming retrieval works because the code runs without crashing.

## Post-Phase-7 Additions Mapped To Phase 3

### Fingerprint-based index reuse
- Added corpus fingerprinting (path, modification time, size) to select index folders deterministically.
- Why it matters: avoids full re-embedding on cold starts when source documents are unchanged.
- Teaching point: retrieval startup latency can often be reduced by precise change detection.

### Small-document atomic chunking
- Added minimum-size bypass so short notes are indexed as atomic chunks instead of being split unnecessarily.
- Why it matters: preserves compact market-note context and reduces splitter overhead.
- Teaching point: chunking strategy should be document-size aware.

### Retrieval score semantics made explicit
- Converted FAISS L2 distance to similarity and ranked descending, with boosts applied in true similarity direction.
- Why it matters: removes ambiguity in ranking interpretation and boost behavior.
- Teaching point: always document score direction and sort order.

### Reranker default and warmup
- Enabled reranker by default with environment opt-out.
- Added startup warmup for retriever initialization.
- Why it matters: better retrieval precision and smoother first-query latency.
- Teaching point: production retrieval quality often depends on post-retrieval reranking.

## Phase 3 Distinctions

### Retrieval vs Generation
- Retrieval finds evidence.
- Generation turns evidence into an answer.

### Embedding Model vs Chat Model
- Embedding model converts text into vectors.
- Chat model writes the final response.

### Chunking vs Indexing
- Chunking splits documents.
- Indexing stores chunk vectors for search.

### Grounded vs Ungrounded Output
- Grounded output cites retrieved evidence.
- Ungrounded output guesses from model memory.
