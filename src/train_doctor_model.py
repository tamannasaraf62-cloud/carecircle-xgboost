import os
import joblib
import pandas as pd

from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


DATA_PATH = "data/doctor_data.csv"
MODEL_PATH = "models/doctor_model.pkl"
ENCODER_PATH = "models/doctor_label_encoder.pkl"


def train_doctor_model():
    df = pd.read_csv(DATA_PATH)
    df = df.dropna()

    df["input_text"] = df["symptoms"] + " " + df["disease"]

    x = df["input_text"]
    y = df["specialization"]

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    model = Pipeline(
        steps=[
            ("vectorizer", TfidfVectorizer()),
            (
                "classifier",
                XGBClassifier(
                    n_estimators=100,
                    max_depth=3,
                    learning_rate=0.1,
                    eval_metric="mlogloss",
                    random_state=42
                )
            )
        ]
    )

    model.fit(x, y_encoded)

    predictions = model.predict(x)
    accuracy = accuracy_score(y_encoded, predictions)

    print("\nDoctor Model Training Complete")
    print("==============================")
    print(f"Training Accuracy: {accuracy:.4f}")
    print("\nReport:")
    print(classification_report(y_encoded, predictions))

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(label_encoder, ENCODER_PATH)

    print("\nSaved:")
    print(MODEL_PATH)
    print(ENCODER_PATH)


if __name__ == "__main__":
    train_doctor_model()