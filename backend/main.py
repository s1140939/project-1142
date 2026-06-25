from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db
from models import Laptop


app = FastAPI(
    title="Laptop Recommendation API",
    description="FastAPI backend with PostgreSQL database",
    version="1.0.0"
)


# 允許前端呼叫 API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開發階段先全部允許
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Laptop Recommendation API is running",
        "docs": "/docs"
    }


@app.get("/api/health")
def health_check(db: Session = Depends(get_db)):
    try:
        count = db.query(Laptop).count()

        return {
            "status": "ok",
            "database": "connected",
            "laptop_count": count
        }

    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "message": str(e)
        }


def laptop_to_dict(item: Laptop):
    return {
        "id": item.id,
        "product_id": item.product_id,
        "name": item.name,
        "brand": item.brand,
        "CPU": item.cpu,
        "RAM": item.ram,
        "SSD": item.ssd,
        "price": item.price,
        "url": item.url,
        "updated_at": str(item.updated_at)
    }


def extract_ram_number(ram_text):
    try:
        return int(str(ram_text).replace("GB", "").strip())
    except:
        return 0


def calculate_score(laptop, usage):
    score = 0

    cpu = str(laptop.cpu).lower()
    ram = extract_ram_number(laptop.ram)
    ssd = str(laptop.ssd).lower()

    # RAM 分數
    if ram >= 16:
        score += 3
    elif ram >= 8:
        score += 2
    elif ram >= 4:
        score += 1

    # SSD 分數
    if "1024" in ssd or "1tb" in ssd:
        score += 3
    elif "512" in ssd:
        score += 2
    elif "256" in ssd:
        score += 1

    # CPU 基礎分數
    if "i7" in cpu or "r7" in cpu or "ryzen 7" in cpu or "ultra 7" in cpu:
        score += 4
    elif "i5" in cpu or "r5" in cpu or "ryzen 5" in cpu or "ultra 5" in cpu or "core 5" in cpu:
        score += 3
    elif "i3" in cpu or "r3" in cpu or "ryzen 3" in cpu or "core 3" in cpu:
        score += 2
    elif "n" in cpu or "celeron" in cpu:
        score += 1

    # 用途加權
    if usage == "文書":
        if ram >= 8:
            score += 2
        if laptop.price and laptop.price <= 20000:
            score += 2

    elif usage == "程式":
        if ram >= 16:
            score += 3
        if "i5" in cpu or "i7" in cpu or "r5" in cpu or "r7" in cpu or "ultra" in cpu:
            score += 2

    elif usage == "遊戲":
        if ram >= 16:
            score += 2
        if "i7" in cpu or "r7" in cpu or "ultra 7" in cpu:
            score += 3
        if laptop.price and laptop.price >= 25000:
            score += 1

    return score


@app.get("/api/laptops")
def get_laptops(
    brand: str | None = Query(default=None),
    max_price: int | None = Query(default=None),
    min_ram: int | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(Laptop)

    if brand:
        query = query.filter(Laptop.brand.ilike(f"%{brand}%"))

    if max_price:
        query = query.filter(Laptop.price <= max_price)

    laptops = query.all()

    result = []

    for item in laptops:
        if min_ram:
            ram_value = extract_ram_number(item.ram)

            if ram_value < min_ram:
                continue

        result.append(laptop_to_dict(item))

    return {
        "count": len(result),
        "data": result
    }


@app.get("/api/recommend")
def recommend_laptops(
    usage: str = Query(default="文書"),
    max_price: int = Query(default=30000),
    brand: str | None = Query(default=None),
    limit: int = Query(default=10),
    db: Session = Depends(get_db)
):
    query = db.query(Laptop).filter(Laptop.price <= max_price)

    if brand:
        query = query.filter(Laptop.brand.ilike(f"%{brand}%"))

    laptops = query.all()

    result = []

    for item in laptops:
        data = laptop_to_dict(item)
        data["score"] = calculate_score(item, usage)
        result.append(data)

    result = sorted(
        result,
        key=lambda x: x["score"],
        reverse=True
    )

    return {
        "usage": usage,
        "max_price": max_price,
        "brand": brand,
        "count": len(result[:limit]),
        "data": result[:limit]
    }