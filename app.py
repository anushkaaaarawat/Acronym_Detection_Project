from flask import Flask, render_template, request
from model import predict_acronym


# Create Flask application
app = Flask(__name__)


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    results = None
    message = None
    user_input = ""

    # When user clicks the button
    if request.method == "POST":

        user_input = request.form.get("acronym", "")

        results = predict_acronym(user_input)

        # If acronym is not found
        if results is None:

            message = (
                "No suitable acronym was found. "
                "Please enter a valid technology or engineering acronym."
            )


    return render_template(
        "index.html",
        results=results,
        message=message,
        user_input=user_input
    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )