import requests
import pandas as pd

print("開始抓資料")

url = "https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=筆電&page=1&sort=sale/dc"

response = requests.get(
    url,
    headers={
        "User-Agent":"Mozilla/5.0"
    }
)

print("狀態碼:",response.status_code)

data = response.json()

products = data["prods"]

print("商品數:",len(products))

for p in products[:5]:

    print("----------------")

    print("名稱:")
    print(p["name"])

    print("價格:")
    print(p["price"])

print("完成")