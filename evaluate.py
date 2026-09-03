import pandas as pd
from model import predict_acronym


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("dataset.csv")

print("Dataset loaded successfully!")
print("Total records:", len(df))


# ==========================================
# 2. PREPROCESS DATA
# ==========================================

df["acronym"] = df["acronym"].astype(str).str.strip().str.upper()
df["full_form"] = df["full_form"].astype(str).str.strip()


# ==========================================
# 3. SELECT TEST DATA
# ==========================================

# We will evaluate the first 40 records
# from the dataset.

test_data = df.head(40)

print("\nTotal test records:", len(test_data))


# ==========================================
# 4. INITIALIZE COUNTERS
# ==========================================

correct_predictions = 0
incorrect_predictions = 0

total_predictions = len(test_data)


# ==========================================
# 5. TEST EACH ACRONYM
# ==========================================

print("\n========================================")
print("MODEL EVALUATION")
print("========================================")


for _, row in test_data.iterrows():

    acronym = row["acronym"]
    actual_full_form = row["full_form"]

    # Get prediction from model
    results = predict_acronym(acronym)

    predicted_full_form = ""

    if results:

        # Take the first prediction
        predicted_full_form = results[0]["full_form"]


    # Compare actual and predicted answer

    if predicted_full_form.lower() == actual_full_form.lower():

        correct_predictions += 1

        status = "CORRECT"

    else:

        incorrect_predictions += 1

        status = "INCORRECT"


    # Display result

    print("\nAcronym:", acronym)
    print("Actual:", actual_full_form)
    print("Predicted:", predicted_full_form)
    print("Status:", status)


# ==========================================
# 6. CALCULATE ACCURACY
# ==========================================

accuracy = (
    correct_predictions / total_predictions
) * 100


# ==========================================
# 7. DISPLAY FINAL RESULTS
# ==========================================

print("\n========================================")
print("FINAL EVALUATION RESULTS")
print("========================================")

print(
    "Total test records:",
    total_predictions
)

print(
    "Correct predictions:",
    correct_predictions
)

print(
    "Incorrect predictions:",
    incorrect_predictions
)

print(
    "Accuracy:",
    round(accuracy, 2),
    "%"
)

print("========================================")