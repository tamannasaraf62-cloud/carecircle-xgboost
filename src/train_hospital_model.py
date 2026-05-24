import os
import joblib
import pandas as pd

from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


DATA_PATH = "data/hospital_data.csv"
MODEL_PATH = "models/hospital_model.pkl"
ENCODER_PATH = "models/hospital_label_encoder.pkl"


def train_hospital_model():
    df = pd.read_csv(DATA_PATH)
    df = df.dropna()

    features = [
        "location",
        "specialization",
        "rating",
        "emergency_available",
        "waiting_time_hours"
    ]

    x = df[features]
    y = df["hospital_name"]

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    categorical_features = ["location", "specialization"]
    numeric_features = ["rating", "emergency_available", "waiting_time_hours"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("numeric", "passthrough", numeric_features)
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
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

    print("\nHospital Model Training Complete")
    print("================================")
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
    train_hospital_model()