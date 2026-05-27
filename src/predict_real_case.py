import joblib
import numpy as np


MODEL_PATH = "models/real_doctor_model.pkl"
ENCODER_PATH = "models/real_label_encoder.pkl"


def predict_top_specialists(symptoms_text, top_n=3):
    model = joblib.load(MODEL_PATH)
    encoder = joblib.load(ENCODER_PATH)

    probabilities = model.predict_proba([symptoms_text])[0]

    top_indexes = np.argsort(probabilities)[::-1][:top_n]

    results = []

    for index in top_indexes:
        specialist = encoder.inverse_transform([index])[0]
        confidence = probabilities[index]

        results.append(
            {
                "specialist": specialist,
                "confidence": round(float(confidence), 4)
            }
        )

    return results


if __name__ == "__main__":
    print("\nREAL MEDICAL SPECIALIST PREDICTION")
    print("=" * 50)

    symptoms = input("\nEnter symptoms: ")

    recommendations = predict_top_specialists(symptoms)

    print("\nTOP 3 SPECIALIST RECOMMENDATIONS")
    print("=" * 50)

    for number, result in enumerate(recommendations, start=1):
        print(
            f"{number}. {result['specialist']} "
            f"- Confidence: {result['confidence']}"
        )

    print("\nDisclaimer:")
    print("Educational project only. Not medical advice.")