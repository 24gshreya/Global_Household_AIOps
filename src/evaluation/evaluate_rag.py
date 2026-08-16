import json

from src.rag.retriever import HouseholdRetriever


def evaluate_rag(
    dataset_path: str,
) -> dict:

    retriever = HouseholdRetriever()

    total = 0
    source_hits = 0
    keyword_hits = 0

    with open(
        dataset_path,
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:
            row = json.loads(line)

            results = retriever.retrieve(
                row["question"],
                top_k=4,
            )

            total += 1

            expected_source = row[
                "expected_source"
            ]

            if any(
                expected_source
                in result["source"]
                for result in results
            ):
                source_hits += 1

            retrieved_text = " ".join(
                result["text"]
                for result in results
            ).lower()

            keywords = row[
                "expected_keywords"
            ]

            matched = sum(
                keyword.lower()
                in retrieved_text
                for keyword in keywords
            )

            if matched == len(keywords):
                keyword_hits += 1

    return {
        "retrieval_source_recall": (
            source_hits / total
        ),
        "retrieval_keyword_recall": (
            keyword_hits / total
        ),
    }