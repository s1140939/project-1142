from crawler import crawl_laptops
from models import Laptop
import traceback
import pandas as pd
import hashlib

def safe_int(value, default=0):
    try:
        return int(value)
    except:
        return default


def clean_text(value):
    if pd.isna(value):
        return ""

    text = str(value).strip()

    if text.lower() in ["nan", "none", "null"]:
        return ""

    return text


def get_value(row, possible_names):
    for name in possible_names:
        if name in row:
            value = clean_text(row.get(name, ""))
            if value:
                return value

    return ""


def make_fallback_id(name, price):
    raw_text = f"{name}_{price}"
    return hashlib.md5(raw_text.encode("utf-8")).hexdigest()


def extract_product_id(row):
    # 1. 先看有沒有 product_id 欄位
    product_id = get_value(
        row,
        ["product_id", "Product_ID", "id", "Id"]
    )

    if product_id:
        return product_id

    # 2. 從 url 欄位拆出商品 ID
    url = get_value(
        row,
        ["url", "URL", "Link", "link", "product_url"]
    )

    if "/prod/" in url:
        return url.split("/prod/")[-1].strip()

    # 3. 如果連 url 都沒有，就用 name + price 產生備用 ID
    name = get_value(
        row,
        ["name", "Name"]
    )

    price = get_value(
        row,
        ["price", "Price"]
    )

    if name:
        return make_fallback_id(name, price)

    return ""


def update_database_from_crawler(db):

    try:
        print("開始從爬蟲更新資料庫")

        df = crawl_laptops(save_csv=False)

        print("爬蟲完成，原始資料筆數：", len(df))
        print("目前欄位：", df.columns.tolist())

        # 建立 product_id 欄位
        df["product_id"] = df.apply(
            extract_product_id,
            axis=1
        )

        # 檢查空白 product_id
        empty_count = len(df[df["product_id"] == ""])
        print("空 product_id 筆數：", empty_count)

        # 移除仍然沒有 product_id 的資料
        df = df[df["product_id"] != ""]

        # 檢查重複 product_id
        duplicate_count = df.duplicated(
            subset=["product_id"]
        ).sum()

        print("重複 product_id 筆數：", duplicate_count)

        # 依 product_id 去重複
        df = df.drop_duplicates(
            subset=["product_id"],
            keep="first"
        )

        df = df.reset_index(drop=True)

        print("product_id 去重後筆數：", len(df))

        # 清空資料庫舊資料
        deleted_count = db.query(Laptop).delete(
            synchronize_session=False
        )

        db.commit()

        print("已刪除舊資料筆數：", deleted_count)

        count = 0

        for _, row in df.iterrows():

            product_id = clean_text(row.get("product_id", ""))

            # 最後保險：空白絕對不寫入
            if product_id == "":
                print("跳過空 product_id：", row.get("name", ""))
                continue

            laptop = Laptop(
                product_id=product_id,
                name=get_value(row, ["name", "Name"]),
                brand=get_value(row, ["brand", "Brand"]),
                cpu=get_value(row, ["CPU", "cpu"]),
                ram=get_value(row, ["RAM", "ram"]),
                ssd=get_value(row, ["SSD", "ssd"]),
                price=safe_int(get_value(row, ["price", "Price"])),
                url=get_value(row, ["url", "URL", "Link", "link", "product_url"])
            )

            db.add(laptop)
            count += 1

        db.commit()

        print("資料庫更新完成，共", count, "筆")

        return {
            "status": "success",
            "message": "資料庫更新完成",
            "count": count
        }

    except Exception as e:

        db.rollback()

        error_text = traceback.format_exc()

        print("資料庫更新失敗：")
        print(error_text)

        return {
            "status": "error",
            "message": str(e),
            "detail": error_text
        }
