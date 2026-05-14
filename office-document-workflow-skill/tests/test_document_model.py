from scripts.core.document_model import LayoutMetadata, RiskFlags, StyleMetadata, TextBlock
from scripts.core.workflow import batch_blocks


def test_text_block_round_trip_dict():
    block = TextBlock(
        document_type="pptx",
        block_id="pptx:s0:shape1:p0:r0",
        slide_index=0,
        shape_id=1,
        paragraph_index=0,
        run_index=0,
        original_text="Hello",
        translated_text="Bonjour",
        style=StyleMetadata(font_name="Aptos", font_size=12, bold=True, bullet_level=1),
        layout=LayoutMetadata(x=1, y=2, width=3, height=4),
        risks=RiskFlags(is_table_text=True),
    )

    restored = TextBlock.from_dict(block.to_dict())

    assert restored == block
    assert restored.has_translation is True
    assert restored.risks.any() is True


def test_batch_blocks_respects_character_limit():
    blocks = [TextBlock(document_type="docx", block_id=str(i), original_text="x" * 4) for i in range(3)]

    batches = batch_blocks(blocks, max_chars=8)

    assert [[block.block_id for block in batch] for batch in batches] == [["0", "1"], ["2"]]
