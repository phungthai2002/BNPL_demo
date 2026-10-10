# BNPL Credit Risk Decision Support System

A FinTech portfolio project that combines **Power BI analytics** with a **machine learning prediction app** to explore credit risk in Buy Now Pay Later (BNPL) transactions.

**[Live Demo](https://bnpl-demo.onrender.com/)**

## Project Motivation

Buy Now Pay Later allows customers to spread a purchase across several payments. Assessing repayment risk requires considering both the customer's financial profile and the transaction itself.

This project demonstrates how business intelligence and machine learning can be presented together in a practical decision support interface. It illustrates a workflow from exploring risk patterns to reviewing a specific transaction.

## Key Features

### Interactive Power BI Dashboard

The embedded Power BI report provides several analytical views:

- **Executive Overview** — a starting point for exploring the report.
- **Customer Risk Analysis** — customer risk patterns across income groups, employment types, credit score bands, and purchase-to-income ratio measures.
- **Transaction Risk** — purchase value, product category, installment plans, default rates, and risk distributions.
- **Repayment Performance** — a dedicated report page for repayment analysis.
- **Model Insights & Decision Support** — a dedicated report page for model-related analysis.

The dashboard includes filters and visualizations for exploring customer and transaction segments.

The Power BI report is hosted separately and embedded in the Flask application. Its original Power BI source file is not included in this repository.

### Individual Credit Risk Prediction

The prediction form accepts six inputs:

| Input | Description |
| --- | --- |
| Age | Customer age |
| Credit score | Customer credit score |
| Monthly income | Monthly income in USD, as labeled in the interface |
| Purchase amount | BNPL purchase value in USD, as labeled in the interface |
| Employment type | Salaried, Self-Employed, Student, or Unemployed |
| BNPL installments | 3, 6, 9, or 12 installments |

The application returns:

- A **Default / Non-Default** classification
- An **estimated default probability**
- A **Low / Medium / High Risk** category
- A **suggested action** based on probability thresholds

| Estimated default probability | Risk level | Suggested action |
| --- | --- | --- |
| Below 30% | Low Risk | Approve |
| 30% to below 60% | Medium Risk | Review |
| 60% or above | High Risk | Monitor / Manual Review |

These thresholds are demonstration rules implemented in the application. The classification comes from the model's `predict()` output, while the risk level and suggested action are assigned separately from `predict_proba()`.

## Technology Stack

| Layer | Technologies | Purpose |
| --- | --- | --- |
| Backend | Python, Flask | Page rendering and prediction API |
| Machine learning | scikit-learn | Model inference and preprocessing |
| Data processing | pandas, NumPy | Feature construction and numerical operations |
| Model artifacts | joblib | Loading serialized models, encoders, scaler, and feature list |
| Frontend | HTML, CSS, JavaScript | Input form, API calls, and result display |
| Business intelligence | Microsoft Power BI | Embedded interactive report |
| Hosting | Render | Public deployment |
| WSGI server | Gunicorn | Serving the Flask application in production |

Dependency versions are pinned in `requirements.txt`.

## How Prediction Works

1. The frontend collects customer and transaction inputs.
2. The form sends the data as JSON to the `POST /predict` endpoint.
3. The backend converts numerical inputs and encodes the employment type.
4. Additional features are constructed, including:
   - Installment amount
   - Purchase-to-income ratio
   - Affordability gap
   - High credit score indicator
   - Young customer indicator
5. The feature table is aligned with the saved `selected_features` list.
6. The saved scaler transforms the feature values.
7. The Logistic Regression model produces:
   - A default or non-default classification
   - An estimated default probability
8. The backend assigns a risk level and suggested action.
9. The results are returned to the frontend and displayed to the user.

The repository also contains Decision Tree and Random Forest model artifacts. The current application loads only `logistic_regression.pkl`. It does not currently provide model switching or live model comparison.

## Repository Contents

| Path | Purpose |
| --- | --- |
| `app.py` | Flask routes, feature engineering, preprocessing, and inference |
| `requirements.txt` | Python dependencies |
| `templates/dashboard.html` | Embedded Power BI report page |
| `templates/index.html` | Credit risk prediction interface |
| `static/css/style.css` | Prediction interface styling |
| `static/js/script.js` | Form handling and asynchronous prediction requests |
| `models/logistic_regression.pkl` | Active prediction model |
| `models/decision_tree.pkl` | Additional stored model artifact |
| `models/random_forest.pkl` | Additional stored model artifact |
| `models/scaler.pkl` | Saved numerical preprocessing artifact |
| `models/label_encoders.pkl` | Saved categorical encoders |
| `models/selected_features.pkl` | Feature names and ordering used during inference |

## Run Locally

Clone the repository and enter its root directory:

```bash
git clone https://github.com/phungthai2002/BNPL_demo.git
cd BNPL_demo
