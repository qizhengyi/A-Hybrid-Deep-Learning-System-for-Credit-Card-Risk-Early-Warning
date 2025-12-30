# Credit Risk Early Warning System  
**SQL Feature Store · PyTorch Models · Backtesting & Monitoring**

This repository implements an end-to-end **credit risk early warning pipeline**, covering data ingestion, SQL-based feature engineering, model training, backtesting, and risk reporting.  
The project is designed to resemble a **production-style credit risk workflow** commonly used in financial institutions.

---

## 1. Problem Statement

The goal of this project is to **predict the Probability of Default (PD)** for credit card customers using historical behavioral data, and to convert model outputs into **actionable risk tiers** for early intervention.

Key objectives:
- Generate reproducible and auditable features using SQL
- Train multiple risk models, including deep learning models in PyTorch
- Evaluate models using industry-standard risk metrics
- Produce formal backtesting reports and monitoring artifacts

---

## 2. Data Source

- **Dataset**: *Default of Credit Card Clients (Taiwan)*
- **Provider**: UCI Machine Learning Repository
- **Sample Size**: 30,000 customers
- **Target**: Default in the next billing cycle (binary)

Raw data is **programmatically downloaded** and converted into CSV for reproducibility.  
Raw files are excluded from version control.

---

## 3. Feature Engineering (SQL-Driven)

All features are constructed using **SQL views** in DuckDB, simulating a production feature store.

Feature categories include:
- Credit utilization ratios
- Repayment ratios
- Delinquency frequency and severity
- Trend-based bill and payment deltas
- Six-month behavioral sequences for temporal modeling

This design ensures:
- Full auditability of feature definitions
- Consistent features across training and scoring
- Clear separation between data engineering and modeling

---

## 4. Models Implemented

| Model | Description |
|------|------------|
| Logistic Regression | Interpretable baseline (scorecard-style) |
| Decision Tree | Non-linear baseline |
| PyTorch MLP | Neural network for tabular risk modeling |
| PyTorch Transformer | Sequence model over 6 months of credit behavior |

The **Transformer-based model** achieved the strongest overall ranking performance in backtesting.

---

## 5. Backtesting Setup

- **Train/Test Split**: 80% / 20%
- The test set serves as an **out-of-time proxy**
- Model performance is evaluated on the hold-out set

### Evaluation Metrics
- ROC-AUC
- KS Statistic
- PR-AUC
- Brier Score (calibration)

---

## 6. Backtesting Results

A formal backtesting report has been generated in PDF format:

📄 **Backtesting Report**  
`reports/Credit_Risk_Backtesting_Report.pdf`

Summary results (Transformer model):

| Metric | Value |
|------|------|
| ROC-AUC | ~0.77 |
| KS | ~0.42 |
| PR-AUC | ~0.45 |
| Brier Score | ~0.16 |

These results indicate strong discriminatory power and acceptable probability calibration.

---

## 7. Risk Tiering

Predicted PDs are mapped into operational risk tiers:

- **Green**: Low risk
- **Amber**: Medium risk
- **Red**: High risk

Tier-level analysis shows **monotonic increases in default rates**, validating the effectiveness of the early warning framework.

A structured tier-level backtesting summary is exported as:

```text
data/processed/risk_backtest_report.csv
