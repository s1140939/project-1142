import os
import pandas as pd
from database import SessionLocal
from models import Laptop


def safe_int(value, default=0):
    try:
        return int(value)
    except:
        return default


def get_product_id(row):
    product_id = row.get("product_id", "")

    if pd.notna(product_id) and str(product_id).strip() != "":
        return str(product_id).strip()

    url = row.get("url", "")

    if pd.notna(url) and "/prod/" in str(url):
        return str(url).split("/prod/")[-1].strip()

    return None


def import_csv_to_db():
    csv_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "frontend",
        "laptop.csv"
    )

    print("讀取 CSV：", csv_path)

    df = pd.read_csv(csv_path)

    db = SessionLocal()

    try:
        db.query(Laptop).delete()

        seen_ids = set()
        count = 0

        for _, row in df.iterrows():

            product_id = get_product_id(row)

            # 避免 product_id 重複
            if product_id in seen_ids:
                continue

            seen_ids.add(product_id)

            laptop = Laptop(
                product_id=product_id,
                name=str(row.get("name", "")),
                brand=str(row.get("brand", "")),
                cpu=str(row.get("CPU", "")),
                ram=str(row.get("RAM", "")),
                ssd=str(row.get("SSD", "")),
                price=safe_int(row.get("price", 0)),
                url=str(row.get("url", ""))
            )

            db.add(laptop)
            count += 1

        db.commit()

        print("匯入完成，共", count, "筆資料")

    except Exception as e:
        db.rollback()
        print("匯入失敗：", e)

    finally:
        db.close()


if __name__ == "__main__":
    import_csv_to_db()