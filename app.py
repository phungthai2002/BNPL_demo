from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# =====================================================
# Load Artifacts
# =====================================================

import sklearn
print("Current scikit-learn version:", sklearn.__version__)

model = joblib.load("models/logistic_regression.pkl")

# Temporary fix for sklearn version mismatch
if not hasattr(model, "multi_class"):
    model.multi_class = "auto"

scaler = joblib.load("models/scaler.pkl")
encoders = joblib.load("models/label_encoders.pkl")
selected_features = joblib.load("models/selected_features.pkl")



# =====================================================
# Feature Engineering
# =====================================================

def build_features(data):

    age = int(data["age"])
    credit_score = float(data["credit_score"])
    monthly_income = float(data["monthly_income"])
    purchase_amount = float(data["purchase_amount"])
    installments = int(data["bnpl_installments"])

    # User may enter 23 for 23%, convert to 0.23
    debt_ratio = purchase_amount / max(monthly_income, 1)
    if debt_ratio > 1:
        debt_ratio = debt_ratio / 100

    # Encode employment type safely
    employment_value = data["employment_type"]

    if "employment_type" in encoders:
        encoder = encoders["employment_type"]

        if employment_value in encoder.classes_:
            employment_encoded = encoder.transform([employment_value])[0]
        else:
            employment_encoded = encoder.transform([encoder.classes_[0]])[0]
    else:
        employment_encoded = 0

    # Feature engineering
    installment_amount = purchase_amount / max(installments, 1)
    income_per_installment = monthly_income / max(installments, 1)
    affordability_gap = monthly_income - installment_amount
    purchase_income_ratio = purchase_amount / max(monthly_income, 1)

    high_credit = 1 if credit_score >= 650 else 0
    young_customer = 1 if age <= 25 else 0

    # Build by feature name, not by manual order
    feature_values = {
        "age": age,
        "credit_score": credit_score,
        "monthly_income": monthly_income,
        "purchase_amount": purchase_amount,
        "debt_to_income_ratio": debt_ratio,
        "employment_type": employment_encoded,
        "bnpl_installments": installments,
        "installment_amount": installment_amount,
        "income_per_installment": income_per_installment,
        "affordability_gap": affordability_gap,
        "purchase_income_ratio": purchase_income_ratio,
        "high_credit": high_credit,
        "young_customer": young_customer
    }

    features = pd.DataFrame([feature_values])

    # Force exact model feature order
    features = features.reindex(columns=selected_features, fill_value=0)

    print("\nSelected features:")
    print(selected_features)

    print("\nFeatures sent to model:")
    print(features)

    return features
# =====================================================
# Risk Explanation
# =====================================================

def explain(data):

    explanation = []

    credit_score = float(data["credit_score"])
    monthly_income = float(data["monthly_income"])
    purchase_amount = float(data["purchase_amount"])
    age = int(data["age"])

    debt_ratio = purchase_amount / max(monthly_income, 1)

    if credit_score < 600:
        explanation.append("Low credit score increases default risk.")

    if debt_ratio > 0.40:
        explanation.append("High purchase-to-income ratio.")

    if purchase_amount > 3000:
        explanation.append("Large purchase amount.")

    if age <= 25:
        explanation.append("Young customers usually have higher credit risk.")

    if len(explanation) == 0:
        explanation.append("Customer profile appears financially stable.")

    return explanation


# =====================================================
# Home
# =====================================================

@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/prediction")
def prediction_page():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard_redirect():
    return render_template("dashboard.html")

# =====================================================
# Prediction API
# =====================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        features = build_features(data)

        features_scaled = scaler.transform(features)

        prediction = model.predict(features_scaled)[0]

        probability = model.predict_proba(features_scaled)[0][1]

        if probability < 0.30:
            risk = "Low Risk"
            recommended_action = "Approve"

        elif probability < 0.60:
            risk = "Medium Risk"
            recommended_action = "Review"

        else:
            risk = "High Risk"
            recommended_action = "Monitor / Manual Review"

        prediction_text = (
            "Default"
            if prediction == 1
            else "Non-Default"
        )

        return jsonify({

            "prediction": int(prediction),

            "prediction_text": prediction_text,

            "probability": round(float(probability * 100), 2),

            "risk_level": risk,

            "recommended_action": recommended_action,

            "explanation": explain(data)

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 400


# =====================================================
# Run Flask
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)
