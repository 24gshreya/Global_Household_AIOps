from pathlib import Path

import pandas as pd
import re

class HouseholdDataTool:
    """Pandas-based analytical tool for household dataset queries."""

    def __init__(
        self,
        dataset_path: str = (
            "data/raw/"
            "Global_Household_Financial_Dynamics.csv"
        ),
    ):
        path = Path(dataset_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {path}"
            )

        self.df = pd.read_csv(path)

    def average_income_by_country(
        self,
        country: str,
    ) -> float:

        subset = self.df[
            self.df["Country"].str.lower()
            == country.lower()
        ]

        if subset.empty:
            raise ValueError(
                f"No data found for country: {country}"
            )

        return float(
            subset[
                "Total_Household_Income"
            ].mean()
        )

    def household_count_by_country(
        self,
        country: str,
    ) -> int:

        subset = self.df[
            self.df["Country"].str.lower()
            == country.lower()
        ]

        return int(len(subset))

    def country_with_highest_average_savings(
        self,
    ) -> tuple[str, float]:

        grouped = (
            self.df.groupby("Country")[
                "Monthly_Savings"
            ]
            .mean()
            .sort_values(
                ascending=False
            )
        )

        country = grouped.index[0]
        value = float(grouped.iloc[0])

        return country, value

    def country_with_lowest_average_savings(
        self,
    ) -> tuple[str, float]:

        grouped = (
            self.df.groupby("Country")[
                "Monthly_Savings"
            ]
            .mean()
            .sort_values()
        )

        country = grouped.index[0]
        value = float(grouped.iloc[0])

        return country, value


    def answer_query(
        self,
        query: str,
    ) -> str:

        normalized = query.lower()

        if (
            "average household income" in normalized
            or "average income" in normalized
        ):
            country = self._extract_country(query)

            value = self.average_income_by_country(
                country
            )

            return (
                f"The average household income in "
                f"{country} is {value:,.2f}."
            )

        if (
            "how many households" in normalized
            or "count households" in normalized
        ):
            country = self._extract_country(query)

            count = self.household_count_by_country(
                country
            )

            return (
                f"There are {count:,} households "
                f"in {country}."
            )

        if (
            "highest savings" in normalized
            or "highest average savings" in normalized
        ):
            country, value = (
                self.country_with_highest_average_savings()
            )

            return (
                f"{country} has the highest average "
                f"monthly savings at {value:,.2f}."
            )

        if (
            "lowest savings" in normalized
            or "lowest average savings" in normalized
        ):
            country, value = (
                self.country_with_lowest_average_savings()
            )

            return (
                f"{country} has the lowest average "
                f"monthly savings at {value:,.2f}."
            )

        raise ValueError(
            "This analytical query is not supported yet."
        )

    def _extract_country(
        self,
        query: str,
    ) -> str:

        countries = (
            self.df["Country"]
            .dropna()
            .astype(str)
            .unique()
        )

        query_lower = query.lower()

        for country in countries:
            if country.lower() in query_lower:
                return country

        raise ValueError(
            "Could not identify country in query."
        )