from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from src.api.main import app
import src.api.routes as routes


client = TestClient(app)


def test_health_endpoint():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }


def test_chat_endpoint():

    mock_orchestrator = MagicMock()

    mock_orchestrator.handle.return_value = (
        MagicMock(
            text="Good morning!",
            route="slm",
            model="phi-4-mini",
            sources=[],
        )
    )

    routes._orchestrator = (
        mock_orchestrator
    )

    response = client.post(
        "/api/chat",
        json={
            "query": "Good morning"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["route"] == "slm"
    assert data["model"] == "phi-4-mini"
    assert data["text"] == "Good morning!"


def test_empty_query_is_rejected():

    response = client.post(
        "/api/chat",
        json={
            "query": ""
        },
    )

    assert response.status_code == 422