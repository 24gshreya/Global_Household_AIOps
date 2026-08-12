import pandas as pd
import pytest

from src.data.validation import validate_data


def create_valid_dataframe():
    return pd.DataFrame(
        {
            "Household_ID": [1],
            "Country": ["UK"],
            "City": ["Leeds"],
            "Family_Size": [3],
            "Num_Earners": [2],
            "Primary_Income": [3000],
            "Total_Household_Income": [5000],
            "Estimated_Taxes": [1000],
            "Monthly_Expenses": [2000],
            "Monthly_Savings": [1000],
        }
    )


def test_valid_data_passes():
    df = create_valid_dataframe()

    validate_data(df)


def test_missing_column_fails():
    df = create_valid_dataframe()

    df = df.drop(columns=["Monthly_Savings"])

    with pytest.raises(ValueError):
        validate_data(df)
