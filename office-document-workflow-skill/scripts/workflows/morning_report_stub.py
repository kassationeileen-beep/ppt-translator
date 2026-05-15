"""Future workflow stub: Morning Report update.

Expected inputs:
- prior report DOCX/PPTX
- current market/company data pack
- sections to refresh and house style guidance

Expected outputs:
- updated report preserving the original template
- review_report.json covering stale data, missing sources, and manual-review items

Reuse plan:
- adapters extract report placeholders and narrative blocks.
- llm_provider rewrites only targeted blocks.
- workflow engine controls data-to-section mapping and QA.
"""


def describe_workflow() -> dict:
    return {
        "name": "morning_report",
        "status": "stub",
        "inputs": ["prior report", "data pack", "refresh scope", "style guidance"],
        "outputs": ["updated report", "review_report.json"],
        "reuses": ["document_model", "llm_provider", "workflow", "qa", "docx_adapter", "pptx_adapter"],
    }
