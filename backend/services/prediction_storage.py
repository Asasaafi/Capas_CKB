import pandas as pd
import numpy as np
import joblib
import math
from fastapi import HTTPException

bundle = joblib.load("model/model_pipeline.pkl")

model = bundle["model"]
encoder = bundle.get("encoder")
features = bundle.get("features")
median_values = bundle.get("median_values", {})

VALID_STORAGE = {"RACKING", "SHELVING", "CABINET", "FLOOR"}

capacity_map = {
    "SHELVING": 35,
    "CABINET": 144,
    "RACKING": 12,
    "FLOOR": 2
}

price_map = {
    "CABINET": 27342667,
    "SHELVING": 9434889,
    "RACKING": 490000,
    "FLOOR": 63000,
    "PALLET": 155000
}

def feature_engineering(df):
    df = df.copy()

    df["Volume_m3"] = (
        df["Length (cm)"] *
        df["Width (cm)"] *
        df["Height (cm)"]
    ) / 1_000_000

    df["Total_Volume_m3"] = df["Volume_m3"] * df["Quantity"]
    df["Total_Weight_kg"] = df["Unit Weight (kg)"] * df["Quantity"]

    df["Density"] = np.where(
        df["Volume_m3"] > 0,
        df["Unit Weight (kg)"] / df["Volume_m3"],
        0
    )

    return df

def predict_storage(df: pd.DataFrame):

    df = df.copy()

    num_cols = [
        "Quantity",
        "Unit Weight (kg)",
        "Length (cm)",
        "Width (cm)",
        "Height (cm)"
    ]

    for c in num_cols:
        df[c] = (
            df[c].astype(str)
            .str.replace(",", ".", regex=False)
            .str.strip()
        )
        df[c] = pd.to_numeric(df[c], errors="coerce")
        df[c] = df[c].fillna(median_values.get(c, df[c].median()))

    if encoder is not None:
        df["Growth Indicator"] = df["Growth Indicator"].astype(str).str.strip()
        df.loc[
            ~df["Growth Indicator"].isin(encoder.classes_),
            "Growth Indicator"
        ] = encoder.classes_[0]
        df["Growth_encoded"] = encoder.transform(df["Growth Indicator"])

    df = feature_engineering(df)

    if features is None:
        raise HTTPException(status_code=500, detail="Features not found in model bundle")

    X = df[features]

    try:
        raw_pred = model.predict(X)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    results = []

    for i in range(len(df)):

        storage = str(raw_pred[i]).upper().strip()

        if storage not in VALID_STORAGE:
            storage = "RACKING"

        actual = int(df.iloc[i]["Quantity"])
        capacity = capacity_map.get(storage, 1)
        units_needed = int(math.ceil(actual / capacity))

        if storage == "RACKING":
            total_cost = (units_needed * price_map["RACKING"]) + (actual * price_map["PALLET"])
        elif storage == "FLOOR":
            total_cost = (units_needed * price_map["FLOOR"]) + (actual * price_map["PALLET"])
        else:
            total_cost = units_needed * price_map.get(storage, 0)

        results.append({
            "Part Number": str(df.iloc[i]["Part Number"]),
            "Quantity": actual,
            "Weight (kg)": float(df.iloc[i]["Unit Weight (kg)"]),
            "Growth Indicator": str(df.iloc[i]["Growth Indicator"]),
            "Length (cm)": float(df.iloc[i]["Length (cm)"]),
            "Width (cm)": float(df.iloc[i]["Width (cm)"]),
            "Height (cm)": float(df.iloc[i]["Height (cm)"]),
            "Dimension (cm3)": float(
                df.iloc[i]["Length (cm)"] *
                df.iloc[i]["Width (cm)"] *
                df.iloc[i]["Height (cm)"]
            ),
            "Volume (m3)": float(df.iloc[i]["Volume_m3"]),
            "Total Volume (m3)": float(df.iloc[i]["Total_Volume_m3"]),
            "Actual Requirement": actual,
            "Units Needed": units_needed,
            "Total Cost": total_cost,
            "Storage Type": storage
        })

    return results