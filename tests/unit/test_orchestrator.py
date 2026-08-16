from unittest.mock import MagicMock

from src.genai.llm import LLMResponse
from src.genai.orchestrator import Orchestrator
from src.genai.slm import SLMResponse


def build_mock_orchestrator():
    """
    Create an Orchestrator without running __init__,
    then mock all external dependencies.
    """
    orchestrator = Orchestrator.__new__(
        Orchestrator
    )

    orchestrator.slm = MagicMock()
    orchestrator.llm = MagicMock()
    orchestrator.retriever = MagicMock()
    orchestrator.data_tool = MagicMock()

    return orchestrator


def test_small_talk_uses_slm():

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
    assert response.text == "Good morning!"

    orchestrator.slm.generate.assert_called_once_with(
        "Good morning"
    )

    orchestrator.llm.generate.assert_not_called()
    orchestrator.retriever.retrieve.assert_not_called()
    orchestrator.data_tool.answer_query.assert_not_called()


def test_household_knowledge_query_uses_rag():

    orchestrator = build_mock_orchestrator()

    orchestrator.retriever.retrieve.return_value = [
        {
            "source": (
                "knowledge/analysis_findings/"
                "financial_health_findings.md"
            ),
            "text": (
                "SHAP analysis showed that low monthly "
                "savings and high expense ratio push "
                "predictions toward Poor financial health."
            ),
            "score": 0.91,
        }
    ]

    orchestrator.llm.generate.return_value = (
        LLMResponse(
            text=(
                "SHAP showed that low savings "
                "and high expense ratio are important "
                "drivers of Poor financial health."
            ),
            model="gemini-3.6-flash",
        )
    )

    response = orchestrator.handle(
        "What did SHAP reveal about poor financial health?"
    )

    assert response.route == "rag"
    assert response.model == "gemini-3.6-flash"

    orchestrator.retriever.retrieve.assert_called_once_with(
        query=(
            "What did SHAP reveal about "
            "poor financial health?"
        ),
        top_k=4,
    )

    orchestrator.llm.generate.assert_called_once()

    orchestrator.slm.generate.assert_not_called()
    orchestrator.data_tool.answer_query.assert_not_called()


def test_numeric_query_uses_data_tool():

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

    orchestrator.data_tool.answer_query.assert_called_once_with(
        "What is the average household income in India?"
    )

    orchestrator.slm.generate.assert_not_called()
    orchestrator.retriever.retrieve.assert_not_called()
    orchestrator.llm.generate.assert_not_called()