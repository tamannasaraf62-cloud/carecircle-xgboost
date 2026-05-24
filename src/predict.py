import joblib
import pandas as pd


DOCTOR_MODEL_PATH = "models/doctor_model.pkl"
DOCTOR_ENCODER_PATH = "models/doctor_label_encoder.pkl"
HOSPITAL_DATA_PATH = "data/hospital_data.csv"


def recommend_doctor(symptoms, disease):
    doctor_model = joblib.load(DOCTOR_MODEL_PATH)
    doctor_encoder = joblib.load(DOCTOR_ENCODER_PATH)

    input_text = symptoms + " " + disease

    prediction = doctor_model.predict([input_text])[0]
    specialization = doctor_encoder.inverse_transform([prediction])[0]

    return specialization


def recommend_best_hospital(location, specialization):
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
        return "No matching hospital found"

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

    return best_hospital["hospital_name"]


if __name__ == "__main__":
    print("\nCareCircle Recommendation System")
    print("Educational project only. Not medical advice.\n")

    symptoms = input("Enter symptoms: ")
    disease = input("Enter known/possible disease: ")
    location = input("Enter location: ")

    specialization = recommend_doctor(symptoms, disease)
    hospital_name = recommend_best_hospital(location, specialization)

    print("\nRecommendation Result")
    print("=====================")
    print(f"Recommended Doctor Specialization: {specialization}")
    print(f"Recommended Hospital: {hospital_name}")
    print("\nDisclaimer: This is for learning only, not medical advice.")