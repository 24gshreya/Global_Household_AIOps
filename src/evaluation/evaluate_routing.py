import json
from pathlib import Path

from src.genai.router import route_query


def evaluate_routing(
    dataset_path: str,
) -> dict:

    path = Path(dataset_path)

    total = 0
    correct = 0
    failures = []

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:
            row = json.loads(line)

            predicted = route_query(
                row["query"]
            ).value

            expected = row["expected_route"]

            total += 1

            if predicted == expected:
                correct += 1
            else:
                failures.append(
                    {
                        "query": row["query"],
                        "expected": expected,
                        "predicted": predicted,
                    }
                )

    accuracy = (
        correct / total
        if total
        else 0.0
    )

    return {
        "routing_accuracy": accuracy,
        "total": total,
        "failures": failures,
    }