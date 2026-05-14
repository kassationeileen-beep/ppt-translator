# office-document-workflow-skill

An AI-executable skill and script framework for Office document translation and future document workflows. The initial implementation supports DOCX and PPTX translation while preserving document structure and formatting as much as possible.

## Philosophy

Do **not** let an LLM recreate a document. The LLM translates or rewrites extracted text blocks only. Python scripts control extraction, structure preservation, writeback, QA, and optional preview export.

## Setup

```bash
cd office-document-workflow-skill
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

LibreOffice is optional. If `soffice` or `libreoffice` is available, the CLI can export DOCX/PPTX outputs to PDF previews.

## Usage

PPTX translation with glossary and mock provider:

```bash
python scripts/cli.py translate \
  --input input.pptx \
  --output translated.pptx \
  --source-lang zh \
  --target-lang en \
  --glossary config/glossary.sample.csv \
  --review-report review_report.json \
  --provider mock
```

DOCX translation:

```bash
python scripts/cli.py translate \
  --input input.docx \
  --output translated.docx \
  --source-lang en \
  --target-lang zh \
  --provider mock
```

Useful optional flags:

- `--extracted-blocks extracted_blocks.json`: save extracted `TextBlock` records for debugging.
- `--preview-dir previews`: export a PDF preview if LibreOffice is installed.
- `--provider openai`: use an OpenAI-compatible provider with `OPENAI_API_KEY` from the environment.

## What gets created

The workflow produces:

1. translated Office file (`.docx` or `.pptx`),
2. `review_report.json`,
3. optional `extracted_blocks.json`,
4. optional PDF preview.

## Architecture

- `scripts/core/document_model.py`: shared dataclasses for extracted text blocks, style metadata, layout metadata, risk flags, and reports.
- `scripts/core/llm_provider.py`: `BaseLLMProvider`, mock provider, and OpenAI-compatible provider stub.
- `scripts/core/glossary.py`: glossary CSV loading, prompt formatting, safe enforcement, and mismatch detection.
- `scripts/core/qa.py`: missing translation, unchanged translation, glossary, long text, PPTX overflow, and unsupported-content checks.
- `scripts/adapters/pptx_adapter.py`: PPTX extraction/writeback using python-pptx.
- `scripts/adapters/docx_adapter.py`: DOCX extraction/writeback using python-docx.
- `scripts/workflows/translate_office.py`: deterministic translation workflow.
- `scripts/workflows/*_stub.py`: future workflow stubs for meeting minutes, morning report, and FA deck/teaser drafting.

## Current limitations

- PPTX charts, SmartArt, embedded objects, images with text, and complex grouped shapes may require manual review.
- PPTX overflow detection is heuristic. The adapter only performs per-shape font reduction when likely overflow is detected and never applies global scaling by default.
- DOCX footnotes, comments, tracked changes, text boxes, complex fields, and cross-references are not fully supported in v1.
- Native DOCX Track Changes is not implemented in v1. Use `review_report.json` to compare original and translated text.
- The OpenAI-compatible provider is intentionally minimal; production deployments should add retry/backoff, telemetry, and stricter structured-output validation.

## What to implement next

- End-to-end fixture tests that create real DOCX/PPTX files and validate writeback.
- Richer PPTX shape traversal and better grouped-shape handling.
- More robust DOCX support for footnotes, comments, fields, and text boxes.
- Batch structured LLM calls that return JSON for multiple block IDs at once.
- Visual regression checks using exported PDF previews.
- Fully implemented future workflows for meeting minutes, morning reports, FA teasers/decks, and IC memos.
