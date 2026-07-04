from flask import Flask, render_template, request, send_file
import joblib
import numpy as np
from utils.pdf_generator import generate_pdf

app = Flask(__name__)

# Load models once
svm_model = joblib.load("model/sv_load.lb")
log_model = joblib.load("model/log_load.lb")

# Store latest prediction
latest_prediction = {}
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/prediction", methods=["GET", "POST"])
def prediction():

    result = None
    selected_model = None

    if request.method == "POST":

        income = float(request.form["income"])
        credit_score = float(request.form["credit_score"])
        loan_amount = float(request.form["loan_amount"])
        points = float(request.form["points"])

        selected_model = request.form["model"]

        data = np.array([[income,
                          credit_score,
                          loan_amount,
                          points]])

        if selected_model == "svm":
            prediction = svm_model.predict(data)
            model_name = "Support Vector Machine"

        else:
            prediction = log_model.predict(data)
            model_name = "Logistic Regression"

        if prediction[0] == 1:
            result = "✅ Loan Approved"

        else:
            result = "❌ Loan Rejected"
        global latest_prediction

        latest_prediction = {
            "model": model_name,
            "income": income,
            "credit_score": credit_score,
            "loan_amount": loan_amount,
            "points": points,
            "result": result
            }
        prediction_data = {
            "income": income,
            "credit_score": credit_score,
            "loan_amount": loan_amount,
            "points": points
        }

        return render_template(
            "prediction.html",
            prediction=result,
            model=model_name,
            prediction_data=prediction_data
        )

    return render_template("prediction.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/download_pdf")
def download_pdf():

    if not latest_prediction:
        return "No prediction available."

    filename = generate_pdf(latest_prediction)

    return send_file(
        filename,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)