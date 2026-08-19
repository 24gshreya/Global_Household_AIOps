from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=2000,
        description="User question or conversational message.",
        examples=[
            "What did SHAP reveal about poor financial health?"
        ],
    )


class ChatResponse(BaseModel):
    text: str
    route: str
    model: str
    sources: list[str] = Field(
        default_factory=list
    )


class HealthResponse(BaseModel):
    status: str


class ReadinessResponse(BaseModel):
    status: str
    dataset_available: bool
    knowledge_base_available: bool
    gemini_configured: bool
    foundry_local_configured: bool