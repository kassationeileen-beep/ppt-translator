# Office Document Workflow Skill

Use this skill for DOCX/PPTX translation and future Office document workflows that must preserve a source file's structure and formatting.

## Non-negotiable operating rules

1. **Never recreate the document from scratch.** The LLM may translate or rewrite text blocks only.
2. **Always preserve original document structure.** Use adapters to write into existing paragraphs, runs, shapes, and tables.
3. **Always run extraction first.** Inspect extracted `TextBlock` records before writeback when debugging or handling complex files.
4. **Always use the script-controlled workflow.** Do not manually edit Office XML unless an adapter explicitly supports that operation.
5. **Always generate `review_report.json`.** The report is the audit trail for risky content and QA findings.
6. **Use glossary terms when provided.** Pass them to the LLM provider and run post-translation glossary QA.
7. **Use manual-review flags instead of guessing.** Charts, SmartArt, embedded objects, images with text, grouped shapes, footnotes, comments, tracked changes, and complex fields may need human review.
8. **For PPTX, use per-shape fitting only.** Use run-boundary spacing, per-shape/text-frame autofit, and local run font reduction for likely overflow; never apply global scaling unless the user explicitly asks.
9. **For DOCX, do not promise native Track Changes in v1.** Generate a review report with original vs. translated text instead.
10. **For very complex files, produce best effort output plus review report.** Preserve risky originals rather than corrupting layout.

## Primary workflow

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

DOCX is supported with the same command using `.docx` paths.

## Architecture

- `scripts/core/document_model.py`: common `TextBlock`, style/layout metadata, risk flags, and review report dataclasses.
- `scripts/adapters/pptx_adapter.py`: python-pptx extraction/writeback for text frames and tables; flags unsupported content.
- `scripts/adapters/docx_adapter.py`: python-docx extraction/writeback for body paragraphs, tables, headers, and footers.
- `scripts/core/llm_provider.py`: `BaseLLMProvider`, OpenAI-compatible provider, and deterministic mock provider.
- `scripts/workflows/translate_office.py`: deterministic translation workflow: detect, extract, translate, write back, QA, report.
- `scripts/workflows/*_stub.py`: future workflow placeholders that reuse the same model, provider, adapters, QA, and reports.

## Expected agent behavior

When given an Office translation request:

1. Install requirements if needed.
2. Run the CLI with `--extracted-blocks` for complex files.
3. Review `review_report.json` for missing translations, glossary mismatches, overflow risk, and manual-review items.
4. If LibreOffice is available and a visual preview is useful, pass `--preview-dir previews`.
5. Explain limitations and manual-review items to the user.
