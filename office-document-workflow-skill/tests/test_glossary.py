from pathlib import Path

from scripts.core.glossary import enforce_glossary_safe, find_glossary_mismatches, glossary_prompt, load_glossary
from scripts.core.llm_provider import MockLLMProvider


def test_load_glossary_and_prompt(tmp_path: Path):
    glossary = tmp_path / "glossary.csv"
    glossary.write_text("source,target,case_sensitive,notes\n客户,client,false,Preferred\nEBITDA,EBITDA,true,Acronym\n", encoding="utf-8")

    terms = load_glossary(glossary)

    assert len(terms) == 2
    assert terms[0].source == "客户"
    assert terms[0].case_sensitive is False
    assert "客户 => client" in glossary_prompt(terms)


def test_enforce_glossary_safe_replaces_lingering_source_term():
    terms = load_glossary(Path("config/glossary.sample.csv"))

    result = enforce_glossary_safe("客户增长", "[TRANSLATED] 客户 growth", terms)

    assert "client" in result
    assert "客户" not in result


def test_find_glossary_mismatches():
    terms = load_glossary(Path("config/glossary.sample.csv"))

    mismatches = find_glossary_mismatches("净收入 increased", "income increased", terms)

    assert [(term.source, term.target) for term in mismatches] == [("净收入", "net income")]


def test_mock_provider_prefixes_translation():
    provider = MockLLMProvider()

    assert provider.translate_text("Hello", "en", "zh") == "[TRANSLATED] Hello"
