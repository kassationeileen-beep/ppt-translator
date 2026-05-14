"""Future workflow stub: FA teaser/deck drafting.

Expected inputs:
- source company facts and financials
- house PPTX/DOCX template
- transaction context and compliance constraints

Expected outputs:
- first-draft teaser/deck with template formatting preserved
- review_report.json covering unsupported objects, source gaps, and compliance flags

Reuse plan:
- document_model represents template text placeholders.
- llm_provider drafts block-level language.
- workflow engine manages section order and review gates.
- adapters write back to the existing template rather than recreating slides/pages.
"""


def describe_workflow() -> dict:
    return {
        "name": "fa_deck",
        "status": "stub",
        "inputs": ["company facts", "financials", "template", "transaction context"],
        "outputs": ["draft teaser/deck", "review_report.json"],
        "reuses": ["document_model", "llm_provider", "workflow", "qa", "docx_adapter", "pptx_adapter"],
    }
