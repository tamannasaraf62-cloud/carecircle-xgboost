import joblib
import numpy as np

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="CareCircle Real XGBoost API")

MODEL_PATH = "models/real_doctor_model.pkl"
ENCODER_PATH = "models/real_label_encoder.pkl"

doctor_model = joblib.load(MODEL_PATH)
doctor_encoder = joblib.load(ENCODER_PATH)


class SymptomRequest(BaseModel):
    symptoms: str


def predict_top_specialists(symptoms_text: str, top_n: int = 3):
    probabilities = doctor_model.predict_proba([symptoms_text])[0]

    top_indexes = np.argsort(probabilities)[::-1][:top_n]

    results = []

    for index in top_indexes:
        specialist = doctor_encoder.inverse_transform([index])[0]
        confidence = probabilities[index]

        results.append(
            {
                "specialist": specialist,
                "confidence": round(float(confidence), 4)
            }
        )

    return results


@app.get("/")
def home():
    return {
        "message": "CareCircle Real XGBoost API is running",
        "note": "Educational project only. Not medical advice."
    }


@app.post("/recommend-specialist")
def recommend_specialist(request: SymptomRequest):
    recommendations = predict_top_specialists(request.symptoms)

    return {
        "symptoms": request.symptoms,
        "top_3_specialist_recommendations": recommendations,
        "disclaimer": "Educational project only. Not medical advice."
    }