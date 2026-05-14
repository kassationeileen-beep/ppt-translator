"""Common document model for script-controlled Office document workflows."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Literal, Optional

DocumentType = Literal["pptx", "docx"]


@dataclass
class StyleMetadata:
    """Formatting metadata captured when an adapter can read it."""

    font_name: Optional[str] = None
    font_size: Optional[float] = None
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    underline: Optional[bool] = None
    color: Optional[str] = None
    alignment: Optional[str] = None
    bullet_level: Optional[int] = None
    paragraph_style: Optional[str] = None


@dataclass
class LayoutMetadata:
    """Physical layout metadata, primarily for PPTX text boxes/shapes."""

    x: Optional[int] = None
    y: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None


@dataclass
class RiskFlags:
    """Flags that tell the workflow to preserve originals or request review."""

    is_chart_text: bool = False
    is_table_text: bool = False
    is_grouped_shape: bool = False
    is_smartart_or_unsupported: bool = False
    may_overflow: bool = False
    requires_manual_review: bool = False

    def any(self) -> bool:
        return any(asdict(self).values())


@dataclass
class TextBlock:
    """An editable text block extracted from a DOCX/PPTX file.

    The LLM is allowed to translate or rewrite ``original_text`` only. Adapters
    use the identifiers and metadata to write translated text back into the
    existing document structure.
    """

    document_type: DocumentType
    block_id: str
    original_text: str
    translated_text: Optional[str] = None
    slide_index: Optional[int] = None
    shape_id: Optional[int] = None
    paragraph_index: Optional[int] = None
    run_index: Optional[int] = None
    section_path: Optional[str] = None
    style: StyleMetadata = field(default_factory=StyleMetadata)
    layout: LayoutMetadata = field(default_factory=LayoutMetadata)
    risks: RiskFlags = field(default_factory=RiskFlags)
    context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TextBlock":
        payload = dict(data)
        payload["style"] = StyleMetadata(**payload.get("style", {}))
        payload["layout"] = LayoutMetadata(**payload.get("layout", {}))
        payload["risks"] = RiskFlags(**payload.get("risks", {}))
        return cls(**payload)

    @property
    def has_translation(self) -> bool:
        return self.translated_text is not None and self.translated_text != ""


@dataclass
class ReviewReport:
    """Serializable QA and review report."""

    summary: Dict[str, Any]
    counts_by_status: Dict[str, int]
    risky_blocks: List[Dict[str, Any]] = field(default_factory=list)
    glossary_mismatches: List[Dict[str, Any]] = field(default_factory=list)
    manual_review_items: List[Dict[str, Any]] = field(default_factory=list)
    issues: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
