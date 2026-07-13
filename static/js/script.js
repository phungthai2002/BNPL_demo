const form = document.getElementById("predictForm");

const loading = document.getElementById("loading");
const result = document.getElementById("result");

const predictionText = document.getElementById("predictionText");
const probability = document.getElementById("probability");
const riskLevel = document.getElementById("riskLevel");
const recommendedAction = document.getElementById("recommendedAction");

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    loading.style.display = "block";
    result.style.display = "none";

    const inputData = {
        age: Number(document.getElementById("age").value),
        credit_score: Number(document.getElementById("credit_score").value),
        monthly_income: Number(document.getElementById("monthly_income").value),
        purchase_amount: Number(document.getElementById("purchase_amount").value),
        employment_type: document.getElementById("employment_type").value,
        bnpl_installments: Number(document.getElementById("bnpl_installments").value)
    };

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(inputData)
        });

        const res = await response.json();

        loading.style.display = "none";
        result.style.display = "block";

        if (!response.ok || res.error) {
            predictionText.innerHTML = "Prediction Failed";
            probability.innerHTML = "--";
            riskLevel.innerHTML = "--";
            recommendedAction.innerHTML = "--";

            console.error("Prediction error:", res);
            return;
        }

        predictionText.innerHTML = res.prediction_text;
        probability.innerHTML = res.probability + "%";
        riskLevel.innerHTML = res.risk_level;
        recommendedAction.innerHTML = res.recommended_action;

        riskLevel.className = "";

        if (res.risk_level === "Low Risk") {
            riskLevel.classList.add("low");
        } else if (res.risk_level === "Medium Risk") {
            riskLevel.classList.add("medium");
        } else {
            riskLevel.classList.add("high");
        }

    } catch (error) {
        loading.style.display = "none";
        result.style.display = "block";

        predictionText.innerHTML = "Server Error";
        probability.innerHTML = "--";
        riskLevel.innerHTML = "--";
        recommendedAction.innerHTML = "--";

        console.error("Frontend error:", error);
    }
});