#!/usr/bin/env python3
"""CLI entry point for office document workflows."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.workflows.translate_office import run_translation_workflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Office document workflow skill CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    translate = subparsers.add_parser("translate", help="Translate DOCX/PPTX while preserving structure")
    translate.add_argument("--input", required=True, help="Input .docx or .pptx file")
    translate.add_argument("--output", required=True, help="Translated output file")
    translate.add_argument("--source-lang", required=True, help="Source language code/name")
    translate.add_argument("--target-lang", required=True, help="Target language code/name")
    translate.add_argument("--glossary", help="CSV glossary with source,target,case_sensitive,notes")
    translate.add_argument("--review-report", default="review_report.json", help="Path for review_report.json")
    translate.add_argument("--provider", default="mock", choices=["mock", "openai", "openai-compatible"], help="LLM provider")
    translate.add_argument("--extracted-blocks", help="Optional path to save extracted_blocks.json")
    translate.add_argument("--preview-dir", help="Optional directory for LibreOffice PDF preview")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "translate":
        result = run_translation_workflow(
            input_path=args.input,
            output_path=args.output,
            source_lang=args.source_lang,
            target_lang=args.target_lang,
            glossary_path=args.glossary,
            review_report_path=args.review_report,
            provider_name=args.provider,
            extracted_blocks_path=args.extracted_blocks,
            preview_dir=args.preview_dir,
        )
        print(f"Translated file: {result.output_file}")
        print(f"Review report: {result.review_report}")
        if result.extracted_blocks:
            print(f"Extracted blocks: {result.extracted_blocks}")
        if result.preview_pdf:
            print(f"Preview PDF: {result.preview_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
