[English → README.en.md](README.en.md) | **简体中文**

# Intention Dataset Hub · 人类意图数据集与评测资料库

这个仓库帮你查清楚：**有哪些数据集研究人的意图、输入输出是什么、可以用什么方法做，以及哪些实验结果能够公平比较。**

我们关注人的行动、目标和交互目的，例如行人是否想过街、驾驶员准备怎样转向、说话者想表达什么、视频中的人为什么这样做。未来实际发生的行为可以作为意图的线索，但不能直接等同于人的真实心理状态。

每个数据集详情页包含输入输出示例、标注含义、官方来源、获取方式与许可说明；有可靠结果的数据集还会提供评测协议、数值和 baseline 代码入口。

## 从哪里开始

- **找数据集：** [完整目录](docs/datasets.md)，或按[研究领域](docs/by-domain.md)、[任务](docs/by-task.md)、[模态](docs/by-modality.md)浏览。
- **看一个真实样例：** 打开数据集详情页，先看 `Example input and output`。页面会区分官方标注记录、论文示例图和格式说明。
- **找方法与结果：** 分别查看[普通模型](docs/results-conventional.md)、[LLM / VLM](docs/results-llm-vlm.md)和[混合方法](docs/results-hybrid.md)。[分类规则](docs/model-classification.md)说明如何处理小型大模型和蒸馏方法。
- **了解最近补充：** [研究更新与待核验事项](docs/research-updates.md)；MIntRec 的本地样例与视频转载问题见[素材使用说明](docs/media-policy.md)。

<!-- hub:overview:start -->

**已核验数据集：** 21 | **数据集家族：** 20 | **已核验评测协议：** 8 | **至少有两条同类可比结果的数据集：** 6

## 数据集精选

| 数据集 | 年份 | 领域 | 收录依据 | 获取方式 |
| --- | --- | --- | --- | --- |
| [DeceptionDecoded](docs/datasets/deceptiondecoded.md) | 2025 | 社会交互 | 直接意图 | 受限访问 |
| [Intend to Move (I2M)](docs/datasets/i2m.md) | 2025 | 日常活动, 社会交互, 具身交互 | 直接意图 | 暂不可获取 |
| [Intentonomy](docs/datasets/intentonomy.md) | 2021 | 日常活动, 社会交互 | 直接意图 | 公开获取 |
| [Assembly101](docs/datasets/assembly101.md) | 2022 | 日常活动, 人与物体交互 | 行为代理 | 公开获取 |
| [Brain4Cars](docs/datasets/brain4cars.md) | 2015 | 驾驶员行为, 自动驾驶 | 行为代理 | 尚未确认 |
| [Ego4D](docs/datasets/ego4d.md) | 2021 | 日常活动, 人与物体交互 | 行为代理 | 需注册 |
| [Ego-Exo4D](docs/datasets/ego-exo4d.md) | 2024 | 日常活动, 具身交互 | 相关线索 | 需注册 |
| [HARMONIC](docs/datasets/harmonic.md) | 2021 | 人机协作, 人与物体交互 | 相关线索 | 公开获取 |

[完整数据集目录](docs/datasets.md) | [按领域浏览](docs/by-domain.md) | [按任务浏览](docs/by-task.md) | [按模态浏览](docs/by-modality.md)

## 评测与结果覆盖

| 数据集 | 任务 | 评测协议（原名） | 已核验结果数 | 结果快照核验日期 |
| --- | --- | --- | --- | --- |
| [Assembly101](docs/datasets/assembly101.md) | 动作发生前预测 | [ICIP 2023 Assembly101 validation, all-view fused anticipation](docs/benchmarks/assembly101.md#assembly101-icip2023-val-multiview) | 4 | 2026-10-08 |
| [Brain4Cars](docs/datasets/brain4cars.md) | 动作发生前预测 | [ICCV 2015 five-fold all-maneuver HMM cohort](docs/benchmarks/brain4cars.md#brain4cars-iccv2015-all-maneuvers-cv) | 3 | 2026-10-08 |
| [EPIC-KITCHENS-100](docs/datasets/epic-kitchens-100.md) | 动作发生前预测 | [EK100 challenge test action anticipation](docs/benchmarks/epic-kitchens-100.md#ek100-2021-test-action-anticipation) | 0 | — |
| [Intentonomy](docs/datasets/intentonomy.md) | 意图识别 | [Author repository test-set RGB baseline cohort](docs/benchmarks/intentonomy.md#intentonomy-author-test-rgb) | 2 | 2026-09-30 |
| [IntentQA](docs/datasets/intentqa.md) | 意图推理 | [ICCV 2023 BERT video-and-text no-GPT test cohort](docs/benchmarks/intentqa.md#intentqa-iccv2023-no-gpt-test) | 5 | 2026-09-30 |
| [JAAD](docs/datasets/jaad.md) | 行为预测 | [WACV 2021 JAAD_all PCPA attention comparison](docs/benchmarks/jaad.md#jaad-all-wacv2021-pcpa) | 4 | 2026-09-30 |
| [JAAD](docs/datasets/jaad.md) | 行为预测 | [WACV 2021 JAAD_all RGB 3D convolution comparison](docs/benchmarks/jaad.md#jaad-all-wacv2021-rgb3d) | 2 | 2026-09-30 |
| [PIE](docs/datasets/pie.md) | 意图识别 | [PIE ICCV 2019 intention estimation, location-only inputs](docs/benchmarks/pie.md#pie-intention-loc-iccv2019) | 2 | 2026-09-30 |

[普通模型结果](docs/results-conventional.md) | [LLM / VLM 结果](docs/results-llm-vlm.md) | [按模型类别浏览](docs/by-model-class.md) | [全部分组与覆盖缺口](docs/results.md) | [完整评测目录](docs/benchmarks.md)

<!-- hub:overview:end -->

## 两张概览表有什么区别

**数据集精选**介绍“有什么数据可用”：研究什么、属于什么领域、如何获取。它是浏览入口，不是数据集质量或学术重要性排行榜。

**评测与结果覆盖**介绍“目前整理了哪些可比较实验”：预测的标签、使用的数据版本、划分、输入、时间范围、训练条件和指标都必须明确。一个数据集可以有多个评测协议；也可以已经收录了数据集，却还没有核验完可比较的结果。结果数量为 `0` 不代表模型得分为零。

## 怎样理解分类与最佳结果

| 收录类别 | 含义 | 需要注意 |
| --- | --- | --- |
| 直接意图 `explicit` | 标注目标直接包含意图、目标或交互目的 | 标注可能来自观察者判断，不一定是本人自述 |
| 行为代理 `implicit` | 通过未来动作或行为预测研究意图 | 不能从“后来做了什么”直接推断“内心为什么这样做” |
| 相关线索 `related` | 提供有原始研究依据的目光、轨迹等线索 | 线索本身不是意图真值 |

完整边界见[收录范围](docs/scope.md)。普通客服意图分类、仅有当前动作识别的数据，不会仅因为名称里有“意图”就收录。

**普通模型与 LLM/VLM 分开整理、分开显示结果、分别计算最佳值。** 分类取决于模型在实验中怎样使用，而不是简单按参数量划线。同一类别内部，不同 split、模态、预测时长、训练方式和指标也不能直接混排。

仓库中的“最佳值”仅针对页面注明的协议、已核验结果集合和核验日期；它不代表已经穷尽全球最新 SOTA。数值有出处、但比较条件仍不清楚的结果会放在待核验区。代码链接可访问，也不意味着我们已经成功复现。

## 更新与贡献

新增数据集、协议、结果或纠错，请参照[贡献指南](CONTRIBUTING.md)。本地检查命令：

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python scripts/check_release_gate.py --level preview
python scripts/generate_docs.py
python scripts/generate_docs.py --check
python -m pytest
```

中文与英文主页的统计和概览表由同一份 YAML 数据生成。机器字段及详细资料暂保留英文，方便核对原论文与参与国际协作。请修改源数据，不要直接修改自动生成的表格。

[数据模型](docs/data-model.md)、[分类词表](docs/taxonomy.md)和[核验规则](docs/verification.md)解释了如何整理证据。自动检查能发现结构和已声明条件的问题，不能代替阅读原始论文。

## 当前状态、引用与许可

项目目前是 **研究预览版**。主页数量只统计已经核验的条目，不代表计划中的覆盖已全部完成；剩余缺口见[覆盖说明](docs/coverage.md)与[更新日志](CHANGELOG.md)。

引用本仓库请使用 [CITATION.cff](CITATION.cff)，研究中实际使用的数据集和方法仍需引用各自的原始论文。

代码采用 [MIT](LICENSE)，原创整理内容与文档采用 [CC BY 4.0](LICENSE-CONTENT)。外部数据、视频、论文和代码保留各自的权利与使用条件，**不会因为被本仓库收录而获得重新分发授权**。
