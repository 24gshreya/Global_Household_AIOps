import pandas as pd

from src.data.preprocessing import MODEL_FEATURES
from src.features.feature_engineering import (
    create_financial_features,
)
from src.models.train import build_model, load_config
from sklearn.preprocessing import LabelEncoder

def test_training_pipeline():
    raw_df = pd.DataFrame(
        {
            "Household_ID": list(range(1, 31)),
            "Country": ["UK"] * 10
            + ["India"] * 10
            + ["USA"] * 10,
            "City": ["Leeds"] * 10
            + ["Delhi"] * 10
            + ["New York"] * 10,
            "Family_Size": [2, 3, 4] * 10,
            "Num_Earners": [1, 2, 2] * 10,
            "Primary_Income": [
                2500.0 + i * 100
                for i in range(30)
            ],
            "Total_Household_Income": [
                3500.0 + i * 150
                for i in range(30)
            ],
            "Estimated_Taxes": [
                600.0 + i * 20
                for i in range(30)
            ],
            "Monthly_Expenses": [
                100.0 + i * 10
                for i in range(30)
            ],
            "Monthly_Savings": [
                -50.0 + i * 20
                for i in range(30)
            ],
        }
    )

    engineered_df = create_financial_features(
        raw_df
    )

    X = engineered_df[MODEL_FEATURES].copy()

    X[
        [
            "Family_Size",
            "Num_Earners",
        ]
    ] = X[
        [
            "Family_Size",
            "Num_Earners",
        ]
    ].astype("float64")

    y = (engineered_df["health_category"].astype(str))

    label_encoder = LabelEncoder()

    y_encoded = label_encoder.fit_transform(y)
    
    config = load_config()

    model = build_model(config)

    model.fit(X, y_encoded)

    predictions = model.predict(X)

    assert len(predictions) == len(X)
    assert set(predictions).issubset(set(y_encoded))
