import pytest

from src.genai.router import (
    Route,
    normalize_query,
    route_query,
)


@pytest.mark.parametrize(
    "query",
    [
        "Hello",
        "Hi",
        "Good morning",
        "How are you",
        "Thanks",
        "Bye",
    ],
)
def test_small_talk_routes_to_slm(query):
    assert route_query(query) == Route.SLM


@pytest.mark.parametrize(
    "query",
    [
        "What did SHAP reveal?",
        "Explain the financial health score",
        "Describe cluster 3",
        "What did the ANOVA test show?",
    ],
)
def test_knowledge_queries_route_to_rag(query):
    assert route_query(query) == Route.RAG


@pytest.mark.parametrize(
    "query",
    [
        "What is the average household income in India?",
        "How many households are in the UK?",
        "Which country has the highest savings?",
        "What percentage of households are Poor?",
    ],
)
def test_numeric_queries_route_to_data(query):
    assert route_query(query) == Route.DATA


def test_normalize_query():
    assert (
        normalize_query("  GOOD   MORNING  ")
        == "good morning"
    )