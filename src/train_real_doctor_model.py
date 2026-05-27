import os
import joblib
import pandas as pd

from xgboost import XGBClassifier

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.model_selection import train_test_split


DATA_PATH = "data/doctor_real_data.csv"

MODEL_PATH = "models/real_doctor_model.pkl"
ENCODER_PATH = "models/real_label_encoder.pkl"
DISEASE_ENCODER_PATH = "models/disease_label_encoder.pkl"


DISEASE_SPECIALIST_MAP = {
    "Fungal infection": "Dermatologist",
    "Allergy": "General Physician",
    "GERD": "Gastroenterologist",
    "Chronic cholestasis": "Gastroenterologist",
    "Drug Reaction": "General Physician",
    "Peptic ulcer diseae": "Gastroenterologist",
    "AIDS": "Infectious Disease Specialist",
    "Diabetes": "Endocrinologist",
    "Hypertension": "Cardiologist",
    "Migraine": "Neurologist",
    "Cervical spondylosis": "Orthopedic",
    "Paralysis (brain hemorrhage)": "Neurologist",
    "Jaundice": "Hepatologist",
    "Malaria": "General Physician",
    "Chicken pox": "General Physician",
    "Dengue": "General Physician",
    "Typhoid": "General Physician",
    "Hepatitis A": "Hepatologist",
    "Tuberculosis": "Pulmonologist",
    "Heart attack": "Cardiologist",
    "Pneumonia": "Pulmonologist",
    "Arthritis": "Orthopedic",
    "Acne": "Dermatologist"
}


def combine_symptoms(row):
    symptoms = []

    for column in row.index:
        if "Symptom" in column and pd.notna(row[column]):
            symptoms.append(str(row[column]))

    return " ".join(symptoms)


def train_real_model():
    df = pd.read_csv(DATA_PATH)

    print("\nOriginal Dataset Shape:")
    print(df.shape)

    df["all_symptoms"] = df.apply(combine_symptoms, axis=1)

    df["specialist"] = df["Disease"].map(DISEASE_SPECIALIST_MAP)

    df = df.dropna(subset=["specialist"])

    print("\nFiltered Dataset Shape:")
    print(df.shape)

    x = df["all_symptoms"]
    y = df["specialist"]

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

    print("\nTraining XGBoost model...")

    model.fit(x_train, y_train)

    predictions = model.predict(x_test)

    accuracy = accuracy_score(y_test, predictions)

    print("\nMODEL RESULTS")
    print("=" * 50)

    print(f"\nAccuracy: {accuracy:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=label_encoder.classes_
        )
    )

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    os.makedirs("models", exist_ok=True)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(label_encoder, ENCODER_PATH)

    print("\nSaved Model:")
    print(MODEL_PATH)

    print("\nSaved Label Encoder:")
    print(ENCODER_PATH)


if __name__ == "__main__":
    train_real_model()