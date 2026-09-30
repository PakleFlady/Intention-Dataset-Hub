"""Validate all repository YAML and cross-file references."""

from pathlib import Path

from hub.catalog import load_catalog


def main() -> int:
    catalog = load_catalog(Path(__file__).resolve().parents[1])
    for error in catalog.errors:
        print(f"ERROR: {error}")
    if catalog.errors:
        print(f"Validation failed: {len(catalog.errors)} error(s).")
        return 1
    print(f"Validated {len(catalog.datasets)} datasets and {len(catalog.benchmarks)} benchmarks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
