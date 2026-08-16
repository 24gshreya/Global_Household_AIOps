from unittest.mock import MagicMock

import numpy as np

from src.rag.vector_store import VectorStore


def test_vector_store_returns_best_match():

    store = VectorStore()

    documents = [
        {
            "source": "business_definitions.md",
            "text": "Expense ratio measures expenses relative to income.",
        },
        {
            "source": "cluster_findings.md",
            "text": "Cluster 3 contains financially distressed households.",
        },
    ]

    embeddings = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
        ],
        dtype="float32",
    )

    store.build(
        embeddings,
        documents,
    )

    query_embedding = np.array(
        [1.0, 0.0],
        dtype="float32",
    )

    results = store.search(
        query_embedding,
        top_k=1,
    )

    assert len(results) == 1

    assert (
        results[0]["source"]
        == "business_definitions.md"
    )