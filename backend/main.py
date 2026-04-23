from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from services.prediction_storage import predict_storage

app = FastAPI(
    title="Storage Prediction API",
    description="API untuk memprediksi storage dan biaya berdasarkan CSV/XLSX input",
    version="1.0.0",
    root_path="/api"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://capas.ckblogistics.id",
        "https://ckblogistics.id",
        "https://darling-sfogliatella-ef24f0.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Storage Prediction API Running on CKB Production"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    if not (file.filename.endswith(".csv") or file.filename.endswith(".xlsx")):
        raise HTTPException(status_code=400, detail="File harus CSV atau XLSX")

    try:

        if file.filename.endswith(".csv"):
            df = pd.read_csv(
                file.file,
                sep=None,
                engine="python"
            )
        else:
            df = pd.read_excel(file.file)

        df.columns = df.columns.str.strip()

        print("Detected columns:", df.columns.tolist())

        required_columns = [
            "Part Number",
            "Quantity",
            "Unit Weight (kg)",
            "Growth Indicator",
            "Length (cm)",
            "Width (cm)",
            "Height (cm)"
        ]

        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"CSV/XLSX missing columns: {missing}"
            )

        if "Unit Weight (kg)" in df.columns:
            df["Unit Weight (kg)"] = (
                df["Unit Weight (kg)"]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .str.strip()
            )
            df["Unit Weight (kg)"] = pd.to_numeric(
                df["Unit Weight (kg)"],
                errors="coerce"
            )

        for col in ["Quantity", "Length (cm)", "Width (cm)", "Height (cm)"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        print("First rows:")
        print(df.head())

        results = predict_storage(df)

        results_safe = []

        for r in results:
            clean_r = {
                k: (
                    0 if isinstance(v, float) and
                    (pd.isna(v) or v == float("inf") or v == -float("inf"))
                    else v
                )
                for k, v in r.items()
            }
            results_safe.append(clean_r)

        return JSONResponse(
            content={
                "filename": file.filename,
                "predictions": results_safe
            }
        )

    except Exception as e:
        print("Error during prediction:", str(e))
        raise HTTPException(status_code=500, detail=str(e))