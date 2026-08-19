import os
from pathlib import Path

from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from src.api.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    ReadinessResponse,
)
from src.genai.orchestrator import Orchestrator
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

_orchestrator: Orchestrator | None = None


def get_orchestrator() -> Orchestrator:
    """
    Lazily create one orchestrator instance.

    This avoids rebuilding the embedding model,
    FAISS index, LLM client, and data tool for
    every request.
    """

    global _orchestrator

    if _orchestrator is None:
        _orchestrator = Orchestrator()

    return _orchestrator


@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
)
def health() -> HealthResponse:
    """
    Liveness check.

    Confirms that the API process itself is running.
    """

    return HealthResponse(
        status="healthy"
    )


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    tags=["System"],
)
def readiness() -> ReadinessResponse:
    """
    Readiness check for important application dependencies.
    """

    dataset_available = Path(
        "data/raw/Global_Household_Financial_Dynamics.csv"
    ).exists()

    knowledge_base_available = (
        Path("knowledge").exists()
        and any(Path("knowledge").rglob("*.md"))
    )

    gemini_configured = bool(
        os.getenv("GEMINI_API_KEY")
    )

    foundry_local_configured = bool(
        os.getenv("FOUNDRY_LOCAL_BASE_URL")
    )

    all_ready = all(
        [
            dataset_available,
            knowledge_base_available,
            gemini_configured,
            foundry_local_configured,
        ]
    )

    response = ReadinessResponse(
        status=(
            "ready"
            if all_ready
            else "not_ready"
        ),
        dataset_available=dataset_available,
        knowledge_base_available=knowledge_base_available,
        gemini_configured=gemini_configured,
        foundry_local_configured=foundry_local_configured,
    )

    if not all_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=response.model_dump(),
        )

    return response


@router.post(
    "/api/chat",
    response_model=ChatResponse,
    tags=["AI"],
)
def chat(
    request: ChatRequest,
) -> ChatResponse:
    """
    Send a message through the AI orchestration layer.
    """

    try:
        orchestrator = get_orchestrator()

        response = orchestrator.handle(
            request.query
        )

        return ChatResponse(
            text=response.text,
            route=response.route,
            model=response.model,
            sources=response.sources,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI request failed.",
        ) from exc