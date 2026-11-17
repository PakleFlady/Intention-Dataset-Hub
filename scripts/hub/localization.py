"""Chinese presentation of the shared README overview (facts stay in YAML)."""

TRANSLATIONS = {
    "**Verified datasets:**": "**已核验数据集：**",
    "**Dataset families:**": "**数据集家族：**",
    "**Verified protocols:**": "**已核验评测协议：**",
    "**Datasets with at least two comparable results:**": "**至少有两条同类可比结果的数据集：**",
    "## Featured datasets": "## 数据集精选",
    "## Benchmark availability": "## 评测与结果覆盖",
    "| Dataset | Year | Domain | Relevance | Access |": "| 数据集 | 年份 | 领域 | 收录依据 | 获取方式 |",
    "| Dataset | Task | Protocol | Results | Snapshot checked |": "| 数据集 | 任务 | 评测协议（原名） | 已核验结果数 | 结果快照核验日期 |",
    "Complete dataset index": "完整数据集目录",
    "By domain": "按领域浏览", "By task": "按任务浏览", "By modality": "按模态浏览",
    "Conventional models": "普通模型结果", "LLM / VLM models": "LLM / VLM 结果",
    "By model category": "按模型类别浏览", "All result groups": "全部分组与覆盖缺口",
    "Complete benchmark index": "完整评测目录",
    "social_interaction": "社会交互", "daily_activities": "日常活动",
    "embodied_interaction": "具身交互", "human_robot_interaction": "人机协作",
    "human_object_interaction": "人与物体交互", "driver_behavior": "驾驶员行为",
    "autonomous_driving": "自动驾驶", "pedestrian": "行人",
    "action_anticipation": "动作发生前预测", "intention_recognition": "意图识别",
    "intention_reasoning": "意图推理", "behavior_prediction": "行为预测",
    "explicit": "直接意图", "implicit": "行为代理", "related": "相关线索",
    "restricted": "受限访问", "unavailable": "暂不可获取", "registration": "需注册",
    "unknown": "尚未确认", "open": "公开获取", "request": "需申请",
}


def chinese_overview(overview: str) -> str:
    # Translate visible text only; URLs and anchor IDs must remain byte-identical.
    import re
    parts = re.split(r"(\]\([^)]*\)|<!--.*?-->)", overview)
    for index in range(0, len(parts), 2):
        for original, translated in TRANSLATIONS.items():
            parts[index] = parts[index].replace(original, translated)
    return "".join(parts)
