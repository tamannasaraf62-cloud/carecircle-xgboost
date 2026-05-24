import joblib
import numpy as np


MODEL_PATH = "models/disease_model.pkl"
ENCODER_PATH = "models/disease_label_encoder.pkl"


def predict_top_diseases(symptoms_text, top_n=3):
    model = joblib.load(MODEL_PATH)
    encoder = joblib.load(ENCODER_PATH)

    probabilities = model.predict_proba([symptoms_text])[0]
    top_indexes = np.argsort(probabilities)[::-1][:top_n]

    results = []

    for index in top_indexes:
        disease = encoder.inverse_transform([index])[0]
        confidence = round(float(probabilities[index]) * 100, 2)

        results.append(
            {
                "disease": disease,
                "confidence_percent": confidence
            }
        )

    return results


if __name__ == "__main__":
    print("\nDisease Prediction System")
    print("=" * 40)

    symptoms = input("Enter symptoms: ")

    diseases = predict_top_diseases(symptoms)

    print("\nTop 3 Disease Predictions")
    print("=" * 40)

    for rank, disease in enumerate(diseases, start=1):
        print(
            f"{rank}. {disease['disease']} "
            f"- {disease['confidence_percent']}% confidence"
        )

    print("\nDisclaimer: Educational project only. Not medical advice.")