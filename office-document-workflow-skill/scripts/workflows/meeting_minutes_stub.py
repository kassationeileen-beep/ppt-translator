"""Future workflow stub: meeting minutes generation.

Expected inputs:
- transcript or notes file
- optional agenda DOCX/PPTX template
- participants, date, meeting objective, target language/style

Expected outputs:
- structured minutes DOCX/PPTX produced by adapter-controlled writeback
- review_report.json with unresolved speakers, ambiguous action owners, and missing dates

Reuse plan:
- TextBlock captures editable template placeholders.
- llm_provider drafts concise block-level content only.
- workflow engine batches placeholders/sections.
- adapters write approved text into an existing template.
"""


def describe_workflow() -> dict:
    return {
        "name": "meeting_minutes",
        "status": "stub",
        "inputs": ["transcript", "agenda/template", "participants", "meeting metadata"],
        "outputs": ["minutes document", "review_report.json"],
        "reuses": ["document_model", "llm_provider", "workflow", "qa", "docx_adapter", "pptx_adapter"],
    }
