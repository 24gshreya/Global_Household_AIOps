import os
import json
import tempfile
from pathlib import Path

import mlflow
import mlflow.sklearn
import yaml
from dotenv import load_dotenv
from mlflow import MlflowClient
from mlflow.models import infer_signature

from sklearn.model_selection import (
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

from xgboost import XGBClassifier

from src.data.ingestion import (
    calculate_file_hash,
    load_data,
)
from src.data.preprocessing import (
    MODEL_FEATURES,
    build_preprocessor,
)
from src.data.validation import validate_data
from src.features.feature_engineering import (
    create_financial_features,
)
from src.models.evaluate import evaluate_classifier

from src.evaluation.quality_gate import evaluate_quality_gate
from src.registry.mlflow_registry import promote_to_champion




PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONFIG_PATH = PROJECT_ROOT / "ml" / "model_config.yaml"


def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def build_model(config: dict) -> Pipeline:
    """Create complete preprocessing + model pipeline."""

    preprocessor = build_preprocessor()

    training_config = config["training"]

    classifier = XGBClassifier(
        n_estimators=training_config["n_estimators"],
        max_depth=training_config["max_depth"],
        learning_rate=training_config["learning_rate"],
        random_state=training_config["random_state"],
        eval_metric="mlogloss",
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )


def train() -> None:
    """Run complete ML training pipeline."""

    load_dotenv()

    config = load_config()

    dataset_path = os.getenv(
        "DATASET_PATH",
        "data/raw/Global_Household_Financial_Dynamics.csv",
    )

    tracking_uri = os.getenv(
        "MLFLOW_TRACKING_URI",
        "http://127.0.0.1:5000",
    )

    mlflow.set_tracking_uri(tracking_uri)

    mlflow.set_experiment("global-household-financial-health")

    # -----------------------------
    # Data ingestion
    # -----------------------------

    df = load_data(dataset_path)

    validate_data(df)

    dataset_hash = calculate_file_hash(dataset_path)

    # -----------------------------
    # Feature engineering
    # -----------------------------

    df = create_financial_features(df)

    X = df[MODEL_FEATURES].copy()

    integer_features = ["Family_Size", "Num_Earners",]
    X[integer_features] = X[integer_features].astype("float64")

    y = df["health_category"].astype(str)

    # -----------------------------
    # Target encoding
    # -----------------------------

    label_encoder = LabelEncoder()

    y_encoded = label_encoder.fit_transform(y)

    label_mapping = {
        int(index): label for index, label in enumerate(label_encoder.classes_)
    }

    # -----------------------------
    # Train/test split
    # -----------------------------

    test_size = config["data"]["test_size"]
    random_state = config["data"]["random_state"]

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = train_test_split(
        X,
        y_encoded,
        test_size=test_size,
        random_state=random_state,
        stratify=y_encoded,
    )

    model = build_model(config)

    # -----------------------------
    # Cross-validation
    # -----------------------------

    cv = StratifiedKFold(
        n_splits=config["cross_validation"]["folds"],
        shuffle=True,
        random_state=random_state,
    )

    cv_scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring="accuracy",
    )

    # -----------------------------
    # Final training
    # -----------------------------

    model.fit(
        X_train,
        y_train,
    )

    predictions = model.predict(X_test)

    signature = infer_signature(X_train, model.predict(X_train))

    metrics = evaluate_classifier(
        y_test,
        predictions,
    )

    quality_config = config["quality_gate"]

    quality_passed, quality_failures = evaluate_quality_gate(
        metrics=metrics,
        minimum_accuracy=quality_config["minimum_accuracy"],
        minimum_f1_macro=quality_config["minimum_f1_macro"],
    )

    # -----------------------------
    # MLflow
    # -----------------------------

    with mlflow.start_run(run_name="xgboost-financial-health") as run:
        mlflow.log_params(
            {
                "algorithm": "XGBoost",
                "n_estimators": config["training"]["n_estimators"],
                "max_depth": config["training"]["max_depth"],
                "learning_rate": config["training"]["learning_rate"],
                "test_size": test_size,
                "random_state": random_state,
                "cv_folds": config["cross_validation"]["folds"],
            }
        )

        mlflow.log_metric(
            "cv_accuracy_mean",
            float(cv_scores.mean()),
        )

        mlflow.log_metric(
            "cv_accuracy_std",
            float(cv_scores.std()),
        )

        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(
                metric_name,
                float(metric_value),
            )

        mlflow.set_tags(
            {
                "project": "Global Household AIOps",
                "model_type": "classification",
                "dataset_sha256": dataset_hash,
                "target": "health_category",
                "framework": "scikit-learn+xgboost",
            }
        )

        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            name="financial-health-model",
            input_example=X_train.head(5),
            signature=signature,
            registered_model_name=("global-household-financial-health"),
            serialization_format="cloudpickle",
        )

        client = MlflowClient()

        registered_versions = client.search_model_versions(
            filter_string=(f"name='global-household-financial-health'")
        )

        current_model_version = None

        for version in registered_versions:
            if version.run_id == run.info.run_id:
                current_model_version = version.version
                break

        if current_model_version is None:
            raise RuntimeError("Could not determine registered model version.")

        if quality_passed:
            promote_to_champion(
                model_name=("global-household-financial-health"),
                model_version=current_model_version,
            )

            mlflow.set_tag(
                "quality_gate",
                "passed",
            )
            mlflow.set_tag(
                "promotion_status",
                "champion",
            )

        else:
            mlflow.set_tag(
                "quality_gate",
                "failed",
            )
            mlflow.set_tag(
                "promotion_status",
                "rejected",
            )

            for failure in quality_failures:
                print(f"QUALITY GATE FAILURE: {failure}")

        with tempfile.TemporaryDirectory() as temp_dir:
            mapping_path = Path(temp_dir) / "label_mapping.json"

            with open(
                mapping_path,
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    label_mapping,
                    file,
                    indent=2,
                )

            mlflow.log_artifact(
                str(mapping_path),
                artifact_path="metadata",
            )

        print()
        print("Training completed.")
        print(f"Run ID: {run.info.run_id}")
        print(f"Registered model version: {current_model_version}")

        print(f"CV accuracy: {cv_scores.mean():.4f}")

        for name, value in metrics.items():
            print(f"{name}: {value:.4f}")
        
        print(
            "Classes:",
            list(label_encoder.classes_),
        )

        if quality_passed:
            print("Quality gate: PASSED")
            print(f"Champion version: {current_model_version}")
        else:
            print("Quality gate: FAILED")
            raise RuntimeError(
                "Candidate model failed production quality gate."
            )

if __name__ == "__main__":
    train()
