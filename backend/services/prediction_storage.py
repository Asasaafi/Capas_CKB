import pandas as pd
import numpy as np
import joblib
import math

model_bundle = joblib.load("model/model.pkl")
model = model_bundle["model"]
encoder = model_bundle["encoder"]
features = model_bundle["features"]

STORAGE_RULES = {
    "CABINET": [("LEVEL I", 0.0009), ("LEVEL G & H", 0.00158), ("LEVEL E & F", 0.00225),
                ("LEVEL C & D", 0.00535), ("LEVEL B", 0.00725), ("LEVEL A", 0.00949)],
    "SHELVING": [("LEVEL A", 0.05092), ("LEVEL B", 0.04207), ("LEVEL C, D & E", 0.02989),
                 ("LEVEL F", 0.01993), ("LEVEL G", 0.01439)],
    "RACKING": [("PALLET", 1.44)],
    "FLOOR": [("FLOOR AREA", 1.44)]
}

STORAGE_PRICE = {
    "CABINET": 571000,
    "SHELVING": 600000,
    "RACKING": 650000,
    "FLOOR": 700000
}

def calculate_cost(storage, volume_per_item, total_volume):
    storage = str(storage).upper()

    if storage not in STORAGE_RULES:
        return "-", 0, 0

    levels = STORAGE_RULES[storage]

    selected_level, level_volume = None, None

    for level_name, capacity in levels:
        if volume_per_item <= capacity:
            selected_level = level_name
            level_volume = capacity
            break

    if selected_level is None:
        selected_level, level_volume = levels[-1]

    required_units = math.ceil(total_volume / level_volume)
    total_cost = required_units * STORAGE_PRICE[storage]

    return selected_level, required_units, total_cost

def predict_storage(df: pd.DataFrame):

    df = df.dropna(how="all")

    df = df[df["Part Number"].astype(str).str.strip() != ""]
    df = df[df["Part Number"] != 0]

    df = df.reset_index(drop=True)

    numeric_cols = [
        "Quantity",
        "Unit Weight (kg)",
        "Length (cm)",
        "Width (cm)",
        "Height (cm)"
    ]

    for col in numeric_cols:

        if col == "Unit Weight (kg)":
            df[col] = df[col].astype(str).str.replace(",", ".")

        df[col] = pd.to_numeric(df[col], errors="coerce")

        df[col] = df[col].fillna(df[col].median())

    df["Growth Indicator"] = df["Growth Indicator"].astype(str)

    most_common_label = encoder.classes_[0]

    df.loc[
        ~df["Growth Indicator"].isin(encoder.classes_),
        "Growth Indicator"
    ] = most_common_label

    df["Growth_encoded"] = encoder.transform(df["Growth Indicator"])

    # feature
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

    # model
    X = df[features].copy()

    predictions = model.predict(X)

    results = []

    for i in range(len(df)):

        storage = str(predictions[i])

        vol_per_item = df.iloc[i]["Volume_m3"]
        total_vol = df.iloc[i]["Total_Volume_m3"]

        level, units, cost = calculate_cost(storage, vol_per_item, total_vol)

        length = df.iloc[i]["Length (cm)"]
        width = df.iloc[i]["Width (cm)"]
        height = df.iloc[i]["Height (cm)"]

        dimension_volume = int(length * width * height)

        results.append({
            "Part Number": df.iloc[i]["Part Number"],
            "Quantity": df.iloc[i]["Quantity"],
            "Weight (kg)": df.iloc[i]["Unit Weight (kg)"],
            "Growth Indicator": df.iloc[i]["Growth Indicator"],

            "Dimension (cm)": dimension_volume,

            "Storage Type": storage,
            "Level": level,
            "Units Needed": units,
            "Total Cost": cost
        })

    results_clean = []

    for r in results:
        clean_r = {
            k: (
                0 if isinstance(v, float) and
                (pd.isna(v) or v == np.inf or v == -np.inf)
                else v
            )
            for k, v in r.items()
        }

        results_clean.append(clean_r)

    return results_clean