import pandas as pd
import numpy as np
import joblib
import math

model_bundle = joblib.load("model/model_2.pkl")
model = model_bundle["model"]
encoder = model_bundle["encoder"]
features = model_bundle["features"]

def clean_for_json(data):
    if isinstance(data, dict):
        return {k: clean_for_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_for_json(v) for v in data]
    elif isinstance(data, tuple):
        return tuple(clean_for_json(v) for v in data)
    elif isinstance(data, (np.integer,)):
        return int(data)
    elif isinstance(data, (np.floating,)):
        return float(data)
    elif isinstance(data, (np.ndarray,)):
        return data.tolist()
    else:
        return data

STORAGE_RULES = {
    "CABINET": [
        ("LEVEL I", 0.0009),
        ("LEVEL G & H", 0.00158),
        ("LEVEL E & F", 0.00225),
        ("LEVEL C & D", 0.00535),
        ("LEVEL B", 0.00725),
        ("LEVEL A", 0.00949)
    ],
    "SHELVING": [
        ("LEVEL G", 0.01439),
        ("LEVEL F", 0.01993),
        ("LEVEL C, D & E", 0.02989),
        ("LEVEL B", 0.04207),
        ("LEVEL A", 0.05092)
    ],
    "RACKING": [
        ("PALLET", 1.44)
    ],
    "FLOOR": [
        ("FLOOR AREA", 1.44)
    ]
}

STORAGE_PRICE = {
    "CABINET": 27342667,
    "SHELVING": 9434889,
    "RACKING": 490000,
    "FLOOR": 63000,
    "PALLET": 155000
}

STORAGE_CAPACITY = {
    "CABINET": {"bin_per_unit": 144},
    "SHELVING": {"bin_per_unit": 35},
    "RACKING": {"pallet_per_unit": 12},
    "FLOOR": {"pallet_per_unit": 1, "stacking": 2}
}

def calculate_cost(storage, volume_per_item, total_volume):
    storage = str(storage).upper()

    if storage not in STORAGE_RULES:
        return "-", 0, 0

    levels = STORAGE_RULES[storage]
    selected_level, level_volume = levels[-1]

    for level_name, capacity in levels:
        if volume_per_item <= capacity:
            selected_level = level_name
            level_volume = capacity
            break

    if storage == "CABINET":
        total_bin = math.ceil(total_volume / level_volume)
        required_units = math.ceil(total_bin / STORAGE_CAPACITY["CABINET"]["bin_per_unit"])
        total_cost = required_units * STORAGE_PRICE["CABINET"]

    elif storage == "SHELVING":
        total_bin = math.ceil(total_volume / level_volume)
        required_units = math.ceil(total_bin / STORAGE_CAPACITY["SHELVING"]["bin_per_unit"])
        total_cost = required_units * STORAGE_PRICE["SHELVING"]

    elif storage == "RACKING":
        total_pallet = math.ceil(total_volume / level_volume)
        required_units = math.ceil(total_pallet / STORAGE_CAPACITY["RACKING"]["pallet_per_unit"])
        total_cost = (required_units * STORAGE_PRICE["RACKING"]) + (total_pallet * STORAGE_PRICE["PALLET"])

    elif storage == "FLOOR":
        total_pallet = math.ceil(total_volume / level_volume)
        required_units = math.ceil(total_pallet / STORAGE_CAPACITY["FLOOR"]["stacking"])
        total_cost = (required_units * STORAGE_PRICE["FLOOR"]) + (total_pallet * STORAGE_PRICE["PALLET"])

    else:
        required_units = 1
        total_cost = 0

    return selected_level, required_units, total_cost

def predict_storage(df: pd.DataFrame):

    df.columns = df.columns.str.strip()

    required_columns = [
        "Part Number",
        "Quantity",
        "Unit Weight (kg)",
        "Growth Indicator",
        "Length (cm)",
        "Width (cm)",
        "Height (cm)"
    ]

    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df = df.dropna(how="all")
    df = df[df["Part Number"].astype(str).str.strip() != ""]
    df = df.reset_index(drop=True)

    numeric_cols = [
        "Quantity",
        "Unit Weight (kg)",
        "Length (cm)",
        "Width (cm)",
        "Height (cm)"
    ]

    for col in numeric_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())

    df["Growth Indicator"] = df["Growth Indicator"].astype(str).str.strip()
    most_common_label = encoder.classes_[0]

    df.loc[
        ~df["Growth Indicator"].isin(encoder.classes_),
        "Growth Indicator"
    ] = most_common_label

    df["Growth_encoded"] = encoder.transform(df["Growth Indicator"])

    df["Volume_m3"] = (
        df["Length (cm)"] *
        df["Width (cm)"] *
        df["Height (cm)"]
    ) / 1_000_000

    df["Volume_cm3"] = (
        df["Length (cm)"] *
        df["Width (cm)"] *
        df["Height (cm)"]
    )

    df["Total_Volume_m3"] = df["Volume_m3"] * df["Quantity"]
    df["Total_Weight_kg"] = df["Unit Weight (kg)"] * df["Quantity"]

    df["Density"] = np.where(
        df["Volume_m3"] > 0,
        df["Unit Weight (kg)"] / df["Volume_m3"],
        0
    )

    X = df[features].copy()
    predictions = model.predict(X)
    predictions = [str(p) for p in predictions]

    results = []

    for i in range(len(df)):

        storage = predictions[i]

        if float(df.iloc[i]["Total_Volume_m3"]) > 1.44 and storage == "RACKING":
            storage = "FLOOR"

        vol_per_item = float(df.iloc[i]["Volume_m3"])
        total_vol = float(df.iloc[i]["Total_Volume_m3"])

        level, units, cost = calculate_cost(storage, vol_per_item, total_vol)

        if storage in ["CABINET", "SHELVING"]:
            if vol_per_item > 0:
                actual_req = math.ceil(total_vol / vol_per_item)
            else:
                actual_req = 0
            unit_type = "bin"
        else:
            actual_req = math.ceil(total_vol / 1.44)
            unit_type = "pallet"

        results.append({
            "Part Number": str(df.iloc[i]["Part Number"]),
            "Quantity": int(df.iloc[i]["Quantity"]),
            "Weight (kg)": float(df.iloc[i]["Unit Weight (kg)"]),
            "Growth Indicator": str(df.iloc[i]["Growth Indicator"]),
            "Dimension (cm3)": float(df.iloc[i]["Volume_cm3"]),
            "Volume per Item (m3)": float(round(vol_per_item, 4)),
            "Storage Type": str(storage),
            "Level": str(level),
            "Actual Requirement": int(actual_req),
            "Unit Type": unit_type,
            "Units Needed": int(units),
            "Total Cost": float(cost)
        })

    return clean_for_json(results)