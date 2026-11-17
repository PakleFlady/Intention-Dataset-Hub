# Model categories and separate best values

The category belongs to a **result configuration**, not to a dataset. Every result requires `model_class` and `classification_notes`, grounded in its cited method/configuration sources. Names and definitions are recorded in `taxonomy.yaml`.

| Value | Meaning | Examples / boundary |
| --- | --- | --- |
| `conventional` | Task-specific models without generative LLM/VLM assistance | HMM, LSTM, CNN classifiers, BERT encoder + fusion classifier. This does not guarantee a small parameter count. |
| `llm_vlm` | Generative language or vision-language foundation models participate in inference | Qwen2-0.5B is still an LLM. GPT reasoning over captions and classifier outputs belongs here too. |
| `hybrid` | LLM/VLM-assisted training; conventional inference | LLM-generated supervision, distillation, or training-only reasoning. Document the teacher and generated-data source. |
| `unknown` | Insufficient evidence | Preserve the record without ranking it. Never infer the class just from a model name. |

Use `llm_vlm` when a pipeline includes both a conventional predictor and an LLM at inference. Reserve `hybrid` for training-only assistance, so those methods cannot silently enter the conventional group. Frozen contrastive encoders such as CLIP do not automatically make a method a generative VLM; explain their role.

The generator calculates each metric's winners independently within **protocol × category × snapshot**. Missing scores, disputed/withdrawn records, unclear protocols, and unknown categories remain excluded. Zero-shot, few-shot, single-dataset SFT and multi-dataset instruction tuning retain distinct comparison settings. A category split does not make different modalities or training data comparable.

Browse [conventional results](results-conventional.md), [LLM/VLM results](results-llm-vlm.md), [training-assisted hybrids](results-hybrid.md), or [all categories](by-model-class.md). Source-reported numbers with unresolved conditions appear separately and are not promoted to SOTA.

## Migration

This preview adds two required Result fields to schema 0.1: `model_class` and `classification_notes`. Existing source cohorts were labeled `conventional` based on their recorded HMM/LSTM/CNN/BERT/task-specific configurations. Snapshot dates and numeric values were not refreshed. New contributions must document model use before entering rankings.
