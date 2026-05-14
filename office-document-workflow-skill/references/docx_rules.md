# DOCX Rules

- Use `python-docx` for extraction and writeback.
- Extract body paragraphs, runs, headings, tables, headers, and footers where feasible.
- Preserve paragraph styles, run styles, bullets/numbering metadata, and table structure where feasible.
- Write translations into existing runs/paragraphs; do not recreate the document.
- Do not implement or promise native Track Changes in v1.
- Generate `review_report.json` showing QA status and review items.
- Document limitations around footnotes, comments, tracked changes, text boxes, complex fields, and cross-references.
