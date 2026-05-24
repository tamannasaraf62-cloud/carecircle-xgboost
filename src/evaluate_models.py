import joblib
import pandas as pd

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split


DATA_PATH = "data/doctor_real_data.csv"

DISEASE_MODEL_PATH = "models/disease_model.pkl"
DISEASE_ENCODER_PATH = "models/disease_label_encoder.pkl"

SPECIALIST_MODEL_PATH = "models/real_doctor_model.pkl"
SPECIALIST_ENCODER_PATH = "models/real_label_encoder.pkl"


def combine_symptoms(row):
    symptoms = []

    for column in row.index:
        if "Symptom" in column and pd.notna(row[column]):
            symptoms.append(str(row[column]).strip())

    return " ".join(symptoms)


def evaluate_disease_model():
    df = pd.read_csv(DATA_PATH)
    df["all_symptoms"] = df.apply(combine_symptoms, axis=1)

    x = df["all_symptoms"]
    y = df["Disease"]

    encoder = joblib.load(DISEASE_ENCODER_PATH)
    model = joblib.load(DISEASE_MODEL_PATH)

    y_encoded = encoder.transform(y)

    _, x_test, _, y_test = train_test_split(
        x,
        y_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_encoded
    )

    predictions = model.predict(x_test)

    print("\nDISEASE MODEL EVALUATION")
    print("=" * 50)
    print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=encoder.classes_
        )
    )

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, predictions))


def evaluate_specialist_model():
    df = pd.read_csv(DATA_PATH)
    df["all_symptoms"] = df.apply(combine_symptoms, axis=1)

    disease_specialist_map = {
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

    df["specialist"] = df["Disease"].map(disease_specialist_map)
    df = df.dropna(subset=["specialist"])

    x = df["all_symptoms"]
    y = df["specialist"]

    encoder = joblib.load(SPECIALIST_ENCODER_PATH)
    model = joblib.load(SPECIALIST_MODEL_PATH)

    y_encoded = encoder.transform(y)

    _, x_test, _, y_test = train_test_split(
        x,
        y_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_encoded
    )

    predictions = model.predict(x_test)

    print("\nSPECIALIST MODEL EVALUATION")
    print("=" * 50)
    print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=encoder.classes_
        )
    )

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, predictions))


if __name__ == "__main__":
    evaluate_disease_model()
    evaluate_specialist_model()