# PDF-derived curation, 2026-10-08

This batch adds 18 records and supplements five existing records. The catalog now has 34 datasets. Public original papers and author resources support the records; private library paths and PDF copies are not published. The [scope](scope.md) and [verification policy](verification.md) apply. Source-checked descriptions do not imply reproduced experiments, guaranteed downloads, or a completed independent release review.

## Admission decisions

| Paper or evidence path | Catalog additions or existing records | Reason and boundary |
| --- | --- | --- |
| [Context relationships / STGAIN](https://doi.org/10.1016/j.eswa.2024.126147) | [DSG](datasets/dsg.md), [Action Genome](datasets/action-genome.md) | Script-derived intention categories and their graph cue source. Graph CSVs exist; paper-corpus completeness and label mapping remain unresolved. |
| [Explainable driver prediction](https://arxiv.org/abs/2510.09200) | [DAAD-X](datasets/daad-x.md), [DAAD](datasets/daad.md) | Separate source corpus and explanation extension. Observer reasons and future maneuvers have distinct semantics. |
| Same driving comparison context, checked against original author resources | [VIENA2](datasets/viena2.md), [HDD](datasets/hdd.md), [AIDE](datasets/aide.md), [BDD-X](datasets/bdd-x.md), [DR(eye)VE](datasets/dreyeve.md) | Future-action data, motive explanations, or documented behavior/context/gaze cues. HDD, AIDE and DR(eye)VE have no intention benchmark asserted here. |
| [CAMF](https://arxiv.org/abs/2609.10339) | [Industrial assembly study](datasets/camf-industrial-assembly.md) | Experiment-instructed component goal; recognition after reach onset is explicitly early action recognition. Distribution is unknown. |
| [Visual planning](https://arxiv.org/abs/2507.15130) | [EPIC-KITCHENS-55](datasets/epic-kitchens-55.md), [COIN](datasets/coin.md), [CrossTask](datasets/crosstask.md) | Dataset sources checked separately. Future-step protocols justify instructional corpus admission; the 2018 EPIC release has its own original anticipation task. |
| [Action Anticipation at a Glimpse](https://arxiv.org/abs/2512.02846) | [IKEA ASM](datasets/ikea-asm.md), [MECCANO](datasets/meccano.md); existing Assembly101 | Anticipation evidence without pretending native action labels are mental states. No protocol-mismatched scores imported. |
| [PAR-VLA](https://openaccess.thecvf.com/content/CVPR2026/papers/Shao_Prototypical_Action_Reasoning_Facilitated_by_Vision-Language_Alignment_for_Egocentric_Action_CVPR_2026_paper.pdf) | [50 Salads](datasets/fifty-salads.md); existing EPIC-KITCHENS-100 and EGTEA | Future action targets with study-specific temporal selection and vocabularies. |
| [EgoAdapt](https://arxiv.org/abs/2506.21080) | [Aria Everyday Activities](datasets/aria-everyday-activities.md) | Downstream behavior anticipation; semantic intention labels and exact temporal benchmark mapping remain unestablished. |
| [STEP](https://arxiv.org/abs/2608.27225) | [Extended block assembly data](datasets/step-block-assembly.md) | Human task goal in simulated teleoperation; extension is distinguished from its underlying 2025 corpus. Robot assistance plans are not human intention labels. |
| [Visual planning](https://arxiv.org/abs/2507.15130) | Existing Ego4D | LTA reuse; inferred goal text is distinguished from native intention ground truth. |
| [IntentVLM](https://arxiv.org/abs/2604.24002) | Existing [IntentQA](datasets/intentqa.md) | Source-backed downstream use; no duplicate dataset or new native release asserted. |

## Deduplication and held-out candidates

IntentQA, Ego4D, EPIC-KITCHENS-100, EGTEA Gaze+, Assembly101 and Brain4Cars were already present. Repeated PDF copies and method names (including AntGPT, INSIGHT and PAR-VLA) are not independent datasets. No new benchmark scores are introduced.

- [Inst-IT Bench](https://github.com/inst-it/inst-it): general instance understanding, used as a transfer test. That use alone does not establish an intention, goal or future-behavior target.
- [BDD-OIA](https://github.com/Twizwei/bddoia_project): appropriate autonomous-vehicle action decisions and rationales. These do not establish the observed human driver's actual intention; held out under the agent-policy boundary.
- ROAD and EasyCom: current road-event labels and active-speaker localization do not establish an eligible intention or future-behavior task in the inspected uses. A separately sourced eligible protocol could change this decision.
- Informer forecasting and generic commonsense knowledge mining: no eligible human-intention dataset was established in these papers.

## Access and licenses

Availability describes the resource component actually checked. Public code does not establish full media access, and software or paper licenses are not transferred to datasets. Original DAAD, CAMF study data, STEP extended data, Aria binary access, 50 Salads bulk access and the DR(eye)VE legacy download remain unresolved. Unknown fields are retained rather than filled by inference. The DAAD-X publisher-declared hosted-release license is kept separate from unverified upstream DAAD media terms.
