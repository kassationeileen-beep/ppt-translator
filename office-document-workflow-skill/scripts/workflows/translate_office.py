"""Deterministic DOCX/PPTX translation workflow."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Optional

from scripts.core.document_model import TextBlock
from scripts.core.glossary import enforce_glossary_safe, load_glossary
from scripts.core.llm_provider import BaseLLMProvider, provider_from_name
from scripts.core.qa import run_qa
from scripts.core.utils import export_pdf_preview, write_json
from scripts.core.workflow import WorkflowResult, batch_blocks


def detect_document_type(path: str | Path) -> str:
    suffix = Path(path).suffix.lower()
    if suffix == ".pptx":
        return "pptx"
    if suffix == ".docx":
        return "docx"
    raise ValueError(f"Unsupported file type: {suffix}. Expected .pptx or .docx")


def adapter_for(path: str | Path):
    doc_type = detect_document_type(path)
    if doc_type == "pptx":
        from scripts.adapters.pptx_adapter import PptxAdapter

        return PptxAdapter(path)
    if doc_type == "docx":
        from scripts.adapters.docx_adapter import DocxAdapter

        return DocxAdapter(path)
    raise ValueError(f"Unsupported document type: {doc_type}")


def translate_blocks(
    blocks: Iterable[TextBlock],
    provider: BaseLLMProvider,
    source_lang: str,
    target_lang: str,
    glossary_terms,
    max_batch_chars: int = 6000,
) -> List[TextBlock]:
    translated: List[TextBlock] = []
    for batch in batch_blocks(blocks, max_chars=max_batch_chars):
        for block in batch:
            if not block.original_text.strip():
                block.translated_text = block.original_text
            elif block.risks.requires_manual_review:
                block.translated_text = block.original_text
            else:
                style_hint = _style_hint(block)
                result = provider.translate_text(
                    block.original_text,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    context={"block_id": block.block_id, **block.context},
                    glossary_terms=glossary_terms,
                    style_hint=style_hint,
                )
                block.translated_text = enforce_glossary_safe(block.original_text, result, glossary_terms)
            translated.append(block)
    missing = [block.block_id for block in translated if block.translated_text is None]
    if missing:
        raise RuntimeError(f"Translation missing for blocks: {missing}")
    return translated


def run_translation_workflow(
    input_path: str | Path,
    output_path: str | Path,
    source_lang: str,
    target_lang: str,
    glossary_path: Optional[str | Path] = None,
    review_report_path: str | Path = "review_report.json",
    provider_name: str = "mock",
    extracted_blocks_path: Optional[str | Path] = None,
    preview_dir: Optional[str | Path] = None,
) -> WorkflowResult:
    adapter = adapter_for(input_path)
    glossary_terms = load_glossary(glossary_path)
    provider = provider_from_name(provider_name)
    blocks = adapter.extract_text_blocks()
    if extracted_blocks_path:
        write_json(extracted_blocks_path, [block.to_dict() for block in blocks])
    translated_blocks = translate_blocks(blocks, provider, source_lang, target_lang, glossary_terms)
    adapter.write_translations(translated_blocks, output_path)
    report = run_qa(translated_blocks, source_lang, target_lang, glossary_terms)
    write_json(review_report_path, report.to_dict())
    preview_pdf = export_pdf_preview(output_path, preview_dir) if preview_dir else None
    return WorkflowResult(Path(output_path), Path(review_report_path), Path(extracted_blocks_path) if extracted_blocks_path else None, preview_pdf)


def _style_hint(block: TextBlock) -> str:
    hints = []
    if block.style.paragraph_style:
        hints.append(f"paragraph style: {block.style.paragraph_style}")
    if block.style.bullet_level is not None:
        hints.append(f"bullet level: {block.style.bullet_level}")
    if block.document_type == "pptx":
        hints.append("keep concise for slide layout")
    return "; ".join(hints) or "preserve source tone and formatting intent"
