from src.evaluation.quality_gate import (
    evaluate_quality_gate,
)


def test_quality_gate_passes():
    metrics = {
        "accuracy": 0.95,
        "f1_macro": 0.94,
    }

    passed, failures = evaluate_quality_gate(
        metrics=metrics,
        minimum_accuracy=0.93,
        minimum_f1_macro=0.93,
    )

    assert passed is True
    assert failures == []


def test_quality_gate_fails():
    metrics = {
        "accuracy": 0.90,
        "f1_macro": 0.89,
    }

    passed, failures = evaluate_quality_gate(
        metrics=metrics,
        minimum_accuracy=0.93,
        minimum_f1_macro=0.93,
    )

    assert passed is False
    assert len(failures) == 2
