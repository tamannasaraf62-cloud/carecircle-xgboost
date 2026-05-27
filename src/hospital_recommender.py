import pandas as pd


HOSPITAL_DATA_PATH = "data/hospital_data.csv"


def recommend_top_hospitals(location: str, specialization: str, top_n: int = 3):
    hospitals = pd.read_csv(HOSPITAL_DATA_PATH)

    matched = hospitals[
        (hospitals["location"].str.lower() == location.lower())
        &
        (hospitals["specialization"].str.lower() == specialization.lower())
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
                "specialization": row["specialization"],
                "rating": float(row["rating"]),
                "emergency_available": int(row["emergency_available"]),
                "waiting_time_hours": int(row["waiting_time_hours"]),
                "recommendation_score": round(float(row["recommendation_score"]), 2)
            }
        )

    return results


if __name__ == "__main__":
    location = input("Enter location: ")
    specialization = input("Enter specialization: ")

    hospitals = recommend_top_hospitals(location, specialization)

    print("\nTop Hospital Recommendations")
    print("=" * 40)

    if not hospitals:
        print("No matching hospitals found.")
    else:
        for index, hospital in enumerate(hospitals, start=1):
            print(f"{index}. {hospital}")