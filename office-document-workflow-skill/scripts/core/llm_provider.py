"""LLM provider abstraction for office workflows."""
from __future__ import annotations

import json
import os
import urllib.request
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, List, Optional

from .glossary import GlossaryTerm, glossary_prompt


class BaseLLMProvider(ABC):
    @abstractmethod
    def translate_text(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        context: Optional[Dict[str, Any]] = None,
        glossary_terms: Optional[Iterable[GlossaryTerm]] = None,
        style_hint: Optional[str] = None,
    ) -> str:
        """Translate one text block and return translated text only."""


class MockLLMProvider(BaseLLMProvider):
    """Deterministic provider for tests and dry runs."""

    def translate_text(self, text: str, source_lang: str, target_lang: str, context=None, glossary_terms=None, style_hint=None) -> str:
        return f"[TRANSLATED] {text}"


class OpenAICompatibleProvider(BaseLLMProvider):
    """Minimal OpenAI-compatible chat completions provider.

    Requires OPENAI_API_KEY. OPENAI_BASE_URL and OPENAI_MODEL are optional.
    """

    def __init__(self, model: Optional[str] = None, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
        self.base_url = (base_url or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is required for the OpenAI-compatible provider")

    def translate_text(self, text: str, source_lang: str, target_lang: str, context=None, glossary_terms=None, style_hint=None) -> str:
        terms = list(glossary_terms or [])
        system = (
            "You translate only the supplied text block. Preserve meaning, inline punctuation, "
            "numbers, placeholders, and formatting cues. Return JSON: {\"translation\": \"...\"}."
        )
        user = {
            "source_lang": source_lang,
            "target_lang": target_lang,
            "text": text,
            "context": context or {},
            "style_hint": style_hint or "preserve source tone and brevity",
            "glossary": glossary_prompt(terms),
        }
        body = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        }).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=body,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = json.loads(response.read().decode("utf-8"))
        content = payload["choices"][0]["message"]["content"]
        return json.loads(content)["translation"]


def provider_from_name(name: str) -> BaseLLMProvider:
    normalized = name.lower()
    if normalized == "mock":
        return MockLLMProvider()
    if normalized in {"openai", "openai-compatible"}:
        return OpenAICompatibleProvider()
    raise ValueError(f"Unknown provider: {name}")
