"""Glossary parsing and safe post-translation enforcement."""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional


@dataclass(frozen=True)
class GlossaryTerm:
    source: str
    target: str
    case_sensitive: bool = False
    notes: str = ""

    def source_in(self, text: str) -> bool:
        if self.case_sensitive:
            return self.source in text
        return self.source.lower() in text.lower()

    def target_in(self, text: str) -> bool:
        if self.case_sensitive:
            return self.target in text
        return self.target.lower() in text.lower()


def load_glossary(path: Optional[str | Path]) -> List[GlossaryTerm]:
    if not path:
        return []
    glossary_path = Path(path)
    if not glossary_path.exists():
        raise FileNotFoundError(f"Glossary not found: {glossary_path}")
    with glossary_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"source", "target", "case_sensitive", "notes"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Glossary missing columns: {sorted(missing)}")
        terms = []
        for row in reader:
            source = (row.get("source") or "").strip()
            target = (row.get("target") or "").strip()
            if not source or not target:
                continue
            case_sensitive = (row.get("case_sensitive") or "").strip().lower() in {"1", "true", "yes", "y"}
            terms.append(GlossaryTerm(source, target, case_sensitive, row.get("notes") or ""))
        return terms


def glossary_prompt(terms: Iterable[GlossaryTerm]) -> str:
    lines = []
    for term in terms:
        sensitivity = "case-sensitive" if term.case_sensitive else "case-insensitive"
        note = f" ({term.notes})" if term.notes else ""
        lines.append(f"- {term.source} => {term.target} [{sensitivity}]{note}")
    return "\n".join(lines)


def enforce_glossary_safe(source_text: str, translated_text: str, terms: Iterable[GlossaryTerm]) -> str:
    """Apply conservative replacements when source contains a glossary term.

    This does not attempt linguistic inflection. It only replaces lingering source
    terms in the translation with the target term.
    """
    result = translated_text
    for term in terms:
        if not term.source_in(source_text):
            continue
        flags = 0 if term.case_sensitive else re.IGNORECASE
        result = re.sub(re.escape(term.source), term.target, result, flags=flags)
    return result


def find_glossary_mismatches(source_text: str, translated_text: str, terms: Iterable[GlossaryTerm]) -> List[GlossaryTerm]:
    mismatches = []
    for term in terms:
        if term.source_in(source_text) and not term.target_in(translated_text):
            mismatches.append(term)
    return mismatches
