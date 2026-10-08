# Intention Dataset Hub

A curated, GitHub-native database of datasets and evaluation protocols for **human intention recognition, goal reasoning, and future behavior prediction**.

The organizing question is: **What does a person intend to do next, and why?** Each record explains what its labels actually mean. Future actions are useful proxies for intention, but they do not by themselves reveal a person's mental state.

We include three evidence-based classes: **explicit** intention or goal targets; **implicit** future action or behavior tasks; and **related** data that supplies a documented intention cue. The [scope and boundary rules](docs/scope.md) explain the distinction. A benchmark here is one comparison setting with a defined target, version, split, inputs, time window, training policy, and metric. Results from different settings are never silently ranked together.

<!-- hub:overview:start -->

**Verified datasets:** 34 | **Dataset families:** 32 | **Verified protocols:** 6 | **Datasets with at least two comparable results:** 4

## Featured datasets

| Dataset | Year | Domain | Relevance | Access |
| --- | --- | --- | --- | --- |
| [BDD-X](docs/datasets/bdd-x.md) | 2018 | driver_behavior, autonomous_driving | explicit | open |
| [CAMF industrial assembly study data (author-collected)](docs/datasets/camf-industrial-assembly.md) | 2026 | industrial_collaboration, human_robot_interaction | explicit | unknown |
| [DAAD-X](docs/datasets/daad-x.md) | 2025 | driver_behavior | explicit | open |
| [Aria Everyday Activities](docs/datasets/aria-everyday-activities.md) | 2024 | daily_activities, social_interaction | implicit | unknown |
| [Assembly101](docs/datasets/assembly101.md) | 2022 | daily_activities, human_object_interaction | implicit | open |
| [Brain4Cars](docs/datasets/brain4cars.md) | 2015 | driver_behavior, autonomous_driving | implicit | unknown |
| [Action Genome](docs/datasets/action-genome.md) | 2020 | daily_activities, human_object_interaction | related | open |
| [AIDE](docs/datasets/aide.md) | 2023 | driver_behavior | related | open |

[Complete dataset index](docs/datasets.md) | [By domain](docs/by-domain.md) | [By task](docs/by-task.md) | [By modality](docs/by-modality.md)

## Benchmark availability

| Dataset | Task | Protocol | Results | Snapshot checked |
| --- | --- | --- | --- | --- |
| [EPIC-KITCHENS-100](docs/datasets/epic-kitchens-100.md) | action_anticipation | [EK100 challenge test action anticipation](docs/benchmarks/epic-kitchens-100.md#ek100-2021-test-action-anticipation) | 0 | — |
| [Intentonomy](docs/datasets/intentonomy.md) | intention_recognition | [Author repository test-set RGB baseline cohort](docs/benchmarks/intentonomy.md#intentonomy-author-test-rgb) | 2 | 2026-09-30 |
| [IntentQA](docs/datasets/intentqa.md) | intention_reasoning | [ICCV 2023 BERT video-and-text no-GPT test cohort](docs/benchmarks/intentqa.md#intentqa-iccv2023-no-gpt-test) | 5 | 2026-09-30 |
| [JAAD](docs/datasets/jaad.md) | behavior_prediction | [WACV 2021 JAAD_all PCPA attention comparison](docs/benchmarks/jaad.md#jaad-all-wacv2021-pcpa) | 4 | 2026-09-30 |
| [JAAD](docs/datasets/jaad.md) | behavior_prediction | [WACV 2021 JAAD_all RGB 3D convolution comparison](docs/benchmarks/jaad.md#jaad-all-wacv2021-rgb3d) | 2 | 2026-09-30 |
| [PIE](docs/datasets/pie.md) | intention_recognition | [PIE ICCV 2019 intention estimation, location-only inputs](docs/benchmarks/pie.md#pie-intention-loc-iccv2019) | 2 | 2026-09-30 |

[Complete benchmark index](docs/benchmarks.md)

<!-- hub:overview:end -->

## How to use this repository

Start at the dataset index to see an input/output example, an author-published visual or demo where available, the target, and its annotation provenance. Examples marked illustrative show the task shape and are not claimed to be copied dataset rows. Open a benchmark page to inspect the protocol and verified result sources. The baseline section favors original baselines and available author code; a code link does not imply that this project reproduced the result.

Best-result labels are restricted to the result set and date shown in their snapshot. Empty or incomplete leaderboards are stated plainly.

## Contribute and verify

See [CONTRIBUTING.md](CONTRIBUTING.md) for adding a dataset, protocol, result, or correction. Run:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python scripts/check_release_gate.py --level preview
python scripts/generate_docs.py
python scripts/generate_docs.py --check
python -m pytest
```

The [data model](docs/data-model.md), [taxonomy](docs/taxonomy.md), and [verification policy](docs/verification.md) describe the evidence standard. Automated validation checks structure and declared comparisons; original-source review remains essential.

## Status, citation, and licenses

This is a research preview while the seed collection and protocol coverage are under review. Counts above reflect only verified YAML entries; they are not release claims. See [CHANGELOG.md](CHANGELOG.md) for current gaps.

The [coverage and release-gate notes](docs/coverage.md) identify incomplete independent-method comparisons and the remaining second-pass research review.

Please cite this repository via [CITATION.cff](CITATION.cff) and cite each original dataset and method used in your research. Code is MIT licensed ([LICENSE](LICENSE)); original curation and documentation are CC BY 4.0 ([LICENSE-CONTENT](LICENSE-CONTENT)). Linked datasets, papers, and repositories retain their own terms.
