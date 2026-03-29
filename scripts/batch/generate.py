"""
generate.py — Batch script generator

Generates submit/retrieve Python scripts from a batch.yaml config file
using Jinja2 templates.

Usage:
    python scripts/batch/generate.py batch.yaml
    python scripts/batch/generate.py batch.yaml --dry-run
    python scripts/batch/generate.py batch.yaml --output scripts/
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

# Ensure workspace root is on path so we can import scripts.batch
_WS_ROOT = pathlib.Path(__file__).parent.parent.parent
if str(_WS_ROOT) not in sys.path:
    sys.path.insert(0, str(_WS_ROOT))

import jinja2

from scripts.batch.config import BatchConfig


TEMPLATE_DIR = pathlib.Path(__file__).parent / "templates"


def _slugify(text: str) -> str:
    """Convert a name to a filename-safe slug."""
    slug = text.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[_\s]+", "-", slug)
    return slug


def generate_scripts(
    yaml_path: str | pathlib.Path,
    output_dir: pathlib.Path | None = None,
    dry_run: bool = False,
) -> dict[str, pathlib.Path]:
    """
    Generate submit and retrieve Python scripts from a batch.yaml config.

    Args:
        yaml_path:  Path to the batch.yaml file
        output_dir: Directory to write scripts into (default: yaml parent dir)
        dry_run:    If True, only print what would be generated

    Returns:
        Dict mapping script names to their output paths
    """
    yaml_path = pathlib.Path(yaml_path)
    config = BatchConfig.from_yaml(yaml_path)

    if output_dir is None:
        output_dir = yaml_path.parent

    slug = _slugify(config.name)
    submit_script_name = f"submit_{slug}.py"
    retrieve_script_name = f"retrieve_{slug}.py"

    yaml_relative = yaml_path.relative_to(output_dir)

    submit_template = (TEMPLATE_DIR / "batch_submit_script.py.j2").read_text(encoding="utf-8")
    retrieve_template = (TEMPLATE_DIR / "batch_retrieve_script.py.j2").read_text(encoding="utf-8")

    submit_content = jinja2.Template(submit_template).render(
        name=config.name,
        yaml_path=str(yaml_relative).replace("\\", "/"),
        batch_id_file=str(config.batch_id_path).replace("\\", "/"),
        script_path=submit_script_name,
        retrieve_script_name=retrieve_script_name,
    )

    retrieve_content = jinja2.Template(retrieve_template).render(
        name=config.name,
        yaml_path=str(yaml_relative).replace("\\", "/"),
        output_dir=str(config.output_dir).replace("\\", "/"),
        slugified_name=slug,
        script_path=retrieve_script_name,
    )

    outputs: dict[str, pathlib.Path] = {}

    if dry_run:
        print(f"[generate] === DRY RUN: would generate ===")
        print(f"  {output_dir / submit_script_name}")
        print(f"  {output_dir / retrieve_script_name}")
        print(f"[generate] === submit_{slug}.py (first 30 lines) ===")
        for i, line in enumerate(submit_content.splitlines()[:30], 1):
            print(f"  {i:3d}: {line}")
        print(f"[generate] === retrieve_{slug}.py (first 30 lines) ===")
        for i, line in enumerate(retrieve_content.splitlines()[:30], 1):
            print(f"  {i:3d}: {line}")
    else:
        out_submit = output_dir / submit_script_name
        out_retrieve = output_dir / retrieve_script_name

        out_submit.write_text(submit_content, encoding="utf-8")
        out_retrieve.write_text(retrieve_content, encoding="utf-8")

        print(f"[generate] Generated: {out_submit}")
        print(f"[generate] Generated: {out_retrieve}")

        import os
        os.chmod(out_submit, 0o755)
        os.chmod(out_retrieve, 0o755)

        outputs["submit"] = out_submit
        outputs["retrieve"] = out_retrieve

    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate batch submit/retrieve scripts from batch.yaml"
    )
    parser.add_argument(
        "yaml",
        help="Path to batch.yaml file",
    )
    parser.add_argument(
        "--output", "-o",
        type=pathlib.Path,
        default=None,
        help="Output directory (default: same directory as batch.yaml)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without writing files",
    )
    args = parser.parse_args()

    try:
        generate_scripts(args.yaml, output_dir=args.output, dry_run=args.dry_run)
        return 0
    except Exception as e:
        print(f"[generate] ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
