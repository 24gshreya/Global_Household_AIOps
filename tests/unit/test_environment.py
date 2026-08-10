import pandas
import sklearn
import xgboost
import mlflow
import fastapi


def test_environment():
    assert pandas.__version__
    assert sklearn.__version__
    assert xgboost.__version__
    assert mlflow.__version__
    assert fastapi.__version__