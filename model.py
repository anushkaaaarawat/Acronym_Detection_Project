import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("dataset.csv")

print("Dataset loaded successfully!")
print("Number of records:", len(df))


# ==========================================
# 2. DATA PREPROCESSING
# ==========================================

df["acronym"] = df["acronym"].astype(str).str.strip().str.upper()
df["full_form"] = df["full_form"].astype(str).str.strip()
df["category"] = df["category"].astype(str).str.strip()
df["level"] = df["level"].astype(str).str.strip()


# Combine acronym and full form for NLP processing
df["text"] = df["acronym"] + " " + df["full_form"]


# ==========================================
# 3. TF-IDF VECTORIZATION
# ==========================================

vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(1, 3)
)

tfidf_matrix = vectorizer.fit_transform(df["text"])


# ==========================================
# 4. ACRONYM PREDICTION FUNCTION
# ==========================================

def predict_acronym(user_input):

    # Clean user input
    user_input = str(user_input).strip().upper()

    # If user enters nothing
    if not user_input:
        return None


    # ======================================
    # EXACT MATCH
    # ======================================

    exact_match = df[df["acronym"] == user_input]

    if not exact_match.empty:

        results = []

        for _, row in exact_match.iterrows():

            results.append({
                "acronym": row["acronym"],
                "full_form": row["full_form"],
                "category": row["category"],
                "level": row["level"]
            })

        return results


    # ======================================
    # NLP: TF-IDF + COSINE SIMILARITY
    # ======================================

    user_vector = vectorizer.transform([user_input])

    similarities = cosine_similarity(
        user_vector,
        tfidf_matrix
    )[0]

    max_similarity = similarities.max()


    # ======================================
    # SIMILARITY THRESHOLD
    # ======================================

    THRESHOLD = 0.60

    # Reject unrelated words such as LOL
    if max_similarity < THRESHOLD:
        return None


    # Get the best matching record
    best_index = similarities.argmax()


    return [{
        "acronym": df.iloc[best_index]["acronym"],
        "full_form": df.iloc[best_index]["full_form"],
        "category": df.iloc[best_index]["category"],
        "level": df.iloc[best_index]["level"]
    }]


# ==========================================
# 5. TEST MODEL DIRECTLY
# ==========================================

if __name__ == "__main__":

    print("\nTesting the model...\n")

    test_inputs = [
        "CPU",
        "NLP",
        "CNN",
        "CFC",
        "CFD",
        "cpu",
        "LOL"
    ]

    for test in test_inputs:

        print("Input:", test)

        result = predict_acronym(test)

        if result:

            for item in result:

                print(
                    item["acronym"],
                    "->",
                    item["full_form"]
                )

                print("Category:", item["category"])
                print("Level:", item["level"])

        else:

            print("No suitable acronym found.")

        print("-" * 50)