from scripts.core.text_spacing import add_run_boundary_space_if_needed, should_insert_space_between_runs


def test_inserts_space_for_cjk_to_latin_run_boundary():
    assert should_insert_space_between_runs("客户", "增长", "Client", "Growth") is True
    assert add_run_boundary_space_if_needed("客户", "增长", "Client", "Growth") == " Growth"


def test_preserves_existing_space_or_punctuation_boundaries():
    assert should_insert_space_between_runs("客户", "增长", "Client ", "Growth") is False
    assert should_insert_space_between_runs("客户", "。", "Client", ".") is False


def test_does_not_split_plain_latin_runs_without_source_boundary():
    assert should_insert_space_between_runs("Inter", "national", "Inter", "national") is False
