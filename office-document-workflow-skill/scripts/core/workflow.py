"""Reusable workflow engine primitives."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from .document_model import TextBlock


@dataclass
class WorkflowResult:
    output_file: Path
    review_report: Path
    extracted_blocks: Path | None = None
    preview_pdf: Path | None = None


def batch_blocks(blocks: Iterable[TextBlock], max_chars: int = 6000) -> List[List[TextBlock]]:
    batches: List[List[TextBlock]] = []
    current: List[TextBlock] = []
    current_chars = 0
    for block in blocks:
        size = len(block.original_text)
        if current and current_chars + size > max_chars:
            batches.append(current)
            current = []
            current_chars = 0
        current.append(block)
        current_chars += size
    if current:
        batches.append(current)
    return batches
