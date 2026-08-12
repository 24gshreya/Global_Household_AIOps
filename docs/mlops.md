# MLOps Implementation

## Overview

The Global Household AIOps project demonstrates how a machine learning model is moved from experimentation into a repeatable, testable, versioned and production-oriented MLOps workflow.

The machine learning component predicts household financial health categories using an XGBoost classifier.

The target classes are:

* Fair
* Good
* Poor

The implementation is primarily developed and tested locally to minimize cloud cost. Azure Machine Learning will later be used for short-lived cloud registration, deployment and monitoring demonstrations.

## MLOps Architecture

```text
Raw Household Dataset
        |
        v
Data Ingestion
        |
        v
Data Validation
        |
        v
Feature Engineering
        |
        v
Train / Test Split
        |
        v
Preprocessing Pipeline
        |
        v
Stratified Cross Validation
        |
        v
XGBoost Training
        |
        v
Model Evaluation
        |
        v
MLflow Experiment Tracking
        |
        v
MLflow Model Registry
        |
        v
Quality Gate
      /     \
   PASS     FAIL
    |         |
    v         v
Champion   Rejected
    |
    v
Inference
```

## Data Ingestion

Training data is loaded through:

```text
src/data/ingestion.py
```

The ingestion layer validates that the dataset exists and is not empty.

A SHA-256 hash of the source dataset is generated for each training run.

The dataset hash is recorded as MLflow metadata to provide lightweight data lineage and make it possible to identify which dataset version produced a model.

## Data Validation

Data validation is implemented in:

```text
src/data/validation.py
```

Validation is performed before model training.

Checks include:

* Required columns
* Empty datasets
* Duplicate household identifiers
* Invalid family size
* Invalid number of earners
* Negative household income
* Invalid tax values
* Invalid expense values

Negative monthly savings are allowed because households may spend more than their available monthly income.

## Feature Engineering

Feature engineering is implemented in:

```text
src/features/feature_engineering.py
```

Derived features include financial measures such as:

* Net income
* Disposable income
* Savings rate
* Expense ratio
* Income per capita
* Income per earner
* Primary income share
* Tax rate
* Financial health score

The financial health score is converted into the target classes Poor, Fair and Good.

## Leakage Improvement

During productionisation of the original experimental model, Monthly Savings was identified as being closely related to the engineered financial-health target.

Monthly Savings was therefore removed from the predictive feature set.

This reduced the reported model performance slightly but produced a more realistic estimate of model generalisation.

The productionised model currently achieves approximately:

```text
Cross-validation accuracy: 94.28%
Test accuracy:             94.68%
Macro precision:           94.80%
Macro recall:              94.78%
Macro F1:                  94.79%
```

## Preprocessing

Preprocessing is implemented using a Scikit-learn `ColumnTransformer`.

Categorical features:

```text
Country
City
```

are transformed using `OneHotEncoder`.

Numerical features are standardized using `StandardScaler`.

The preprocessing component and XGBoost classifier are placed inside a single Scikit-learn Pipeline.

This ensures preprocessing is fitted separately within each cross-validation training fold and avoids leakage from validation folds.

## Training

Training is implemented in:

```text
src/models/train.py
```

The training workflow performs:

```text
Load data
   |
Validate data
   |
Generate features
   |
Encode target
   |
Stratified train/test split
   |
Stratified cross-validation
   |
Train final model
   |
Evaluate
   |
Track experiment
   |
Register model
```

Model configuration and quality thresholds are stored separately in:

```text
ml/model_config.yaml
```

This separates operational configuration from application code.

## Experiment Tracking

MLflow is used locally for experiment tracking.

Each run records:

### Parameters

```text
Algorithm
Number of estimators
Maximum tree depth
Learning rate
Test size
Random state
Cross-validation folds
```

### Metrics

```text
Cross-validation accuracy
Cross-validation standard deviation
Accuracy
Macro precision
Macro recall
Macro F1
```

### Metadata

```text
Project
Model type
Dataset SHA-256
Prediction target
ML framework
```

This allows individual model versions to be traced back to the experiment and dataset that produced them.

## Model Registry

Successful training runs create versions of the registered model:

```text
global-household-financial-health
```

Example:

```text
Version 1
Version 2
Version 3
Version 4
```

Model versions are retained so model history remains auditable.

The project uses the MLflow model alias:

```text
champion
```

to identify the model currently approved for inference.

Inference therefore loads:

```text
models:/global-household-financial-health@champion
```

rather than hard-coding a specific model version.

## Quality Gate

Model promotion is controlled through automated quality thresholds.

Current thresholds are:

```text
Accuracy >= 0.93
Macro F1 >= 0.93
```

The lifecycle is:

```text
Candidate Model
      |
      v
Evaluation
      |
      v
Quality Gate
   /       \
PASS       FAIL
 |           |
 v           v
Champion   Rejected
```

A candidate that fails the quality gate is not assigned the champion alias.

A failed quality gate also causes the CI training process to return a failure status.

## Inference

Production-style inference is implemented in:

```text
src/models/predict.py
```

Inference resolves the model through the `champion` registry alias.

This decouples application code from individual model versions.

For example, moving the champion alias from version 4 to version 5 does not require modification of inference code.

## Testing

The project contains multiple test levels.

Unit tests validate individual components including:

```text
Data validation
Feature engineering
Quality gates
Prediction logic
```

Integration tests verify that feature engineering, preprocessing and XGBoost training work together correctly.

The testing strategy separates local registry integration tests from unit tests so tests do not unnecessarily depend on external services.

## GitHub Actions CI

ML training automation is implemented in:

```text
.github/workflows/ml-training.yml
```

The workflow performs:

```text
Git push / Pull request
        |
        v
Checkout repository
        |
        v
Set up Python environment
        |
        v
Install dependencies
        |
        v
Run unit tests
        |
        v
Validate dataset
        |
        v
Start temporary MLflow server
        |
        v
Train model
        |
        v
Evaluate model
        |
        v
Apply quality gate
        |
        v
Run integration tests
        |
        v
Upload MLflow logs
```

The GitHub Actions environment uses a temporary MLflow tracking server.

This CI registry is intentionally ephemeral and is used to verify that the training workflow can be reproduced from a clean environment.

The persistent local MLflow registry remains the development registry.

## Current Environment Strategy

```text
Local Development
        |
        v
Local MLflow
        |
        v
Git / GitHub
        |
        v
GitHub Actions
        |
        v
Automated CI Validation
```

The project deliberately uses a local-first development approach to minimize cloud costs.

## Planned Azure Production Mapping

Later stages will map the local implementation to Microsoft Azure.

```text
Current Local Component        Azure Production Component

Local MLflow                   Azure ML experiment tracking
MLflow Model Registry          Azure ML model registry
Local training                 Azure ML jobs
Local inference                Azure ML managed online endpoint
Local monitoring              Azure Monitor / Application Insights
GitHub Actions CI              GitHub Actions CI/CD
Local configuration            Azure ML environments
Bicep                          Azure infrastructure provisioning
```

Azure resources will be provisioned using Infrastructure as Code and used only for short-lived deployment and demonstration purposes.

## MLOps Skills Demonstrated

This implementation demonstrates:

```text
Data validation
Feature engineering
Training reproducibility
Experiment tracking
Data lineage
Model evaluation
Model signatures
Model versioning
Model registry
Quality gates
Champion model promotion
Registry-based inference
Unit testing
Integration testing
GitHub Actions CI
Production-oriented ML lifecycle
```

The next cloud stage will extend this lifecycle with Azure Machine Learning registration, deployment, monitoring and Infrastructure as Code.
