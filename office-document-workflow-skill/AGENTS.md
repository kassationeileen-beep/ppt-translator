# Agent Guide

## Run tests

```bash
python -m pytest tests
```

## Run the CLI

```bash
python scripts/cli.py translate --help
python scripts/cli.py translate \
  --input input.docx \
  --output translated.docx \
  --source-lang en \
  --target-lang zh \
  --provider mock \
  --review-report review_report.json
```

Run commands from the `office-document-workflow-skill/` directory so imports resolve consistently.

## Add a new workflow

1. Add a module under `scripts/workflows/`.
2. Reuse `TextBlock` and `ReviewReport` from `scripts/core/document_model.py`.
3. Use adapters for extraction/writeback; do not recreate Office files from scratch.
4. Use `BaseLLMProvider` for all LLM calls.
5. Produce a deterministic review report for QA and manual review.
6. Add tests for workflow-specific parsing, validation, and edge cases.

## Coding principles

- LLMs rewrite text only; Python controls structure, extraction, writeback, QA, and export.
- Preserve the original document unless an adapter has explicit support to change it.
- Prefer conservative manual-review flags to risky automated edits.
- Do not hardcode secrets. API keys come from environment variables.
- Keep the mock provider deterministic for tests.

## Known pitfalls

- PPTX charts, SmartArt, embedded objects, images with text, and complex grouped shapes are not reliably editable.
- PPTX overflow detection is heuristic; use visual review for important decks.
- DOCX footnotes, comments, tracked changes, text boxes, complex fields, and cross-references are documented limitations in v1.
- Native DOCX Track Changes is not implemented in v1; use `review_report.json`.
