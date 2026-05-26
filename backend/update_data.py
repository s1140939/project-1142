from crawler import run_crawler
from datetime import datetime

print("開始更新資料")

run_crawler()

print(
    "更新時間:",
    datetime.now()
)

print("更新完成")