"""Generate or check the GitHub Markdown projection of YAML facts."""

import argparse
from pathlib import Path

from hub.catalog import load_catalog
from hub.render import GENERATED, check_local_links, render_all, update_readme


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if committed documentation differs from generated output")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    catalog = load_catalog(root)
    if catalog.errors:
        for error in catalog.errors:
            print(f"ERROR: {error}")
        return 1
    output, overview = render_all(catalog)
    readme_path = root / "README.md"
    try:
        readme = update_readme(readme_path.read_text(encoding="utf-8"), overview)
    except (OSError, ValueError) as exc:
        print(f"ERROR: README.md: {exc}")
        return 1
    output[readme_path] = readme
    failures = []
    for path, content in output.items():
        failures.extend(check_local_links(content, path, output, root))
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                failures.append(f"{path.relative_to(root)}: generated content differs")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    managed = {root / "docs/datasets.md", root / "docs/benchmarks.md", root / "docs/by-domain.md", root / "docs/by-task.md", root / "docs/by-modality.md", root / "docs/taxonomy.md"}
    managed.update((root / "docs/datasets").glob("*.md"))
    managed.update((root / "docs/benchmarks").glob("*.md"))
    for path in managed - output.keys():
        if path.exists() and path.read_text(encoding="utf-8").startswith(GENERATED):
            if args.check:
                failures.append(f"{path.relative_to(root)}: stale generated page")
            else:
                path.unlink()
    for failure in failures:
        print(f"ERROR: {failure}")
    if failures:
        return 1
    print(f"{'Checked' if args.check else 'Generated'} {len(output) - 1} Markdown pages and README overview.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
