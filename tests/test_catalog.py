"""Behavioral guards for target semantics and honest result comparison."""

from __future__ import annotations

import copy
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from scripts.hub.catalog import load_catalog, rankable
from scripts.hub.render import GENERATED, _best, cell, check_local_links, render_all


ROOT = Path(__file__).resolve().parents[1]


def sandbox(tmp_path: Path, docs: bool = False) -> Path:
    for folder in ("schema", "datasets", "benchmarks"):
        shutil.copytree(ROOT / folder, tmp_path / folder)
    shutil.copy2(ROOT / "taxonomy.yaml", tmp_path / "taxonomy.yaml")
    if docs:
        shutil.copytree(ROOT / "scripts", tmp_path / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(ROOT / "docs", tmp_path / "docs")
        for filename in ("README.md", "CONTRIBUTING.md", "CHANGELOG.md", "CITATION.cff", "LICENSE", "LICENSE-CONTENT"):
            shutil.copy2(ROOT / filename, tmp_path / filename)
    return tmp_path


def edit_yaml(path: Path, change) -> None:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    change(data)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def test_seed_catalog_passes_all_declared_checks():
    catalog = load_catalog(ROOT)
    assert not catalog.errors, catalog.errors
    assert len(catalog.datasets) >= 15
    assert len(catalog.benchmarks) >= 3


def test_intention_probability_cannot_be_replaced_by_crossing_action(tmp_path):
    root = sandbox(tmp_path)
    path = root / "benchmarks/pie/pie-intention-loc-iccv2019.yaml"
    edit_yaml(path, lambda data: data.update(target_id="crossing_action"))
    assert any("annotation semantic 'future_action' does not match task 'intention_recognition'" in error for error in load_catalog(root).errors)


def test_different_split_is_separate_benchmark_and_duplicate_context_fails(tmp_path):
    root = sandbox(tmp_path)
    original = root / "benchmarks/pie/pie-intention-loc-iccv2019.yaml"
    clone = root / "benchmarks/pie/pie-intention-loc-alternative-split.yaml"
    data = yaml.safe_load(original.read_text(encoding="utf-8"))
    data["id"] = clone.stem
    data["split"]["name"] = "Alternative split"
    clone.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    assert not load_catalog(root).errors
    data["split"]["name"] = yaml.safe_load(original.read_text(encoding="utf-8"))["split"]["name"]
    clone.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    assert any("comparison context duplicates" in error for error in load_catalog(root).errors)


@pytest.mark.parametrize("change,expected", [
    (lambda b: b["results"][0]["scores"]["accuracy"].update(value=63), "outside finite valid range"),
    (lambda b: b["results"][0]["scores"]["accuracy"].update(locator={}), "should be non-empty"),
    (lambda b: b["temporal"]["observation_window"].update(kind="unknown"), "claimed confirmed and verified"),
    (lambda b: b["results"][0]["configuration"].update(ensemble=True), "claimed confirmed and verified"),
])
def test_invalid_comparison_conditions_fail(tmp_path, change, expected):
    root = sandbox(tmp_path)
    path = root / "benchmarks/pie/pie-intention-loc-iccv2019.yaml"
    edit_yaml(path, change)
    assert any(expected in error for error in load_catalog(root).errors)


def test_best_of_k_requires_exact_parameters():
    catalog = load_catalog(ROOT)
    b = copy.deepcopy(catalog.benchmarks["pie-intention-loc-iccv2019"])
    result = b["results"][0]
    b["evaluation"]["parameters"] = {"k": 5, "z": 20}
    result["configuration"]["evaluation_parameters"] = {"k": 3, "z": 20}
    assert not rankable(b, result)
    result["configuration"]["evaluation_parameters"]["k"] = 5
    assert rankable(b, result)


def test_metric_direction_ties_missing_scores_and_disputed_results():
    catalog = load_catalog(ROOT)
    b = copy.deepcopy(catalog.benchmarks["pie-intention-loc-iccv2019"])
    snapshot = b["snapshots"][0]
    accuracy = b["metrics"][0]
    f1 = b["metrics"][1]
    assert [r["id"] for r in _best(b, snapshot, accuracy)] == ["lstm_ed_loc"]
    b["results"][0]["scores"].pop("f1")
    assert [r["id"] for r in _best(b, snapshot, f1)] == ["lstm_ed_loc"]
    b["results"][0]["scores"]["accuracy"]["value"] = 0.67
    assert {r["id"] for r in _best(b, snapshot, accuracy)} == {"lstm_loc", "lstm_ed_loc"}
    accuracy["direction"] = "lower"
    assert len(_best(b, snapshot, accuracy)) == 2
    b["results"][0]["verification"]["status"] = "disputed"
    assert [r["id"] for r in _best(b, snapshot, accuracy)] == ["lstm_ed_loc"]
    b["results"][0]["verification"]["status"] = "verified"
    b["results"][0]["status"] = "withdrawn"
    assert [r["id"] for r in _best(b, snapshot, accuracy)] == ["lstm_ed_loc"]


def test_snapshot_result_set_does_not_expand_when_new_result_is_added():
    b = copy.deepcopy(load_catalog(ROOT).benchmarks["pie-intention-loc-iccv2019"])
    snapshot = b["snapshots"][0]
    newcomer = copy.deepcopy(b["results"][0])
    newcomer["id"] = "later_better"
    newcomer["scores"]["accuracy"]["value"] = 0.99
    b["results"].append(newcomer)
    assert [r["id"] for r in _best(b, snapshot, b["metrics"][0])] == ["lstm_ed_loc"]


def test_yaml_duplicate_keys_and_nonfinite_numbers_are_rejected(tmp_path):
    root = sandbox(tmp_path)
    path = root / "datasets/pie.yaml"
    path.write_text(path.read_text(encoding="utf-8") + "\nid: pie\n", encoding="utf-8")
    assert any("duplicate YAML key" in error for error in load_catalog(root).errors)
    shutil.copy2(ROOT / "datasets/pie.yaml", path)
    path.write_text(path.read_text(encoding="utf-8") + "\nnotes: .nan\n", encoding="utf-8")
    assert any("non-finite YAML number" in error for error in load_catalog(root).errors)


def test_render_is_stable_escapes_pipes_and_checks_anchors():
    catalog = load_catalog(ROOT)
    first, overview = render_all(catalog)
    second, second_overview = render_all(catalog)
    assert first == second and overview == second_overview
    assert cell("a | b\nnext") == "a \\| b<br>next"
    page = ROOT / "docs/benchmarks/pie.md"
    assert not check_local_links("[valid](docs/benchmarks/pie.md#pie-intention-loc-iccv2019)", ROOT / "README.md", first, ROOT)
    assert check_local_links("[bad](docs/benchmarks/pie.md#missing)", ROOT / "README.md", first, ROOT)


def test_generated_check_detects_stale_page(tmp_path):
    root = sandbox(tmp_path, docs=True)
    cmd = [sys.executable, str(root / "scripts/generate_docs.py"), "--check"]
    baseline = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    assert baseline.returncode == 0, baseline.stdout + baseline.stderr
    stale = root / "docs/datasets/stale.md"
    stale.write_text(GENERATED + "# Old page\n", encoding="utf-8")
    observed = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    assert observed.returncode == 1
    assert "stale generated page" in observed.stdout


def test_release_gate_counts_independent_method_families():
    script = ROOT / "scripts/check_release_gate.py"
    preview = subprocess.run([sys.executable, str(script), "--level", "preview"], cwd=ROOT, capture_output=True, text=True)
    reduced = subprocess.run([sys.executable, str(script), "--level", "reduced"], cwd=ROOT, capture_output=True, text=True)
    full = subprocess.run([sys.executable, str(script), "--level", "full"], cwd=ROOT, capture_output=True, text=True)
    assert preview.returncode == 0, preview.stdout + preview.stderr
    assert "pie" in preview.stdout and "jaad" in preview.stdout
    assert reduced.returncode == 0 and "intentqa" in reduced.stdout
    assert full.returncode == 1 and "count gate not met" in full.stdout


def test_github_issue_forms_are_valid_yaml_with_unique_fields():
    forms = list((ROOT / ".github/ISSUE_TEMPLATE").glob("*.yml"))
    assert len(forms) == 4
    for path in forms:
        form = yaml.safe_load(path.read_text(encoding="utf-8"))
        fields = [field["id"] for field in form["body"]]
        assert form["name"] and len(fields) == len(set(fields))
