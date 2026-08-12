from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd

from src.models.predict import (
    predict_financial_health,
)


def test_predict_financial_health():

    sample_input = pd.DataFrame(
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

    mock_model = MagicMock()

    mock_model.predict.return_value = np.array([1])

    with patch(
        "src.models.predict.load_champion_model",
        return_value=mock_model,
    ):
        prediction = predict_financial_health(sample_input)

    mock_model.predict.assert_called_once()

    assert len(prediction) == 1
    assert prediction[0] == 1
