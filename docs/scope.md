# Research scope and inclusion rules

Human intention here means an anticipated human action, desired outcome, destination, interaction purpose, or inference about such aims. We separate a person's intended outcome, preparation to act, and an action that later occurs. An observed future action can be a proxy for intention; it is not direct evidence of the person's internal state. Intention reasoning requires goal, motive, explanation, or relational evidence.

## Inclusion classes

| Class | Include when | Required qualification |
|---|---|---|
| `explicit` | A goal, intention, motive, or purpose is an annotation target. | State who assigned it: the person, an observer, an experimenter, or a derivation. |
| `implicit` | An original task predicts a future action, activity, or behavior. | Explain the behavior proxy and its limits. |
| `related` | An original source connects gaze, objects, motion, or another cue to intention modeling. | Cite the connection; do not claim an intention target. |

The class records why a dataset belongs here, not its quality. Benchmark files select an exact annotation target. A dataset with both intention and action labels may support several distinct benchmarks.

## Admission test

A verified entry needs an original paper or author/official resource; an operational intention definition; at least one grounded task or cue; checked access status; and traceable sources for core claims. Synthetic data needs an explicit human-intention or human-social-cognition purpose and must be labeled `synthetic` or `mixed`.

Exclude current-action classification collections without an anticipation, goal, or intention task; generic customer-service intent slots; agent-only policy data; unsourced collections; and data relabeled as intention without an author-backed rationale. A publication's use of the word ��intention�� is not sufficient.

## Borderline decisions

- A general action dataset becomes eligible when a specific, sourced anticipation protocol exists. The corresponding record is `implicit`.
- Future trajectory alone is normally `related`; a documented future-behavior or goal-prediction target may justify `implicit`.
- An endpoint-derived destination is marked `behavior_derived`, never described as a self-report.
- Observer-judged motives, such as image intent categories, may be `explicit` while remaining explicitly observer judgments.
- A goal conditioned robot policy is not by itself a human-intention task.
- Restricted or unavailable data can remain documented when access status is checked and stated.
- Ambiguous source terms such as ��action prediction�� retain the original name and receive a precise local task mapping.

The [PIE annotation documentation](https://github.com/aras62/PIE/blob/master/annotations/README.md) is a useful example: crossing intention and actual crossing are different targets and cannot share a result table.

