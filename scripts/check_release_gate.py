"""Count only independent, source-checked method families toward release gates.

This is a structural/count gate. The separate human source review in
docs/verification.md is mandatory before publishing a named release.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from hub.catalog import Catalog, load_catalog, rankable


THRESHOLDS = {"preview": (5, 2), "reduced": (15, 3), "full": (15, 5)}


def assess(catalog: Catalog) -> tuple[int, set[str]]:
    datasets = sum(d["verification"]["status"] == "verified" for d in catalog.datasets.values())
    complete: set[str] = set()
    for benchmark in catalog.benchmarks.values():
        if benchmark["verification"]["status"] != "verified":
            continue
        method_families = {m["id"]: m.get("model_family") for m in catalog.methods.get(benchmark["dataset_id"], {}).get("methods", [])}
        snapshot_ids = {result_id for snapshot in benchmark["snapshots"] for result_id in snapshot["result_ids"]}
        families = {method_families.get(result["method_id"]) for result in benchmark["results"] if result["id"] in snapshot_ids and rankable(benchmark, result)}
        families.discard(None)
        if len(families) >= 2:
            complete.add(benchmark["dataset_id"])
    return datasets, complete


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", choices=THRESHOLDS, default="preview")
    args = parser.parse_args()
    catalog = load_catalog(Path(__file__).resolve().parents[1])
    if catalog.errors:
        for error in catalog.errors:
            print(f"ERROR: {error}")
        return 1
    datasets, complete = assess(catalog)
    required_datasets, required_results = THRESHOLDS[args.level]
    passed = datasets >= required_datasets and len(complete) >= required_results
    print(f"{args.level}: {'count gate passed' if passed else 'count gate not met'}; verified datasets={datasets}/{required_datasets}; datasets with two independent, snapshot-backed method families={len(complete)}/{required_results} ({', '.join(sorted(complete)) or 'none'}).")
    print("A named release still requires a separate human review of source claims, access, and licenses.")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
