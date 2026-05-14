# PPTX Rules

- Use `python-pptx` for extraction and writeback.
- Extract text frames and table cell text where possible.
- Preserve slide index, shape id, paragraph index, and run index.
- Preserve run formatting, paragraph alignment, and bullet level metadata where available.
- Write translations into the original shapes/runs; do not recreate slides.
- Use per-shape font-size reduction only when overflow is likely.
- Never apply global scaling by default.
- Mark charts, SmartArt, embedded objects, images with text, and complex grouped shapes for manual review.
