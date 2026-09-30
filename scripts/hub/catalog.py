"""Load YAML records and enforce cross-file research invariants."""

from __future__ import annotations

import datetime as dt
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


class UniqueSafeLoader(yaml.SafeLoader):
    pass


def _unique_mapping(loader: UniqueSafeLoader, node: yaml.MappingNode) -> dict:
    result: dict = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in result:
            raise ValueError(f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}")
        result[key] = loader.construct_object(value_node)
    return result


UniqueSafeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping)


@dataclass
class Catalog:
    root: Path
    taxonomy: dict[str, Any] = field(default_factory=dict)
    datasets: dict[str, dict[str, Any]] = field(default_factory=dict)
    methods: dict[str, dict[str, Any]] = field(default_factory=dict)
    benchmarks: dict[str, dict[str, Any]] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def error(self, path: Path | str, detail: str) -> None:
        location = str(path.relative_to(self.root)) if isinstance(path, Path) and path.is_relative_to(self.root) else str(path)
        self.errors.append(f"{location}: {detail}")


def _read_yaml(path: Path, catalog: Catalog) -> dict[str, Any] | None:
    try:
        with path.open(encoding="utf-8") as handle:
            value = yaml.load(handle, Loader=UniqueSafeLoader)
        if not isinstance(value, dict):
            raise ValueError("top-level YAML value must be a mapping")
        def reject_nonfinite(item: Any) -> None:
            if isinstance(item, float) and not math.isfinite(item):
                raise ValueError("non-finite YAML number (NaN or Infinity) is forbidden")
            if isinstance(item, dict):
                for child in item.values():
                    reject_nonfinite(child)
            elif isinstance(item, list):
                for child in item:
                    reject_nonfinite(child)
        reject_nonfinite(value)
        return value
    except (OSError, yaml.YAMLError, ValueError, TypeError) as exc:
        catalog.error(path, str(exc))
        return None


def _validate_schema(path: Path, data: dict, schema_name: str, catalog: Catalog) -> None:
    common = json.loads((catalog.root / "schema/common.schema.json").read_text(encoding="utf-8"))
    schema = json.loads((catalog.root / f"schema/{schema_name}.schema.json").read_text(encoding="utf-8"))
    schema["$defs"] = common["$defs"] | schema.get("$defs", {})
    for error in sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data), key=lambda e: str(list(e.path))):
        pointer = ".".join(map(str, error.path)) or "<root>"
        catalog.error(path, f"{pointer}: {error.message}")


def _ids(items: list[dict], catalog: Catalog, path: Path, field_name: str) -> set[str]:
    seen: set[str] = set()
    for item in items:
        identifier = item.get("id")
        if not isinstance(identifier, str):
            continue
        if identifier in seen:
            catalog.error(path, f"duplicate {field_name} id {identifier!r}")
        seen.add(identifier)
    return seen


def _check_source_refs(value: Any, allowed: set[str], catalog: Catalog, path: Path, prefix: str = "") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            location = f"{prefix}.{key}" if prefix else key
            if key == "source_ids" and isinstance(child, list):
                for source_id in child:
                    if source_id not in allowed:
                        catalog.error(path, f"{location}: unknown source {source_id!r}")
            elif key != "sources":
                _check_source_refs(child, allowed, catalog, path, location)
    elif isinstance(value, list):
        for number, child in enumerate(value):
            _check_source_refs(child, allowed, catalog, path, f"{prefix}[{number}]")


def _check_dates(value: Any, catalog: Catalog, path: Path, prefix: str = "") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            location = f"{prefix}.{key}" if prefix else key
            if key in {"checked_at", "accessed_at"} and isinstance(child, str):
                try:
                    if dt.date.fromisoformat(child) > dt.date.today():
                        catalog.error(path, f"{location}: future verification date")
                except ValueError:
                    pass
            else:
                _check_dates(child, catalog, path, location)
    elif isinstance(value, list):
        for number, child in enumerate(value):
            _check_dates(child, catalog, path, f"{prefix}[{number}]")


def _check_verifications(value: Any, catalog: Catalog, path: Path, prefix: str = "") -> None:
    if isinstance(value, dict):
        verification = value.get("verification")
        if isinstance(verification, dict) and verification.get("status") == "verified":
            sources = verification.get("source_ids", [])
            if not sources or not verification.get("checked_at"):
                catalog.error(path, f"{prefix or '<root>'}.verification: verified record needs a date and source")
        for key, child in value.items():
            _check_verifications(child, catalog, path, f"{prefix}.{key}" if prefix else key)
    elif isinstance(value, list):
        for number, child in enumerate(value):
            _check_verifications(child, catalog, path, f"{prefix}[{number}]")


def _check_taxonomy(catalog: Catalog) -> None:
    tax = catalog.taxonomy
    for group in ("domains", "intention_types", "tasks", "modalities", "data_formats", "viewpoints", "capture_setup"):
        terms = tax.get(group, {})
        for term, details in terms.items():
            parent = details.get("parent")
            if parent and parent not in terms:
                catalog.error("taxonomy.yaml", f"{group}.{term}: unknown parent {parent!r}")
            if parent and terms.get(parent, {}).get("parent"):
                catalog.error("taxonomy.yaml", f"{group}.{term}: hierarchy exceeds two levels")
    for dataset_id, data in catalog.datasets.items():
        path = catalog.root / "datasets" / f"{dataset_id}.yaml"
        for field_name, group in (("domains", "domains"), ("intention_types", "intention_types"), ("tasks", "tasks"), ("modalities", "modalities"), ("data_formats", "data_formats"), ("viewpoints", "viewpoints"), ("capture_setup", "capture_setup")):
            for term in data.get(field_name, []):
                if term not in tax.get(group, {}):
                    catalog.error(path, f"{field_name}: unknown taxonomy value {term!r}")
        if "other" in data.get("domains", []) and not data.get("notes"):
            catalog.error(path, "domains: 'other' requires notes")
        if data.get("intention_relevance") == "explicit" and not any(a.get("semantic") in {"intention", "goal", "explanation"} for a in data.get("annotations", [])):
            catalog.error(path, "explicit relevance requires an intention, goal or explanation annotation")
        if data.get("intention_relevance") == "implicit" and not any(a.get("semantic") in {"future_action", "trajectory"} for a in data.get("annotations", [])):
            catalog.error(path, "implicit relevance requires a future-action or trajectory target")
        if data.get("intention_relevance") == "related" and not data.get("notes"):
            catalog.error(path, "related relevance requires notes explaining the research link")


def _check_temporal(parameter: dict, catalog: Catalog, path: Path, label: str) -> None:
    if parameter.get("kind") == "range" and parameter.get("min", 0) > parameter.get("max", -1):
        catalog.error(path, f"{label}: min exceeds max")


def rankable(benchmark: dict, result: dict) -> bool:
    if benchmark.get("verification", {}).get("status") != "verified":
        return False
    if result.get("status") != "active" or result.get("verification", {}).get("status") != "verified" or result.get("protocol_match", {}).get("status") != "confirmed":
        return False
    if any(p.get("kind") == "unknown" for p in benchmark.get("temporal", {}).values()):
        return False
    if any(benchmark.get("training_policy", {}).get(field) == "unknown" for field in ("external_data", "pretraining", "extra_supervision")):
        return False
    if sorted(result.get("configuration", {}).get("modalities", [])) != sorted(benchmark.get("inputs", {}).get("modalities", [])):
        return False
    if result.get("configuration", {}).get("ensemble") and benchmark.get("training_policy", {}).get("ensemble") != "allowed":
        return False
    if benchmark.get("evaluation", {}).get("parameters", {}) != result.get("configuration", {}).get("evaluation_parameters", {}):
        return False
    return True


def _benchmark_signature(benchmark: dict) -> str:
    fields = ("dataset_id", "release_id", "annotation_version", "task", "target_id", "split", "sample_selection", "inputs", "temporal", "training_policy", "evaluation", "metrics")
    return json.dumps({field: benchmark.get(field) for field in fields}, sort_keys=True, ensure_ascii=False)


def _check_benchmarks(catalog: Catalog) -> None:
    signatures: dict[str, str] = {}
    allowed_targets = {
        "intention_recognition": {"intention"}, "intention_prediction": {"intention"},
        "intention_reasoning": {"intention", "goal", "explanation"},
        "goal_recognition": {"goal"}, "goal_prediction": {"goal"},
        "action_anticipation": {"future_action"}, "early_action_recognition": {"ongoing_action"},
        "future_activity_prediction": {"future_action"}, "behavior_prediction": {"future_action"},
        "trajectory_prediction": {"trajectory"},
        "human_object_interaction_prediction": {"future_action"},
    }
    for benchmark_id, item in catalog.benchmarks.items():
        path = catalog.root / "benchmarks" / item.get("dataset_id", "unknown") / f"{benchmark_id}.yaml"
        dataset = catalog.datasets.get(item.get("dataset_id"))
        if not dataset:
            catalog.error(path, "unknown dataset_id")
            continue
        if item.get("task") not in catalog.taxonomy.get("tasks", {}):
            catalog.error(path, f"unknown task {item.get('task')!r}")
        if item.get("task") not in dataset.get("tasks", []):
            catalog.error(path, "task is not listed in dataset")
        releases = {r.get("id"): r for r in dataset.get("releases", [])}
        release = releases.get(item.get("release_id"))
        if not release:
            catalog.error(path, "unknown release_id")
        elif item.get("annotation_version") != release.get("annotation_version"):
            catalog.error(path, "annotation_version differs from referenced release")
        annotations = {a.get("id"): a for a in dataset.get("annotations", [])}
        target = annotations.get(item.get("target_id"))
        if not target:
            catalog.error(path, "unknown target_id")
        elif target.get("semantic") == "cue":
            catalog.error(path, "a cue annotation cannot be the benchmark target")
        elif target.get("semantic") not in allowed_targets.get(item.get("task"), set()):
            catalog.error(path, f"target_id: annotation semantic {target.get('semantic')!r} does not match task {item.get('task')!r}")
        for modality in item.get("inputs", {}).get("modalities", []):
            if modality not in dataset.get("modalities", []):
                catalog.error(path, f"input modality {modality!r} is not available in dataset")
        for name, parameter in item.get("temporal", {}).items():
            if isinstance(parameter, dict):
                _check_temporal(parameter, catalog, path, f"temporal.{name}")
        metrics = _ids(item.get("metrics", []), catalog, path, "metric")
        results = _ids(item.get("results", []), catalog, path, "result")
        _ids(item.get("snapshots", []), catalog, path, "snapshot")
        methods = {m.get("id") for m in catalog.methods.get(item["dataset_id"], {}).get("methods", [])}
        for result in item.get("results", []):
            result_id = result.get("id", "<unknown>")
            if result.get("method_id") not in methods:
                catalog.error(path, f"result {result_id}: unknown method_id")
            if result.get("protocol_match", {}).get("status") == "mismatch":
                catalog.error(path, f"result {result_id}: mismatched protocol must be moved to another benchmark")
            if result.get("status") == "withdrawn" and not result.get("correction_note"):
                catalog.error(path, f"result {result_id}: withdrawn result requires correction_note")
            if result.get("status") == "active" and result.get("protocol_match", {}).get("status") == "confirmed" and result.get("verification", {}).get("status") == "verified" and not rankable(item, result):
                catalog.error(path, f"result {result_id}: claimed confirmed and verified but has unknown or inconsistent comparison context")
            for modality in result.get("configuration", {}).get("modalities", []):
                if modality not in catalog.taxonomy.get("modalities", {}):
                    catalog.error(path, f"result {result_id}: unknown modality {modality!r}")
            for metric_id, score in result.get("scores", {}).items():
                if metric_id not in metrics:
                    catalog.error(path, f"result {result_id}: unknown metric {metric_id!r}")
                    continue
                metric = next(m for m in item["metrics"] if m["id"] == metric_id)
                value = score.get("value")
                if isinstance(value, (int, float)) and (not math.isfinite(value) or ("valid_range" in metric and not metric["valid_range"][0] <= value <= metric["valid_range"][1])):
                    catalog.error(path, f"result {result_id}: {metric_id} outside finite valid range")
                if result.get("verification", {}).get("status") == "verified" and not score.get("locator"):
                    catalog.error(path, f"result {result_id}: verified score needs a source locator")
        for snapshot in item.get("snapshots", []):
            for result_id in snapshot.get("result_ids", []):
                if result_id not in results:
                    catalog.error(path, f"snapshot {snapshot.get('id')}: unknown result {result_id!r}")
                else:
                    result = next(r for r in item["results"] if r["id"] == result_id)
                    if snapshot.get("checked_at", "") < result.get("verification", {}).get("checked_at", ""):
                        catalog.error(path, f"snapshot {snapshot.get('id')}: checked before result {result_id} was verified")
            if snapshot.get("first_place_confirmed") and snapshot.get("scope") != "official_leaderboard":
                catalog.error(path, f"snapshot {snapshot.get('id')}: first place requires official leaderboard scope")
        signature = _benchmark_signature(item)
        if signature in signatures:
            catalog.error(path, f"comparison context duplicates {signatures[signature]}")
        signatures[signature] = benchmark_id


def load_catalog(root: Path) -> Catalog:
    root = root.resolve()
    catalog = Catalog(root)
    taxonomy_path = root / "taxonomy.yaml"
    catalog.taxonomy = _read_yaml(taxonomy_path, catalog) or {}
    if catalog.taxonomy:
        _validate_schema(taxonomy_path, catalog.taxonomy, "taxonomy", catalog)
    if catalog.errors:
        return catalog
    for path in sorted((root / "datasets").glob("*.yaml")):
        data = _read_yaml(path, catalog)
        if not data:
            continue
        before = len(catalog.errors)
        _validate_schema(path, data, "dataset", catalog)
        if len(catalog.errors) != before:
            continue
        dataset_id = data.get("id")
        if not isinstance(dataset_id, str):
            continue
        if path.stem != dataset_id:
            catalog.error(path, f"filename must be {dataset_id}.yaml")
        if dataset_id in catalog.datasets:
            catalog.error(path, f"duplicate dataset id {dataset_id}")
        catalog.datasets[dataset_id] = data
        if isinstance(data.get("year"), int) and data["year"] > dt.date.today().year:
            catalog.error(path, "year: first public year cannot be in the future")
        _ids(data.get("sources", []), catalog, path, "source")
        _ids(data.get("annotations", []), catalog, path, "annotation")
        _ids(data.get("releases", []), catalog, path, "release")
        allowed = {s.get("id") for s in data.get("sources", [])}
        _check_source_refs(data, allowed, catalog, path)
        _check_dates(data, catalog, path)
        _check_verifications(data, catalog, path)
        for statistic in data.get("statistics", []):
            if statistic.get("release_id") not in {r.get("id") for r in data.get("releases", [])}:
                catalog.error(path, f"statistic {statistic.get('name')}: unknown release_id")
    for path in sorted((root / "benchmarks").glob("*/methods.yaml")):
        data = _read_yaml(path, catalog)
        if not data:
            continue
        before = len(catalog.errors)
        _validate_schema(path, data, "method-catalog", catalog)
        if len(catalog.errors) != before:
            continue
        if path.parent.name != data.get("dataset_id") or data.get("dataset_id") not in catalog.datasets:
            catalog.error(path, "method catalog directory or dataset_id does not match an existing dataset")
        catalog.methods[data.get("dataset_id", path.parent.name)] = data
        _ids(data.get("methods", []), catalog, path, "method")
        _ids(data.get("sources", []), catalog, path, "source")
        _check_source_refs(data, {s.get("id") for s in data.get("sources", [])}, catalog, path)
        _check_dates(data, catalog, path)
    for path in sorted((root / "benchmarks").glob("*/*.yaml")):
        if path.name == "methods.yaml":
            continue
        data = _read_yaml(path, catalog)
        if not data:
            continue
        before = len(catalog.errors)
        _validate_schema(path, data, "benchmark", catalog)
        if len(catalog.errors) != before:
            continue
        benchmark_id = data.get("id")
        if not isinstance(benchmark_id, str):
            continue
        if path.stem != benchmark_id or path.parent.name != data.get("dataset_id"):
            catalog.error(path, "benchmark filename or directory does not match id/dataset_id")
        if benchmark_id in catalog.benchmarks:
            catalog.error(path, f"duplicate benchmark id {benchmark_id}")
        catalog.benchmarks[benchmark_id] = data
        _ids(data.get("sources", []), catalog, path, "source")
        _check_source_refs(data, {s.get("id") for s in data.get("sources", [])}, catalog, path)
        _check_dates(data, catalog, path)
        _check_verifications(data, catalog, path)
    if catalog.errors:
        return catalog
    for dataset_id, data in catalog.datasets.items():
        for related in data.get("related_datasets", []):
            if related not in catalog.datasets:
                catalog.error(root / "datasets" / f"{dataset_id}.yaml", f"unknown related dataset {related!r}")
    _check_taxonomy(catalog)
    _check_benchmarks(catalog)
    return catalog
