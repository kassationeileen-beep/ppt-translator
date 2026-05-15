"""Quality checks and review-report generation."""
from __future__ import annotations

from collections import Counter
from typing import Iterable, List

from .document_model import ReviewReport, TextBlock
from .glossary import GlossaryTerm, find_glossary_mismatches


def likely_pptx_overflow(block: TextBlock, ratio_threshold: float = 1.8) -> bool:
    if block.document_type != "pptx" or not block.translated_text:
        return False
    if not block.original_text:
        return False
    length_ratio = len(block.translated_text) / max(len(block.original_text), 1)
    if length_ratio > ratio_threshold:
        return True
    if block.layout.width and block.layout.height and block.style.font_size:
        rough_capacity = max((block.layout.width / 914400) * (block.layout.height / 914400) * 55 / max(block.style.font_size / 12, 0.5), 20)
        return len(block.translated_text) > rough_capacity
    return False


def run_qa(blocks: Iterable[TextBlock], source_lang: str, target_lang: str, glossary_terms: Iterable[GlossaryTerm]) -> ReviewReport:
    block_list = list(blocks)
    terms = list(glossary_terms)
    issues = []
    risky_blocks = []
    glossary_mismatches = []
    manual_review_items = []
    counts = Counter()

    for block in block_list:
        block_issues = []
        translated = block.translated_text or ""
        if not translated:
            block_issues.append("missing_translation")
        if source_lang != target_lang and translated.strip() == block.original_text.strip() and block.original_text.strip():
            block_issues.append("unchanged_translation")
        if block.original_text and translated and len(translated) > max(80, len(block.original_text) * 2.5):
            block_issues.append("translation_much_longer")
        if likely_pptx_overflow(block):
            block.risks.may_overflow = True
            block_issues.append("pptx_likely_overflow")
        mismatches = find_glossary_mismatches(block.original_text, translated, terms)
        for term in mismatches:
            glossary_mismatches.append({"block_id": block.block_id, "source": term.source, "target": term.target})
            block_issues.append("glossary_mismatch")
        if block.risks.any():
            risky_blocks.append(block.to_dict())
        if block.risks.requires_manual_review or block.risks.is_smartart_or_unsupported or block.risks.is_chart_text:
            manual_review_items.append(block.to_dict())
            block_issues.append("manual_review_required")
        if block_issues:
            counts["needs_review"] += 1
            issues.append({"block_id": block.block_id, "issues": sorted(set(block_issues))})
        else:
            counts["ok"] += 1

    counts["total"] = len(block_list)
    summary = {
        "total_blocks": len(block_list),
        "ok_blocks": counts["ok"],
        "needs_review_blocks": counts["needs_review"],
        "source_lang": source_lang,
        "target_lang": target_lang,
    }
    return ReviewReport(summary, dict(counts), risky_blocks, glossary_mismatches, manual_review_items, issues)
