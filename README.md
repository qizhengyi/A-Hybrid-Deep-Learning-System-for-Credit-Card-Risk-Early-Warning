# CardGuard
### A Hybrid Deep Learning System for Credit Card Risk Early Warning

## Overview
CardGuard is an end-to-end machine learning project for credit card risk early warning.
It predicts customer default risk by combining:
- Traditional statistical models
- Tree-based models
- Transformer-based deep learning models (PyTorch)

The project is designed to simulate real-world financial risk modeling pipelines used in banks and fintech companies.

---

## Key Features
- SQL-style data extraction and preprocessing
- Feature engineering for credit risk modeling
- Baseline models:
  - Logistic Regression
  - Decision Tree
- Deep learning model:
  - Transformer for sequential transaction data
- Model comparison with financial risk metrics
- Clean, modular, and reproducible codebase

---

## Tech Stack
- **Python**
- **PyTorch**
- **scikit-learn**
- **SQL (via pandas / SQLite simulation)**
- **NumPy / Pandas / Matplotlib**

---

## Data
Public credit card and financial datasets (e.g. UCI Credit Card Default Dataset).
The pipeline supports extension to large-scale relational databases.

---

## Modeling Pipeline
1. Data ingestion (SQL-style queries)
2. Data cleaning & feature engineering
3. Baseline risk models (Logistic Regression, Decision Tree)
4. Transformer-based sequential modeling (PyTorch)
5. Model evaluation & comparison

---

## Evaluation Metrics
- AUC-ROC
- KS Statistic
- Precision / Recall
- Time-based validation

---

## Project Structure
