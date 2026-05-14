# Limitations

## PPTX

- Charts, SmartArt, embedded objects, images with text, and complex grouped shapes may require manual review.
- Overflow checks are approximate and do not replace human visual QA.
- Only per-shape fitting is allowed by default.

## DOCX

- Footnotes, comments, tracked changes, text boxes, complex fields, and cross-references are not fully supported in v1.
- Native Track Changes is not implemented in v1.

## LLM provider

- The OpenAI-compatible provider is a minimal stub. Production use should add retries, request logging, and stricter structured-output validation.
