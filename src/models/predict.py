import os

import mlflow
import mlflow.sklearn
import pandas as pd
from dotenv import load_dotenv
from mlflow import MlflowClient


MODEL_NAME = "global-household-financial-health"
MODEL_ALIAS = "champion"


def configure_mlflow() -> None:
    """Configure MLflow connection."""

    load_dotenv()

    tracking_uri = os.getenv(
        "MLFLOW_TRACKING_URI",
        "http://127.0.0.1:5000",
    )

    mlflow.set_tracking_uri(tracking_uri)


def load_champion_model():
    """Load the approved champion model from MLflow Registry."""

    configure_mlflow()

    model_uri = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"

    return mlflow.sklearn.load_model(model_uri)


def predict_financial_health(
    input_data: pd.DataFrame,
):
    """Predict financial-health class using champion model."""

    model = load_champion_model()

    predictions = model.predict(input_data)

    return predictions


def get_champion_version() -> str:
    """Return version currently assigned to champion."""

    configure_mlflow()

    client = MlflowClient()

    model_version = client.get_model_version_by_alias(
        name=MODEL_NAME,
        alias=MODEL_ALIAS,
    )

    return model_version.version


if __name__ == "__main__":
    champion_version = get_champion_version()

    print(f"Champion model version: {champion_version}")

    sample_household = pd.DataFrame(
        [
            {
                "Country": "UK",
                "City": "Leeds",
                "Family_Size": 3.0,
                "Num_Earners": 2.0,
                "Primary_Income": 3000.0,
                "Total_Household_Income": 5000.0,
                "Estimated_Taxes": 1000.0,
                "Monthly_Expenses": 2000.0,
            }
        ]
    )

    prediction = predict_financial_health(sample_household)

    print(f"Prediction: {prediction[0]}")
