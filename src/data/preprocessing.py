from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


CATEGORICAL_FEATURES = [
    "Country",
    "City",
]

NUMERICAL_FEATURES = [
    "Family_Size",
    "Num_Earners",
    "Primary_Income",
    "Total_Household_Income",
    "Estimated_Taxes",
    "Monthly_Expenses",
]

MODEL_FEATURES = CATEGORICAL_FEATURES + NUMERICAL_FEATURES


def build_preprocessor() -> ColumnTransformer:
    """Create preprocessing pipeline."""

    return ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore",
                    min_frequency=0.05,
                ),
                CATEGORICAL_FEATURES,
            ),
            (
                "numerical",
                StandardScaler(),
                NUMERICAL_FEATURES,
            ),
        ]
    )
