import numpy as np
import pandas as pd


def create_financial_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Create financial-health features and target label."""

    df = df.copy()

    # Annual take-home income
    df["net_income"] = df["Total_Household_Income"] - df["Estimated_Taxes"]

    # Annual financial headroom
    df["disposable_income"] = (df["net_income"] - df["Monthly_Expenses"]) * 12

    monthly_net_income = df["net_income"] / 12

    # Avoid divide-by-zero problems
    monthly_net_income = monthly_net_income.replace(0, np.nan)

    df["savings_rate"] = (df["Monthly_Savings"] / monthly_net_income).round(2)

    df["expense_ratio"] = (df["Monthly_Expenses"] / monthly_net_income).round(2)

    df["income_per_capita"] = df["Total_Household_Income"] / df["Family_Size"]

    df["income_per_earner"] = df["Total_Household_Income"] / df["Num_Earners"]

    df["primary_income_share"] = df["Primary_Income"] / df["Total_Household_Income"]

    df["tax_rate"] = df["Estimated_Taxes"] / df["Total_Household_Income"]

    df["financial_health_score"] = df["savings_rate"] - df["expense_ratio"]

    df["health_category"] = pd.cut(
        df["financial_health_score"],
        bins=3,
        labels=["Poor", "Fair", "Good"],
    )

    df = df.dropna(
        subset=[
            "savings_rate",
            "expense_ratio",
            "financial_health_score",
            "health_category",
        ]
    )

    return df
