# Phase 7 Teaching Modules

Phase 7 packages the project for reproducibility, deployment, and portfolio presentation.

## 1. Production Readiness

Simple explanation: Production readiness means others can run and evaluate your system reliably.

Technical explanation: It includes reproducible setup, explicit environment configuration, test command paths, and stable entrypoints.

Why it matters in this project: Resume-quality projects should be easy for recruiters and peers to run.

Example: README includes setup, run, test, and evaluation commands.

Common mistake: Assuming evaluators will infer missing setup steps.

## 2. Containerization

Simple explanation: Containerization packages app and dependencies into one deployable unit.

Technical explanation: A Dockerfile defines runtime image, install steps, exposed port, and startup command.

Why it matters in this project: It reduces "works on my machine" issues.

Example: docker build and docker run for Streamlit app on port 8501.

Common mistake: Forgetting to copy required source directories into the image.

## 3. Environment Management

Simple explanation: Environment management keeps secrets and settings outside code.

Technical explanation: pydantic-settings reads environment variables from .env and runtime environment.

Why it matters in this project: You can tune behavior without changing source files.

Example: FINANCE_AI_LOW_GROUNDING_THRESHOLD adjusts caution strictness.

Common mistake: Hardcoding environment-specific values.

## 4. Operational Scripts

Simple explanation: Operational scripts speed up common workflows.

Technical explanation: Scripts can run smoke demos and scenario evaluations to validate app behavior quickly.

Why it matters in this project: Faster quality checks improve iteration and confidence before demos.

Example: run_eval.py checks core query types and route coverage.

Common mistake: Relying only on manual clicking in the UI (User Interface).

## 5. Documentation Design

Simple explanation: Good documentation helps others understand architecture and decisions.

Technical explanation: README should cover capabilities, architecture, commands, deployment, and known limitations.

Why it matters in this project: Communication quality strongly affects portfolio impact.

Example: Dedicated sections for phase status, runtime coverage, and teaching modules.

Common mistake: Writing only installation steps with no design rationale.

## 6. Demo Narrative

Simple explanation: Demo narrative is how you explain the project in interviews.

Technical explanation: A strong narrative walks through user query -> routing -> tools -> retrieval -> synthesis -> confidence.

Why it matters in this project: Interviewers assess system thinking, not just code volume.

Example: Show a compare query and explain each node executed.

Common mistake: Demoing outputs without describing internal flow.

## 7. Release Checklist

Simple explanation: Checklist ensures quality before sharing publicly.

Technical explanation: Typical checks include tests passing, scripts running, docs updated, and environment examples aligned.

Why it matters in this project: Consistency and polish increase reviewer trust.

Example: Run pytest and run_eval.py before publishing.

Common mistake: Publishing after major refactor without rerunning tests.

## 8. Continuous Integration (CI)

Simple explanation: Continuous Integration (CI) automatically validates your code changes.

Technical explanation: A GitHub Actions workflow runs dependency installation, automated tests, and an MCP (Model Context Protocol) smoke check on push and pull request.

Why it matters in this project: It catches regressions early and demonstrates production engineering discipline.

Example: CI runs pytest on Python 3.11 and 3.12 and verifies tools/list from the MCP server.

Common mistake: Treating tests as optional local-only checks.

## 9. MCP (Model Context Protocol) Exposure

Simple explanation: MCP (Model Context Protocol) exposure lets external AI clients call your tools through a standard interface.

Technical explanation: A stdio JSON-RPC server exposes initialize, tools/list, and tools/call methods for core finance tools and full route_query orchestration.

Why it matters in this project: The same tool layer can be reused beyond Streamlit, increasing interoperability and system value.

Example: An MCP client can call get_stock_price or route_query without importing your app code directly.

Common mistake: Building tools that only work inside one UI (User Interface) runtime.

## 10. Portfolio Positioning

Simple explanation: Positioning means presenting the project in a way that highlights real skills.

Technical explanation: Emphasize architecture, reliability strategy, observability, and tradeoff decisions.

Why it matters in this project: It demonstrates applied AI engineering beyond prompt chaining.

Example: Discuss why LangGraph was chosen for explicit state transitions.

Common mistake: Framing it as only a UI (User Interface) chatbot.

## 11. Known Limitations and Roadmap

Simple explanation: State what is still missing and what comes next.

Technical explanation: Include constrained areas like deeper evaluation benchmarks, stronger test data versioning, and advanced backtesting modules.

Why it matters in this project: Honest limitations signal engineering maturity.

Example: Note that advanced evaluation datasets and backtesting are next milestones.

Common mistake: Claiming full production readiness when core enterprise needs are missing.

## 12. Phase 7 Distinctions

### Prototype vs Deployable Artifact
- Prototype proves concept viability.
- Deployable artifact supports reproducibility and external evaluation.

### Feature Count vs Engineering Quality
- Feature count is raw functionality volume.
- Engineering quality is reliability, observability, and maintainability.

### Demo Output vs System Understanding
- Demo output is what the app says.
- System understanding is why it said that and how it was validated.

## Post-Phase-7 Additions Mapped To Phase 7

### Environment onboarding clarity
- Updated .env.example to include required and optional runtime variables with current defaults and safe overrides.
- Why it matters: setup no longer depends on reverse-engineering config.py.

### CI pipeline modernization
- Reworked CI into separate lint and test jobs.
- Added dependency caching and pytest cache reuse.
- Why it matters: faster feedback loops and clearer failure isolation.

### State and constants hygiene
- Centralized Streamlit session defaults in init_state.
- Replaced repeated history magic numbers with named constants for maintainability.
- Why it matters: improves readability, testability, and predictable behavior over time.

### Production-facing quality trend
- After these updates the non-live suite remained green while feature coverage increased.
- Teaching point: deployment readiness is iterative; each hardening pass should preserve regression safety.
