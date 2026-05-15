# PPTX Rules

- Use `python-pptx` for extraction and writeback.
- Extract text frames and table cell text where possible.
- Preserve slide index, shape id, paragraph index, and run index.
- Preserve run formatting, paragraph alignment, and bullet level metadata where available.
- Write translations into the original shapes/runs; do not recreate slides.
- Use per-shape font-size reduction only when overflow is likely; shrink affected paragraph runs, not the whole deck.
- Enable per-shape/text-frame autofit for shapes or table cells whose translated text is likely to overflow.
- Preserve readable boundaries between adjacent translated runs; CJK-to-Latin run boundaries may need an inserted space.
- Never apply global scaling by default.
- Mark charts, SmartArt, embedded objects, images with text, and complex grouped shapes for manual review.
