import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="CareCircle XGBoost API")

DOCTOR_MODEL_PATH = "models/doctor_model.pkl"
DOCTOR_ENCODER_PATH = "models/doctor_label_encoder.pkl"
HOSPITAL_DATA_PATH = "data/hospital_data.csv"

doctor_model = joblib.load(DOCTOR_MODEL_PATH)
doctor_encoder = joblib.load(DOCTOR_ENCODER_PATH)


class RecommendationRequest(BaseModel):
    symptoms: str
    disease: str
    location: str


def recommend_doctor(symptoms: str, disease: str) -> str:
    input_text = symptoms + " " + disease

    prediction = doctor_model.predict([input_text])[0]
    specialization = doctor_encoder.inverse_transform([prediction])[0]

    return specialization


def recommend_best_hospital(location: str, specialization: str) -> dict:
    hospitals = pd.read_csv(HOSPITAL_DATA_PATH)

    matched_hospitals = hospitals[
        (hospitals["location"].str.lower() == location.lower())
        & (hospitals["specialization"].str.lower() == specialization.lower())
    ]

    if matched_hospitals.empty:
        matched_hospitals = hospitals[
            hospitals["specialization"].str.lower() == specialization.lower()
        ]

    if matched_hospitals.empty:
        return {
            "hospital_name": "No matching hospital found",
            "rating": None,
            "emergency_available": None,
            "waiting_time_hours": None
        }

    matched_hospitals = matched_hospitals.copy()

    matched_hospitals["recommendation_score"] = (
        matched_hospitals["rating"] * 2
        + matched_hospitals["emergency_available"] * 1.5
        - matched_hospitals["waiting_time_hours"] * 0.3
    )

    best_hospital = matched_hospitals.sort_values(
        by="recommendation_score",
        ascending=False
    ).iloc[0]

    return {
        "hospital_name": best_hospital["hospital_name"],
        "rating": float(best_hospital["rating"]),
        "emergency_available": int(best_hospital["emergency_available"]),
        "waiting_time_hours": int(best_hospital["waiting_time_hours"])
    }


@app.get("/")
def home():
    return {
        "message": "CareCircle XGBoost API is running",
        "note": "Educational project only. Not medical advice."
    }


@app.post("/recommend")
def recommend(request: RecommendationRequest):
    specialization = recommend_doctor(
        symptoms=request.symptoms,
        disease=request.disease
    )

    hospital = recommend_best_hospital(
        location=request.location,
        specialization=specialization
    )

    return {
        "doctor_specialization": specialization,
        "recommended_hospital": hospital,
        "disclaimer": "Educational project only. Not medical advice."
    }