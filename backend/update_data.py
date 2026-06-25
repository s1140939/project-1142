from datetime import datetime
import crawler


def main():
    print("開始更新 laptop.csv")
    print("開始時間：", datetime.now())

    # 優先使用 run_crawler()
    if hasattr(crawler, "run_crawler"):
        result = crawler.run_crawler()

    # 如果 crawler.py 已經改成 crawl_laptops(save_csv=True)
    elif hasattr(crawler, "crawl_laptops"):
        result = crawler.crawl_laptops(save_csv=True)

    else:
        raise AttributeError(
            "crawler.py 中找不到 run_crawler() 或 crawl_laptops()"
        )

    print("laptop.csv 更新完成")
    print("結束時間：", datetime.now())

    # 如果 crawler 回傳 DataFrame，就顯示資料筆數
    if result is not None and hasattr(result, "__len__"):
        print("資料筆數：", len(result))


if __name__ == "__main__":
    main()