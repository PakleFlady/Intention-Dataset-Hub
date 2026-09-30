# Data model

Dataset, method, and benchmark facts live only in YAML. [JSON Schemas](../schema/) check field structure, and [taxonomy.yaml](../taxonomy.yaml) is the controlled vocabulary. Generated indexes and detail pages are projections of the YAML.

## Dataset

Each `datasets/<id>.yaml` documents one identifiable release. Required fields describe identity, publication year, intention meaning, relevance, domains, types, tasks, formats, modalities, origin, annotations, releases, access, component licenses, sources, and verification. Optional statistics always carry a unit, release, scope, and source. Omit unknown statistics instead of using zero.

`annotations` identify the target used by a benchmark. `semantic` records what the label represents; `provenance` records how it was obtained. For example, an observer judgment of intention has `semantic: intention` and `provenance: observer_judgment`. `releases` give the exact data and annotation version referenced by a benchmark.

## Benchmark

Each `benchmarks/<dataset-id>/<benchmark-id>.yaml` defines one comparison context: release and annotation version, exact target, task, split, sample selection, available inputs, time windows, training constraints, evaluation, and metrics. Any material difference calls for a separate benchmark. Method identities are reused within that dataset through `methods.yaml`; experiment configuration remains on each result.

`model_family` groups closely related ablations for release-gate counting. The gate requires two distinct method families in a protocol snapshot; a table with four variants of one architecture does not count as four independent baselines. This is a conservative count aid, not a substitute for source review.

`observation_window` describes the observed past; `anticipation_gap` separates the last observed moment from a future action; `prediction_horizon` describes the requested future. Fixed values have a unit, value, and anchor; frame-based timing also needs frame rate. `unknown` differs from `not_applicable`. Results under an unknown required setting cannot be ranked.

Each metric defines its unit, direction, aggregation, and evaluation subset. Overall and tail-class scores, percentages and fractions, and different best-of-K settings are distinct. Each result score points to a primary source and a table, row, entry, or other locator. Missing scores stay missing.

## Verification and snapshots

`verified` means checked against the specified original source, not independently reproduced. A rankable result is active, verified, protocol matched, and has complete comparison context. A snapshot freezes a named set of result IDs and a real checking date. Official first place is claimed only when the exact official leaderboard scope and first entry were checked. Paper-reported best means best among the verified results found in that snapshot.

Results and snapshots are append-oriented. Correct an error with an explanatory correction and preserve the Git history. Publication year is not the date a method became best.
