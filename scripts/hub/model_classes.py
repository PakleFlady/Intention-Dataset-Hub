"""Result-level method categories; parameter count is not a category boundary."""

MODEL_CLASSES = {
    "conventional": ("Conventional / task-specific models", "Task-specific classifiers and predictors, including BERT encoders, without generative LLM/VLM assistance."),
    "llm_vlm": ("LLM / VLM models", "A generative language or vision-language foundation model participates in inference, including small foundation models and tool pipelines."),
    "hybrid": ("LLM-assisted training / hybrid models", "LLM/VLM-generated supervision or distillation is used in training, while inference uses a conventional model."),
    "unknown": ("Unclassified models", "Evidence does not yet establish the model category. These results cannot enter best-value calculations."),
}


def model_class(result: dict) -> str:
    return result.get("model_class", "unknown")
