from fastapi import FastAPI

from src.api.routes import router


app = FastAPI(
    title="Global Household AIOps API",
    description=(
        "Production API for the Global Household "
        "MLOps and GenAIOps platform."
    ),
    version="0.1.0",
)

app.include_router(router)