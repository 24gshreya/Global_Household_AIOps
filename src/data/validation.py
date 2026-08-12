import pandas as pd


REQUIRED_COLUMNS = [
    "Household_ID",
    "Country",
    "City",
    "Family_Size",
    "Num_Earners",
    "Primary_Income",
    "Total_Household_Income",
    "Estimated_Taxes",
    "Monthly_Expenses",
    "Monthly_Savings",
]


def validate_data(df: pd.DataFrame) -> None:
    """Validate raw household dataset before training."""

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df.empty:
        raise ValueError("Dataset contains no rows.")

    if df["Household_ID"].duplicated().any():
        raise ValueError("Duplicate Household_ID values detected.")

    if (df["Family_Size"] <= 0).any():
        raise ValueError("Family_Size must be greater than zero.")

    if (df["Num_Earners"] <= 0).any():
        raise ValueError("Num_Earners must be greater than zero.")

    if (df["Total_Household_Income"] < 0).any():
        raise ValueError("Total_Household_Income cannot be negative.")

    if (df["Monthly_Expenses"] < 0).any():
        raise ValueError("Monthly_Expenses cannot be negative.")


"""    if (df["Monthly_Savings"] < 0).any():
        raise ValueError("Monthly_Savings cannot be negative.") """
