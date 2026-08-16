import pandas as pd

from src.genai.data_tool import (
    HouseholdDataTool,
)


def test_average_income_by_country(
    tmp_path,
):

    df = pd.DataFrame(
        {
            "Country": [
                "India",
                "India",
                "UK",
            ],
            "Total_Household_Income": [
                3000.0,
                5000.0,
                7000.0,
            ],
            "Monthly_Savings": [
                200.0,
                400.0,
                600.0,
            ],
        }
    )

    file_path = (
        tmp_path / "households.csv"
    )

    df.to_csv(
        file_path,
        index=False,
    )

    tool = HouseholdDataTool(
        dataset_path=str(file_path)
    )

    result = tool.average_income_by_country(
        "India"
    )

    assert result == 4000.0


def test_household_count_by_country(
    tmp_path,
):

    df = pd.DataFrame(
        {
            "Country": [
                "India",
                "India",
                "UK",
            ],
            "Total_Household_Income": [
                3000.0,
                5000.0,
                7000.0,
            ],
            "Monthly_Savings": [
                200.0,
                400.0,
                600.0,
            ],
        }
    )

    file_path = (
        tmp_path / "households.csv"
    )

    df.to_csv(
        file_path,
        index=False,
    )

    tool = HouseholdDataTool(
        dataset_path=str(file_path)
    )

    result = (
        tool.household_count_by_country(
            "India"
        )
    )

    assert result == 2