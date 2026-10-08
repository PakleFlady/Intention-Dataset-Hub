"""Validate all repository YAML and cross-file references."""

import os
from pathlib import Path

from hub.catalog import load_catalog


TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".py", ".toml", ".txt", ".cff"}
SKIP_DIRS = {".git", ".deps", ".venv", ".pytest_cache", ".pytest_tmp", "__pycache__"}


def encoding_errors(root: Path) -> list[str]:
    errors = []
    for directory, folders, files in os.walk(root):
        folders[:] = [folder for folder in folders if folder not in SKIP_DIRS]
        for name in files:
            path = Path(directory) / name
            if path.suffix not in TEXT_SUFFIXES and name not in {"LICENSE", "LICENSE-CONTENT"}:
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                errors.append(f"{path.relative_to(root)}: invalid UTF-8 at byte {exc.start}")
                continue
            for number, line in enumerate(content.splitlines(), 1):
                if "\ufffd" in line:
                    errors.append(f"{path.relative_to(root)}:{number}: Unicode replacement character U+FFFD")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    catalog = load_catalog(root)
    errors = catalog.errors + encoding_errors(root)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"Validation failed: {len(errors)} error(s).")
        return 1
    print(f"Validated {len(catalog.datasets)} datasets and {len(catalog.benchmarks)} benchmarks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
