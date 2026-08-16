from src.evaluation.quality_gate import (
    evaluate_genai_quality_gate,
)


def test_genai_quality_gate_passes():

    metrics = {
        "routing_accuracy": 1.00,
        "retrieval_source_recall": 0.95,
        "retrieval_keyword_recall": 0.90,
    }

    passed, failures = evaluate_genai_quality_gate(
        metrics=metrics,
        minimum_routing_accuracy=0.95,
        minimum_source_recall=0.90,
        minimum_keyword_recall=0.85,
    )

    assert passed is True
    assert failures == []


def test_genai_quality_gate_fails():

    metrics = {
        "routing_accuracy": 0.80,
        "retrieval_source_recall": 0.70,
        "retrieval_keyword_recall": 0.60,
    }

    passed, failures = evaluate_genai_quality_gate(
        metrics=metrics,
        minimum_routing_accuracy=0.95,
        minimum_source_recall=0.90,
        minimum_keyword_recall=0.85,
    )

    assert passed is False
    assert len(failures) == 3