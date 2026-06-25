from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "Laptop recommendation backend is running"
    }


@app.get("/api/laptops")
def get_laptops():
    df = pd.read_csv("../frontend/laptop.csv")

    laptops = df.to_dict(orient="records")

    return {
        "count": len(laptops),
        "data": laptops
    }