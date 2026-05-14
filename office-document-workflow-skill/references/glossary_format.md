# Glossary Format

CSV columns:

```csv
source,target,case_sensitive,notes
```

- `source`: source-language term to detect in extracted blocks.
- `target`: required target-language rendering.
- `case_sensitive`: `true`/`false`, `yes`/`no`, or `1`/`0`.
- `notes`: optional guidance passed to the LLM prompt.

Glossary terms are passed to the LLM provider and checked after translation. Safe post-processing replaces leftover source terms with target terms when the source block contains the glossary source term.
