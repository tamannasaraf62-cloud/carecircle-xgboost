import joblib
import numpy as np
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="CareCircle Final Recommendation API")

DOCTOR_MODEL_PATH = "models/real_doctor_model.pkl"
DOCTOR_ENCODER_PATH = "models/real_label_encoder.pkl"
HOSPITAL_DATA_PATH = "data/hospital_data.csv"

doctor_model = joblib.load(DOCTOR_MODEL_PATH)
doctor_encoder = joblib.load(DOCTOR_ENCODER_PATH)


class FinalRecommendationRequest(BaseModel):
    symptoms: str
    location: str


def predict_top_specialists(symptoms_text: str, top_n: int = 3):
    probabilities = doctor_model.predict_proba([symptoms_text])[0]
    top_indexes = np.argsort(probabilities)[::-1][:top_n]

    results = []

    for index in top_indexes:
        specialist = doctor_encoder.inverse_transform([index])[0]

        results.append(
            {
                "specialist": specialist,
                "confidence": round(float(probabilities[index]), 4)
            }
        )

    return results


def recommend_top_hospitals(location: str, specialization: str, top_n: int = 3):
    hospitals = pd.read_csv(HOSPITAL_DATA_PATH)

    matched = hospitals[
        (hospitals["location"].str.lower() == location.lower())
        & (hospitals["specialization"].str.lower() == specialization.lower())
    ]

    if matched.empty:
        matched = hospitals[
            hospitals["specialization"].str.lower() == specialization.lower()
        ]

    if matched.empty:
        return []

    matched = matched.copy()

    matched["recommendation_score"] = (
        matched["rating"] * 2
        + matched["emergency_available"] * 1.5
        - matched["waiting_time_hours"] * 0.3
    )

    matched = matched.sort_values(
        by="recommendation_score",
        ascending=False
    )

    results = []

    for _, row in matched.head(top_n).iterrows():
        results.append(
            {
                "hospital_name": row["hospital_name"],
                "location": row["location"],
                "rating": float(row["rating"]),
                "emergency_available": int(row["emergency_available"]),
                "waiting_time_hours": int(row["waiting_time_hours"]),
                "recommendation_score": round(float(row["recommendation_score"]), 2)
            }
        )

    return results


@app.get("/")
def home():
    return {
        "message": "CareCircle Final API is running",
        "note": "Educational project only. Not medical advice."
    }


@app.post("/final-recommendation")
def final_recommendation(request: FinalRecommendationRequest):
    specialists = predict_top_specialists(request.symptoms)

    best_specialist = specialists[0]["specialist"]

    hospitals = recommend_top_hospitals(
        location=request.location,
        specialization=best_specialist
    )

    return {
        "input_symptoms": request.symptoms,
        "input_location": request.location,
        "top_3_specialists": specialists,
        "best_specialist_used_for_hospital_search": best_specialist,
        "recommended_hospitals": hospitals,
        "disclaimer": "Educational project only. Not medical advice."
    }
