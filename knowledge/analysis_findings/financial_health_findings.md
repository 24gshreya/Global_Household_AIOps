# Financial Health Findings

## Savings and Expense Rates

Savings rate and expense ratio vary considerably across households.
Expense ratio is typically inversely related to financial health. Households with higher expense ratios generally show poorer financial-health outcomes.

## Financial Risk Share

A meaningful share of households falls into financially vulnerable clusters.
These households are generally characterised by:
- Low savings rate
- High expense ratio relative to income
- Limited financial resilience

## Income as a Protective Factor

Income is the strongest protective factor against poor financial health across the dataset.
Higher household income generally reduces the likelihood that a household will fall into financially vulnerable categories.

## Monthly Savings as a Risk Indicator

Low monthly savings is a primary risk indicator associated with poor household financial health.
SHAP analysis identified low monthly savings as an important contributor toward classification into the Poor financial-health category.

## Financial Health Classification

An XGBoost classification model was developed to classify households into:
- Poor
- Fair
- Good
The original analysis reported approximately 97% cross-validation accuracy and ROC-AUC close to 0.999.

> Note: These results refer to the original experimental analysis. The productionised MLOps model uses a revised feature set and has separate evaluation metrics.

## Feature Importance

The strongest predictors of household financial-health category in the original analysis were:
1. Savings rate
2. Expense ratio
3. Income per earner

## SHAP Explainability

SHAP analysis showed that:
- Low monthly savings pushes predictions toward the Poor financial-health category.
- High expense ratio pushes predictions toward Poor.
- Higher income per earner pushes predictions toward Good.