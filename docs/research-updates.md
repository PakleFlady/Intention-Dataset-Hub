# Research update review — 2026-11-17

This pass covered MIntRec, MIntRec2.0 and IntentQA. It is not an exhaustive review of all catalog datasets or a claim that the newest/highest result has been found. Numerical evidence is stored in Benchmark YAML and displayed in the separate [conventional](results-conventional.md) and [LLM/VLM](results-llm-vlm.md) result pages.

## LLM / VLM evidence

- [MMLA, arXiv v2](https://arxiv.org/html/2504.16427v2): Tables 3 and 4 report dataset-specific SFT and instruction-tuning results. They are separate settings. The README leaderboard aggregates multiple tasks; it must not be copied as a MIntRec score. The MIntRec2.0 subset excludes out-of-scope labels. [Recorded source values and audit gaps](benchmarks/mintrec2.md).
- The [author training configuration](https://github.com/thuiar/MMLA/blob/12d1a7ccc94f54764be439d392e7c37fb4eeb890/src/Finetune/MLLM/Qwen2-VL/SFT/train_lora/train_lora/MIntRec_intent_Qwen2-VL-7B-Instruct.yaml) identifies LoRA and a validation set; that alone does not establish the exact inference frame sampling or label-extraction behavior behind every table row. Those checks remain open.
- [X-CaVIR / IntentQA, TPAMI accepted manuscript](https://arxiv.org/html/2608.23330v1): Table V model 7-2 uses GPT-4 at inference. Main-set results and the five contrast sets assess different conditions. [Recorded source value and audit gaps](benchmarks/intentqa.md#intentqa-xcavir-gpt4-2026).

## Conventional-model evidence

- [MVCL-DAF++, original preprint](https://arxiv.org/html/2509.17446v1): Table 1 reports a mean across ten seeds. Its BERT/LSTM/fusion architecture belongs in the conventional category under this Hub's definitions. Exact splits, feature preprocessing and MIntRec2.0 out-of-scope handling still need file-level confirmation. [Recorded source values](results-conventional.md).

## Status

The new reports are **not ranked**. Each retains the paper version, table, model row, metric, category and a specific unresolved comparison question in YAML. No new snapshot declares them SOTA, and historical verified values remain unchanged. This preserves useful numerical leads without turning incompletely matched experiments into a leaderboard.

Existing dataset coverage outside the three datasets above has not been re-audited in this pass. A later review can promote a record only after resolving its listed protocol gaps and completing a second source check.
