# Phase 5 Teaching Modules

Phase 5 focuses on user experience, transparency, and response explainability in the Streamlit application.

## 1. UX (User Experience) for AI Applications

Simple explanation: UX (User Experience) is how smooth and clear the app feels for the user.

Technical explanation: For AI systems, UX (User Experience) includes interaction latency, answer readability, source visibility, and confidence signaling.

Why it matters in this project: A finance assistant is only useful when users can understand what it did and trust the output.

Example: Show confidence, tools used, sources, and risks in clearly separated sections.

Common mistake: Returning one long paragraph with no supporting structure.

## 2. Session State

Simple explanation: Session state stores chat context between Streamlit reruns.

Technical explanation: Streamlit reruns the script on each interaction; session state preserves message history and interaction metadata.

Why it matters in this project: Chat continuity requires durable state for both user and assistant messages.

Example: Persist both plain message text and structured tool payloads.

Common mistake: Storing only text and losing trace data for prior turns.

## 3. Diagnostics Panels

Simple explanation: Diagnostics panels show how the assistant arrived at the answer.

Technical explanation: The interface presents tool traces, latencies, inputs, outputs, and quality metrics using tabs and expanders.

Why it matters in this project: It improves trust, debugging speed, and interview explainability.

Example: A tool trace tab listing get_stock_price duration and payload.

Common mistake: Hiding all internal steps behind a black-box answer.

## 4. Confidence Display

Simple explanation: Confidence gives a rough estimate of answer reliability.

Technical explanation: Confidence is calibrated from routing outcome, tool success, and grounding score.

Why it matters in this project: Finance users need a reliability signal before acting on insights.

Example: A 0.82 confidence with rich evidence is stronger than 0.31 with weak evidence.

Common mistake: Showing confidence without explaining what affects it.

## 5. Source Transparency

Simple explanation: Every claim should be traceable to a source.

Technical explanation: The app renders source links or labels for news APIs (Application Programming Interfaces), yfinance calls, and retrieval chunks.

Why it matters in this project: Source visibility is central to grounded AI behavior.

Example: Show both GDELT article URLs (Uniform Resource Locators) and local document retrieval sources.

Common mistake: Listing generic source names without specific evidence pointers.

## 6. Interaction Design

Simple explanation: Good interaction design reduces user effort.

Technical explanation: Quick prompt buttons, clear chat input, and reset controls lower friction for demos and real use.

Why it matters in this project: Faster iteration makes testing and stakeholder demos more effective.

Example: Sidebar prompt buttons for compare/news/risk queries.

Common mistake: Requiring users to remember exact query templates.

## 7. Visual Hierarchy

Simple explanation: Important information should stand out first.

Technical explanation: Use card-like sections, tab grouping, and metric placement to prioritize thesis then evidence.

Why it matters in this project: Finance answers combine multiple data layers and can be cognitively heavy.

Example: Top row for confidence/tool counts, followed by metrics and evidence tabs.

Common mistake: Mixing all metrics and logs in one unstructured block.

## 8. Responsiveness and Readability

Simple explanation: The app should stay usable across different screen sizes.

Technical explanation: Wide layout plus compact metrics and collapsible sections improve readability on desktop and laptop screens.

Why it matters in this project: Portfolio evaluators may open the app on different devices.

Example: Tabs prevent long scrolling when tool traces are large.

Common mistake: Letting large JSON outputs overwhelm the main answer area.

## 9. Error Communication

Simple explanation: Errors should be clear but non-disruptive.

Technical explanation: Runtime notes and warnings are shown in context while preserving successful partial outputs.

Why it matters in this project: External data systems can fail intermittently.

Example: Show news fetch warning while still providing retrieval-backed context.

Common mistake: Replacing all content with a generic failure message.

## 10. Phase 5 Distinctions

### Feature Rich vs Feature Noisy
- Feature rich means high-value visibility.
- Feature noisy means too many panels without hierarchy.

### Transparency vs Information Overload
- Transparency supports trust and debugging.
- Overload confuses users and reduces readability.

### Metrics vs Narrative
- Metrics quantify key signals.
- Narrative explains what those signals imply.

## Post-Phase-7 Additions Mapped To Phase 5

### Rich history replay
- Chat history now stores full typed answers and replays prior turns with expandable full analysis rendering.
- Why it matters: users can revisit charts, sources, risks, and explanation tabs for older messages.
- Teaching point: preserving structured payloads in session history unlocks much better UX.

### Sidebar interaction model improved
- Added Suggestions and History tabs, with clickable history entries that can rerun prior prompts.
- Teaching point: UI navigation primitives should support exploration, not only linear chat.

### Input behavior consistency
- Main query form now uses clear_on_submit=True to prevent accidental duplicate submissions.
- Removed misleading manual query-reset write after render.
- Teaching point: rely on widget lifecycle semantics instead of post-render state hacks.

### Formatting consistency and reuse
- Unified confidence/grounding display formatting to percentages.
- Added shared formatter helpers for comparison metrics to remove repeated inline None-check patterns.
- Teaching point: presentation helpers reduce drift and keep UI behavior testable.
