import pandas as pd

from src.features.feature_engineering import (
    create_financial_features,
)


def test_feature_engineering():
    df = pd.DataFrame(
        {
            "Household_ID": [1],
            "Country": ["UK"],
            "City": ["Leeds"],
            "Family_Size": [2],
            "Num_Earners": [1],
            "Primary_Income": [3000.0],
            "Total_Household_Income": [3000.0],
            "Estimated_Taxes": [600.0],
            "Monthly_Expenses": [100.0],
            "Monthly_Savings": [100.0],
        }
    )

    result = create_financial_features(df)

    assert "net_income" in result.columns
    assert "savings_rate" in result.columns
    assert "expense_ratio" in result.columns
    assert "financial_health_score" in result.columns
    assert "health_category" in result.columns
