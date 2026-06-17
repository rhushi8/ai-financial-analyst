# Phase 6 Teaching Modules

Phase 6 focuses on reliability, grounding quality, evaluation, and regression protection.

## 1. Grounding Quality

Simple explanation: Grounding quality measures whether answers are supported by evidence.

Technical explanation: A grounding score combines evidence presence, source availability, and tool trace coverage into a normalized confidence signal.

Why it matters in this project: Finance outputs must be evidence-backed, not pure language-model fluency.

Example: A response with evidence lines, sources, and tool trace gets a higher score.

Common mistake: Treating fluent wording as correctness.

## 2. Confidence Calibration

Simple explanation: Calibration aligns confidence with actual support quality.

Technical explanation: Base confidence from routing is blended with grounding score and set to zero when hard errors occur.

Why it matters in this project: Confidence should decrease when evidence is thin.

Example: A low-evidence answer gets lower calibrated confidence than a multi-source answer.

Common mistake: Keeping confidence fixed for all routes.

## 3. Cautionary Wording

Simple explanation: Weak evidence should trigger careful language.

Technical explanation: If grounding drops below a threshold, append a caution note to avoid overclaiming.

Why it matters in this project: This reduces misleading certainty in high-stakes domains.

Example: "Grounding note: evidence coverage is limited..."

Common mistake: Making bold recommendations despite sparse evidence.

## 4. Regression Testing

Simple explanation: Regression tests prevent old features from breaking after new changes.

Technical explanation: Tests cover routing, tools, retrieval, and quality helper functions with deterministic checks.

Why it matters in this project: Agent systems regress easily when nodes or prompts change.

Example: Test that price route includes get_stock_price and grounding_score metadata.

Common mistake: Testing only happy-path text output.

## 5. Scenario Evaluation

Simple explanation: Scenario evaluation is a lightweight benchmark on representative prompts.

Technical explanation: A scripted evaluator runs multiple queries and checks confidence thresholds, source presence, and required tools.

Why it matters in this project: It catches practical behavior issues beyond isolated unit tests.

Example: run_eval.py validates compare/news/price/fundamentals scenarios.

Common mistake: Declaring quality based only on one demo query.

## 6. Reliability Engineering

Simple explanation: Reliability means graceful behavior when dependencies fail.

Technical explanation: Tool-level exceptions become structured error fields; the system preserves partial outputs and trace logs.

Why it matters in this project: Live data APIs (Application Programming Interfaces) are variable and occasionally unavailable.

Example: News API (Application Programming Interface) outage still returns local retrieval context.

Common mistake: Failing the entire answer on one tool exception.

## 7. Threshold Tuning

Simple explanation: Threshold tuning sets practical cutoffs for warnings.

Technical explanation: The low grounding threshold is configurable via environment settings for iterative calibration.

Why it matters in this project: Different datasets and demo goals need different strictness.

Example: Raise threshold for stricter grounding warnings in production.

Common mistake: Hardcoding thresholds with no environment override.

## 8. Observability

Simple explanation: Observability helps you inspect model behavior over time.

Technical explanation: Tool traces, quality warnings, and confidence signals form a minimal observability layer in the UI.

Why it matters in this project: It supports debugging and interview narration of system decisions.

Example: Review failed tool traces and corresponding confidence drop.

Common mistake: Logging only final thesis text.

## 9. Risk Communication

Simple explanation: Risk communication emphasizes uncertainty and limits.

Technical explanation: The output includes risk bullets plus confidence and source context to avoid false precision.

Why it matters in this project: Finance users need nuanced interpretation, not absolute statements.

Example: "Signals are mixed; verify with primary filings."

Common mistake: Presenting probabilistic insight as certainty.

## 10. Phase 6 Distinctions

### Accuracy vs Groundedness
- Accuracy is factual correctness.
- Groundedness is whether claims are backed by presented evidence.

### Unit Tests vs Scenario Evaluation
- Unit tests validate isolated behavior.
- Scenario evaluation validates end-to-end user outcomes.

### Error Handling vs Error Hiding
- Error handling preserves context and informs users.
- Error hiding masks failures and harms trust.

## Post-Phase-7 Additions Mapped To Phase 6

### Partial-success synthesis path
- Added explicit handling for mixed tool outcomes: failed tools produce warnings while synthesis continues on successful evidence.
- Grounding and confidence now weight successful traces, not total attempted traces.
- Teaching point: graceful degradation should be measurable, not only narrative.

### Compare-news guardrail in planning
- Compare intent now enforces news retrieval even when an LLM-produced plan omits search_news.
- Why it matters: bull/bear construction and synthesis keep current-event coverage instead of silently losing context.
- Teaching point: enforce non-negotiable planning constraints after model planning to reduce brittle behavior.

### Recommendation robustness upgrades
- Removed recommendation inference from free-text keyword scanning.
- Recommendation now comes from structured synthesis output, with HOLD fallback only when structured block is missing/malformed.
- Teaching point: classification from unstructured prose is brittle; schema-first generation is safer.

### Comparison scoring robustness upgrades
- Comparison scoring now uses normalized weighted metrics (momentum, P/E, beta, dividend yield, market cap).
- If metric overlap is limited, decision logic degrades to Balanced/HOLD instead of overconfident winner selection.
- Teaching point: reliability includes making no-call decisions when evidence dimensions are insufficient.

### Reliability-through-cache correctness
- Disk TTL/version checks and legacy cache invalidation eliminate stale-value regressions.
- Teaching point: reliability bugs often hide in state persistence layers.

### Tool-layer timeout reliability
- Explicit request timeouts prevent indefinite blocking in external data calls.
- Teaching point: timeouts are a correctness feature in production systems, not only a performance feature.
