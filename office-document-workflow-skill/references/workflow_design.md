# Workflow Design

The framework separates document mechanics from LLM text generation.

1. Detect Office type from extension.
2. Use an adapter to extract `TextBlock` objects.
3. Batch text blocks by deterministic size limits.
4. Send each block to an LLM provider with context, style hints, and glossary terms.
5. Validate every block has a translation or preserved original.
6. Write translations into the original document structure.
7. Run QA and emit `review_report.json`.
8. Optionally export PDF preview with LibreOffice.

Future workflows should reuse this flow and swap only the task-specific planning and prompting layers.
