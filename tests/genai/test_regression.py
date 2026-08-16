from unittest.mock import MagicMock

from src.genai.llm import LLMResponse
from src.genai.orchestrator import Orchestrator
from src.genai.slm import SLMResponse


def build_mock_orchestrator():

    orchestrator = Orchestrator.__new__(
        Orchestrator
    )

    orchestrator.slm = MagicMock()
    orchestrator.llm = MagicMock()
    orchestrator.retriever = MagicMock()
    orchestrator.data_tool = MagicMock()

    return orchestrator


def test_regression_small_talk():

    orchestrator = build_mock_orchestrator()

    orchestrator.slm.generate.return_value = (
        SLMResponse(
            text="Good morning!",
            model="phi-4-mini",
        )
    )

    response = orchestrator.handle(
        "Good morning"
    )

    assert response.route == "slm"
    assert response.model == "phi-4-mini"


def test_regression_anova_rag_answer():

    orchestrator = build_mock_orchestrator()

    orchestrator.retriever.retrieve.return_value = [
        {
            "source": "statistical_findings.md",
            "text": (
                "A one-way ANOVA found statistically "
                "significant differences in savings "
                "rates across countries."
            ),
            "score": 0.95,
        }
    ]

    orchestrator.llm.generate.return_value = (
        LLMResponse(
            text=(
                "A one-way ANOVA showed significant "
                "differences in savings rates across countries."
            ),
            model="gemini-3.6-flash",
            prompt_version="v2",
        )
    )

    response = orchestrator.handle(
        "Which statistical test showed savings differ across countries?"
    )

    assert response.route == "rag"
    assert "ANOVA" in response.text
    assert response.model == "gemini-3.6-flash"


def test_regression_numeric_query():

    orchestrator = build_mock_orchestrator()

    orchestrator.data_tool.answer_query.return_value = (
        "The average household income "
        "in India is 4,000.00."
    )

    response = orchestrator.handle(
        "What is the average household income in India?"
    )

    assert response.route == "data"
    assert response.model == "pandas-analytics-v1"
    assert "India" in response.text