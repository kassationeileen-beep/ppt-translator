"""Utility helpers for file IO and optional PDF preview export."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


def write_json(path: str | Path, data: Any) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def export_pdf_preview(input_path: str | Path, output_dir: str | Path) -> Path | None:
    """Export DOCX/PPTX to PDF with LibreOffice when available."""
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        return None
    input_file = Path(input_path)
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(target_dir), str(input_file)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return target_dir / f"{input_file.stem}.pdf"
