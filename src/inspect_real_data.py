import pandas as pd


DATA_PATH = "data/doctor_real_data.csv"


def inspect_dataset():
    df = pd.read_csv(DATA_PATH)

    print("\nFIRST 5 ROWS")
    print("=" * 50)
    print(df.head())

    print("\nCOLUMN NAMES")
    print("=" * 50)
    print(df.columns.tolist())

    print("\nDATASET SHAPE")
    print("=" * 50)
    print(df.shape)

    print("\nMISSING VALUES")
    print("=" * 50)
    print(df.isnull().sum())


if __name__ == "__main__":
    inspect_dataset()