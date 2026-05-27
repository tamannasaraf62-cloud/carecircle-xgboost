import os
import pandas as pd


def create_doctor_data():
    data = [
        ["fever cough tiredness", "flu", "General Physician", "Dr. Sharma"],
        ["chest pain breathlessness sweating", "heart problem", "Cardiologist", "Dr. Mehta"],
        ["skin rash itching redness", "skin allergy", "Dermatologist", "Dr. Rao"],
        ["headache vomiting sensitivity to light", "migraine", "Neurologist", "Dr. Iyer"],
        ["joint pain swelling stiffness", "arthritis", "Orthopedic", "Dr. Khan"],
        ["stomach pain nausea acidity", "gastritis", "Gastroenterologist", "Dr. Patel"],
        ["tooth pain gum bleeding", "dental problem", "Dentist", "Dr. Verma"],
        ["eye pain blurry vision redness", "eye infection", "Ophthalmologist", "Dr. Nair"],
        ["anxiety sadness sleep problem", "mental health issue", "Psychiatrist", "Dr. Sen"],
        ["pregnancy pain bleeding", "pregnancy issue", "Gynecologist", "Dr. Kapoor"],
    ]

    df = pd.DataFrame(
        data,
        columns=["symptoms", "disease", "specialization", "doctor_name"]
    )

    df.to_csv("data/doctor_data.csv", index=False)


def create_hospital_data():
    data = [
        ["City Hospital", "Delhi", "General Physician", 4.5, 1, 3],
        ["Heart Care Hospital", "Delhi", "Cardiologist", 4.8, 1, 2],
        ["Skin Plus Clinic", "Mumbai", "Dermatologist", 4.2, 1, 5],
        ["Neuro Care Center", "Mumbai", "Neurologist", 4.7, 0, 4],
        ["Ortho Life Hospital", "Pune", "Orthopedic", 4.4, 1, 3],
        ["Digestive Health Hospital", "Pune", "Gastroenterologist", 4.3, 1, 6],
        ["Smile Dental Clinic", "Bangalore", "Dentist", 4.6, 0, 2],
        ["Vision Eye Hospital", "Bangalore", "Ophthalmologist", 4.5, 1, 4],
        ["Mind Wellness Center", "Chennai", "Psychiatrist", 4.1, 0, 5],
        ["Women Care Hospital", "Chennai", "Gynecologist", 4.9, 1, 1],
    ]

    df = pd.DataFrame(
        data,
        columns=[
            "hospital_name",
            "location",
            "specialization",
            "rating",
            "emergency_available",
            "waiting_time_hours"
        ]
    )

    df.to_csv("data/hospital_data.csv", index=False)


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    create_doctor_data()
    create_hospital_data()
    print("Sample datasets created successfully.")