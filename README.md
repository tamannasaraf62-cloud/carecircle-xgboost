# 🏥 CareCircle XGBoost Healthcare Recommendation System

AI-powered healthcare recommendation system using XGBoost, FastAPI, and Streamlit.

---

# 📌 Project Overview

CareCircle is an educational machine learning healthcare recommendation system that predicts:

- Possible diseases from symptoms
- Recommended doctor specialists
- Recommended hospitals
- Emergency severity level

The project combines:
- Machine Learning
- NLP-based symptom processing
- FastAPI backend
- Streamlit frontend
- XGBoost classification models

---

# 🚀 Features

✅ Disease Prediction  
✅ Specialist Recommendation  
✅ Hospital Recommendation  
✅ Emergency Detection  
✅ Confidence Scores  
✅ Prediction History Tracking  
✅ Streamlit Dashboard  
✅ FastAPI Backend APIs  
✅ XGBoost ML Models  
✅ Model Evaluation System  

---

# 🧠 Machine Learning Models

The project uses:

- XGBoost Classifier
- Label Encoding
- TF-IDF Vectorization
- NLP symptom preprocessing

---

# 🛠️ Tech Stack

## Backend
- Python
- FastAPI

## Frontend
- Streamlit

## Machine Learning
- XGBoost
- Scikit-learn
- Pandas
- NumPy

---

# 📂 Project Structure

```bash
carecircle_xgboost/
│
├── data/
├── models/
├── src/
├── history/
├── requirements.txt
├── README.md
└── .gitignore

## CareCircle Chatbot Assistant

This module provides a lightweight healthcare chatbot using FastAPI and Streamlit.

### Features
- Emergency detection
- Queue tracking
- Appointment support
- Doctor recommendation
- Hospital navigation
- Billing and insurance support
- Lab report support
- Invalid query handling

### Run Chatbot Backend

```bash
cd chatbot/backend
pip install fastapi uvicorn streamlit requests
python -m uvicorn app:app --reload
```

### Run Chatbot Frontend

```bash
cd chatbot/backend
streamlit run streamlit_app.py
```
