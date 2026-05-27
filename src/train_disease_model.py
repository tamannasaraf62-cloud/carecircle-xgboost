import os
import joblib
import pandas as pd
from xgboost import XGBClassifier

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


DATA_PATH = "data/doctor_real_data.csv"
MODEL_PATH = "models/disease_model.pkl"
ENCODER_PATH = "models/disease_label_encoder.pkl"


def combine_symptoms(row):
    symptoms = []

    for column in row.index:
        if "Symptom" in column and pd.notna(row[column]):
            symptoms.append(str(row[column]).strip())

    return " ".join(symptoms)


def train_disease_model():
    df = pd.read_csv(DATA_PATH)

    df["all_symptoms"] = df.apply(combine_symptoms, axis=1)

    x = df["all_symptoms"]
    y = df["Disease"]

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_encoded
    )

    model = Pipeline(
        steps=[
            ("vectorizer", TfidfVectorizer()),
            (
                "classifier",
                XGBClassifier(
                    n_estimators=300,
                    max_depth=6,
                    learning_rate=0.1,
                    eval_metric="mlogloss",
                    random_state=42
                )
            )
        ]
    )

    print("Training disease prediction model...")
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)

    print("\nDisease Model Results")
    print("=====================")
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, predictions, target_names=label_encoder.classes_))

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(label_encoder, ENCODER_PATH)

    print("\nSaved:")
    print(MODEL_PATH)
    print(ENCODER_PATH)


if __name__ == "__main__":
    train_disease_model()