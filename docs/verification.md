# Source verification policy

Prefer an official leaderboard for official ranking, an original paper and supplement for paper scores, and official code or benchmark documentation for protocol details. A blog, aggregator, or model recollection may point to candidates; it is not enough to verify a result. Every score needs a source locator that enables a quick manual recheck.

Record access dates from actual review. Automated document generation does not refresh them. `verified` confirms agreement with the cited source only. It does not assert successful downloading, model execution, independent reproduction, or complete literature coverage.

Before accepting a result, compare its target label, dataset and annotation version, split, sample filter, input modalities, observed information, temporal parameters, external data, pretraining, extra supervision, evaluation code or definition, and metric aggregation. Unclear results may be kept as unranked records. A known mismatch belongs in another protocol or a correction issue.

Keep official-leaderboard snapshots separate from paper-reported snapshots. Show the checked date and search coverage. Retain baseline and representative entries even when they are no longer the best included result. Source conflicts remain visible until resolved from primary evidence.

Review core benchmarks quarterly and access/license information every six months as a maintenance target. A link-check failure alone is evidence to investigate, not proof of dataset withdrawal.

