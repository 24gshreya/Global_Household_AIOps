import pytest

from src.genai.router import Route, route_query


@pytest.mark.parametrize(
    "query,expected_route",
    [
        ("Good morning", Route.SLM),
        ("Thank you", Route.SLM),
        (
            "What did SHAP reveal about poor financial health?",
            Route.RAG,
        ),
        (
            "Which statistical test showed savings differ across countries?",
            Route.RAG,
        ),
        (
            "What is the average household income in India?",
            Route.DATA,
        ),
        (
            "How many households are in the UK?",
            Route.DATA,
        ),
    ],
)
def test_expected_routes(
    query,
    expected_route,
):
    assert route_query(query) == expected_route