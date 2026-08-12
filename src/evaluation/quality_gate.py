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
