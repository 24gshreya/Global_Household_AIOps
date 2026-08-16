def evaluate_quality_gate(
    metrics: dict[str, float],
    minimum_accuracy: float,
    minimum_f1_macro: float,
) -> tuple[bool, list[str]]:
    """
    Determine whether a candidate model satisfies
    production quality thresholds.
    """

    failures = []

    accuracy = metrics.get("accuracy", 0.0)
    f1_macro = metrics.get("f1_macro", 0.0)

    if accuracy < minimum_accuracy:
        failures.append(
            f"Accuracy {accuracy:.4f} is below minimum {minimum_accuracy:.4f}"
        )

    if f1_macro < minimum_f1_macro:
        failures.append(
            f"F1 macro {f1_macro:.4f} is below minimum {minimum_f1_macro:.4f}"
        )

    passed = len(failures) == 0

    return passed, failures


def evaluate_genai_quality_gate(
    metrics: dict[str, float],
    minimum_routing_accuracy: float = 0.95,
    minimum_source_recall: float = 0.90,
    minimum_keyword_recall: float = 0.85,
) -> tuple[bool, list[str]]:

    failures = []

    if (
        metrics["routing_accuracy"]
        < minimum_routing_accuracy
    ):
        failures.append(
            "Routing accuracy below threshold."
        )

    if (
        metrics["retrieval_source_recall"]
        < minimum_source_recall
    ):
        failures.append(
            "RAG source recall below threshold."
        )

    if (
        metrics["retrieval_keyword_recall"]
        < minimum_keyword_recall
    ):
        failures.append(
            "RAG keyword recall below threshold."
        )

    return (
        len(failures) == 0,
        failures,
    )