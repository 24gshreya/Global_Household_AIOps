import mlflow
import pandas as pd


MODEL_NAME = "global-household-financial-health"

MODEL_ALIAS = "champion"


def load_champion_model():
    """Load the currently approved production model."""

    model_uri = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"

    return mlflow.sklearn.load_model(model_uri)


def predict_financial_health(
    input_data: pd.DataFrame,
):
    """
    Predict financial-health class using the
    current champion model.
    """

    model = load_champion_model()

    predictions = model.predict(input_data)

    return predictions
