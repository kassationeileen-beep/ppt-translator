"""Helpers for preserving readable boundaries between translated text runs."""
from __future__ import annotations

import re

_CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af]")
_OPENING_PUNCTUATION = set("([{<《〈“‘\"'")
_CLOSING_PUNCTUATION = set(")]}>,.!?:;，。！？：；、%‰》〉”’\"'")


def contains_cjk(text: str) -> bool:
    """Return True when text contains common CJK characters."""
    return bool(_CJK_RE.search(text))


def should_insert_space_between_runs(
    previous_original: str,
    current_original: str,
    previous_translated: str,
    current_translated: str,
) -> bool:
    """Decide whether two adjacent translated PPTX runs need a boundary space.

    Translation is performed at run granularity to preserve formatting. That can
    make CJK-to-English output look glued together when adjacent source runs are
    translated independently. This helper is deliberately conservative:

    - restore a source-space boundary if the provider stripped it;
    - add a CJK-to-Latin boundary when both translated sides are word-like;
    - avoid spaces around punctuation or when either side already has whitespace.
    """
    if not previous_translated or not current_translated:
        return False
    if previous_translated[-1].isspace() or current_translated[0].isspace():
        return False
    if current_translated[0] in _CLOSING_PUNCTUATION:
        return False
    if previous_translated[-1] in _OPENING_PUNCTUATION:
        return False

    source_had_boundary_space = bool(previous_original and previous_original[-1].isspace()) or bool(
        current_original and current_original[0].isspace()
    )
    translated_boundary_is_word_like = previous_translated[-1].isalnum() and current_translated[0].isalnum()
    if source_had_boundary_space and translated_boundary_is_word_like:
        return True

    source_boundary_was_cjk = contains_cjk(previous_original) or contains_cjk(current_original)
    return source_boundary_was_cjk and translated_boundary_is_word_like


def add_run_boundary_space_if_needed(
    previous_original: str,
    current_original: str,
    previous_translated: str,
    current_translated: str,
) -> str:
    """Prefix current translated run with one space when a readable boundary is needed."""
    if should_insert_space_between_runs(previous_original, current_original, previous_translated, current_translated):
        return f" {current_translated}"
    return current_translated
