# Contributing

Thank you for improving the source record. Please make one evidence-backed change per pull request when possible. The [scope](docs/scope.md), [data model](docs/data-model.md), and [verification policy](docs/verification.md) govern all additions.

## Add a dataset

Copy [the dataset template](templates/dataset.yaml) to `datasets/<stable-kebab-id>.yaml`. Provide the original paper or author project, a precise intention definition, annotation meaning and provenance, a release ID, access status, component license status, and source locators. `unknown` license or restricted access is acceptable when stated honestly. Do not infer missing counts. Add a new taxonomy value only when existing terms cannot describe the dataset, and explain the boundary in the PR.

## Add a benchmark or result

Start from [the benchmark template](templates/benchmark.yaml). Define the exact label target, release, annotation version, split, sample selection, inputs, time windows, training rules, evaluation, and metrics before entering any score. A distinct experimental setting requires a distinct benchmark file. Add method identity to the dataset's `methods.yaml`; put the actual configuration and score source on the result. The source locator should identify a paper table and row, official leaderboard entry, or equivalent original location.

For a baseline, cite the dataset or protocol authors' designation. Code availability and training/evaluation instructions are separate fields. Avoid permanent `sota` labels: the generator computes best included results within a dated snapshot.

**Never compare numbers from different evaluation protocols in one ranked table.** Do not upgrade `pending` or `unclear` to `verified` or `confirmed` without inspecting the original source. An error correction should explain what changed and preserve the earlier result as withdrawn if already public.

## Local checks

Use Python 3.12 or later:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python scripts/check_release_gate.py --level preview
python scripts/generate_docs.py
python scripts/generate_docs.py --check
python -m pytest
```

Commit both YAML and generated Markdown. CI compares them and checks local links. Network errors in external resources should be reported in a Broken Link issue rather than silently changing access status.
# Model categories and bilingual overview

Every Result must include `model_class` and `classification_notes` supported by its source configuration. See [classification rules](docs/model-classification.md). Conventional, LLM/VLM and training-assisted hybrid results have separate winner calculations; unknown categories cannot rank. Keep zero-shot, SFT and multi-task IT protocols separate.

`README.md` is the Chinese landing page and `README.en.md` is the English version. Edit their introductory prose directly; regenerate both overview blocks with `python scripts/generate_docs.py`. Do not translate stable YAML IDs or link anchors. Keep media archives and local playback outputs out of contributions; see [media policy](docs/media-policy.md).

