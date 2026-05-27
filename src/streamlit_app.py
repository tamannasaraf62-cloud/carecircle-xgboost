import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import os
from datetime import datetime


HISTORY_PATH = "history/prediction_history.csv"
DOCTOR_MODEL_PATH = "models/real_doctor_model.pkl"
DOCTOR_ENCODER_PATH = "models/real_label_encoder.pkl"
HOSPITAL_DATA_PATH = "data/hospital_data.csv"
DISEASE_MODEL_PATH = "models/disease_model.pkl"
DISEASE_ENCODER_PATH = "models/disease_label_encoder.pkl"

@st.cache_resource
def load_doctor_model():
    model = joblib.load(DOCTOR_MODEL_PATH)
    encoder = joblib.load(DOCTOR_ENCODER_PATH)
    return model, encoder

@st.cache_resource
def load_disease_model():
    model = joblib.load(DISEASE_MODEL_PATH)
    encoder = joblib.load(DISEASE_ENCODER_PATH)
    return model, encoder

@st.cache_data
def load_hospital_data():
    return pd.read_csv(HOSPITAL_DATA_PATH)


def predict_top_specialists(symptoms_text, model, encoder, top_n=3):
    probabilities = model.predict_proba([symptoms_text])[0]
    top_indexes = np.argsort(probabilities)[::-1][:top_n]

    results = []

    for index in top_indexes:
        specialist = encoder.inverse_transform([index])[0]
        confidence = round(float(probabilities[index]) * 100, 2)

        results.append(
            {
                "specialist": specialist,
                "confidence_percent": confidence
            }
        )

    return results

def predict_top_diseases(symptoms_text, model, encoder, top_n=3):
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

def recommend_top_hospitals(location, specialization, hospitals, top_n=3):
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

def detect_emergency(symptoms_text):
    emergency_keywords = [
        "chest_pain",
        "breathlessness",
        "unconsciousness",
        "severe_bleeding",
        "heart_attack",
        "stroke",
        "difficulty_breathing",
        "seizure",
        "high_fever",
        "blurred_vision"
    ]

    symptoms_text = symptoms_text.lower()

    matched_keywords = []

    for keyword in emergency_keywords:
        if keyword in symptoms_text:
            matched_keywords.append(keyword)

    if len(matched_keywords) >= 2:
        return {
            "risk_level": "HIGH",
            "matched_keywords": matched_keywords
        }

    elif len(matched_keywords) == 1:
        return {
            "risk_level": "MEDIUM",
            "matched_keywords": matched_keywords
        }

    else:
        return {
            "risk_level": "LOW",
            "matched_keywords": []
        }

def save_prediction_history(symptoms, location, top_disease, top_specialist, risk_level):
    os.makedirs("history", exist_ok=True)

    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symptoms": symptoms,
        "location": location,
        "top_disease": top_disease,
        "top_specialist": top_specialist,
        "risk_level": risk_level
    }

    history_df = pd.DataFrame([row])

    if os.path.exists(HISTORY_PATH):
        history_df.to_csv(HISTORY_PATH, mode="a", header=False, index=False)
    else:
        history_df.to_csv(HISTORY_PATH, index=False)

def main():
    st.set_page_config(
        page_title="CareCircle ML Recommendation",
        page_icon="🏥",
        layout="wide"
    )

    st.title("🏥 CareCircle Doctor & Hospital Recommendation")
    st.write("XGBoost-based educational ML recommendation system")

    st.warning(
        "Disclaimer: This project is for educational purposes only. "
        "It is not a medical diagnosis system and should not replace professional medical advice."
    )

    doctor_model, doctor_encoder = load_doctor_model()
    disease_model, disease_encoder = load_disease_model()
    hospitals = load_hospital_data()

    st.sidebar.header("Patient Input")

    symptoms = st.sidebar.text_area(
        "Enter symptoms",
        value="chest_pain breathlessness sweating",
        height=120
    )

    location = st.sidebar.text_input(
        "Enter location",
        value="Delhi"
    )

    submitted = st.sidebar.button("Get Recommendation")

    if submitted:
        if not symptoms.strip():
            st.error("Please enter symptoms.")
            return

        if not location.strip():
            st.error("Please enter location.")
            return

        emergency_result = detect_emergency(symptoms)

        
        top_diseases = predict_top_diseases(
            symptoms_text=symptoms,
            model=disease_model,
            encoder=disease_encoder,
            top_n=3
            )

        top_specialists = predict_top_specialists(
            symptoms_text=symptoms,
            model=doctor_model,
            encoder=doctor_encoder,
            top_n=3
        )

        best_specialist = top_specialists[0]["specialist"]
        best_disease = top_diseases[0]["disease"]

        save_prediction_history(
            symptoms=symptoms,
            location=location,
            top_disease=best_disease,
            top_specialist=best_specialist,
            risk_level=emergency_result["risk_level"]
        )

        top_hospitals = recommend_top_hospitals(
            location=location,
            specialization=best_specialist,
            hospitals=hospitals,
            top_n=3
        )

        st.subheader("🚨 Emergency Risk Assessment")

        if emergency_result["risk_level"] == "HIGH":
            st.error(
                "HIGH RISK: Dangerous symptoms detected. "
                "Please seek immediate medical attention."
            )

        elif emergency_result["risk_level"] == "MEDIUM":
            st.warning(
                "MEDIUM RISK: Some potentially serious symptoms detected."
            )

        else:
            st.success(
                "LOW RISK: No major emergency symptoms detected."
            )
        if emergency_result["matched_keywords"]:
            st.write("Matched emergency symptoms:")
            st.write(", ".join(emergency_result["matched_keywords"]))
            
        st.subheader("🧬 Top Disease Predictions")

        disease_columns = st.columns(3)

        for index, disease in enumerate(top_diseases):
            with disease_columns[index]:
                st.metric(
                label=f"Rank {index + 1}",
                value=disease["disease"],
                delta=f"{disease['confidence_percent']}% confidence"
            )

        disease_chart_df = pd.DataFrame(top_diseases)

        fig = px.bar(
            disease_chart_df,
            x="confidence_percent",
            y="disease",
            orientation="h",
            title="Disease Prediction Confidence",
            labels={
                "confidence_percent": "Confidence %",
                "disease": "Disease"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🩺 Top Specialist Recommendations")

        columns = st.columns(3)

        for index, specialist in enumerate(top_specialists):
            with columns[index]:
                st.metric(
                    label=f"Rank {index + 1}",
                    value=specialist["specialist"],
                    delta=f"{specialist['confidence_percent']}% confidence"
                )
        specialist_chart_df = pd.DataFrame(top_specialists)

        fig2 = px.bar(
            specialist_chart_df,
            x="confidence_percent",
            y="specialist",
            orientation="h",
            title="Specialist Recommendation Confidence",
            labels={
                "confidence_percent": "Confidence %",
                "specialist": "Specialist"
            }
        )

        st.plotly_chart(fig2, use_container_width=True)
        st.subheader("🏥 Recommended Hospitals")

        if not top_hospitals:
            st.warning(
                "No hospital found for the predicted specialist. "
                "Try another location or add more hospital data."
            )

        else:
            for hospital in top_hospitals:
                with st.container(border=True):

                    st.markdown(f"### {hospital['hospital_name']}")

                    st.write(f"📍 Location: {hospital['location']}")

                    st.write(f"⭐ Rating: {hospital['rating']}")

                    st.write(
                        f"🚑 Emergency Available: "
                        f"{'Yes' if hospital['emergency_available'] == 1 else 'No'}"
                    )

                    st.write(
                        f"⏱ Waiting Time: "
                        f"{hospital['waiting_time_hours']} hours"
                    )

                    st.write(
                        f"📊 Recommendation Score: "
                        f"{hospital['recommendation_score']}"
                    )

        st.subheader("📜 Prediction History")

        if os.path.exists(HISTORY_PATH):

            history_df = pd.read_csv(HISTORY_PATH)

            st.dataframe(
                history_df.tail(10),
                use_container_width=True
            )

        else:
            st.info("No prediction history yet.")
        st.subheader("🔎 Model Explanation")

        st.write(
            "The doctor recommendation model uses TF-IDF to convert symptom text into numeric features. "
            "XGBoost then predicts the most suitable specialist based on learned symptom patterns."
        )

        st.write(
            "The hospital recommendation module ranks hospitals using rating, emergency availability, "
            "waiting time, location, and predicted specialization."
        )


if __name__ == "__main__":
    main()
