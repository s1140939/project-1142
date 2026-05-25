import requests
import pandas as pd
import re

print("開始抓資料")

url="https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=筆電&page=1&sort=sale/dc"

response=requests.get(
    url,
    headers={
        "User-Agent":"Mozilla/5.0"
    }
)

data=response.json()

products=data["prods"]

laptops=[]

for p in products:

    name = p["name"]
    price = p["price"]

    # 品牌

    brand = "Unknown"

    if ("Vivobook" in name or
        "VivoBook" in name):

        brand = "ASUS"

    elif ("Aspire" in name):

        brand = "Acer"

    elif ("IdeaPad" in name):

        brand = "Lenovo"

    elif ("Surface" in name):

        brand = "Microsoft"

    elif ("HP" in name):

        brand = "HP"


    # RAM

    ram="Unknown"

    ram_matches=re.findall(
        r'(\d+)G[B]?',
        name
    )

    if ram_matches:

        values=[]

        for x in ram_matches:

            num=int(x)

            # 避免把SSD當成RAM
            if num<=64:

                values.append(num)

        if values:

            ram=str(sum(values))+"GB"

    # SSD

    ssd="Unknown"

    ssd_matches=re.findall(
        r'(\d+)(?:GB|G)',
        name
    )

    if ssd_matches:

        capacities=[]

        for x in ssd_matches:

            num=int(x)


            # 通常SSD>=128
            if num>=128:

                capacities.append(num)


        if capacities:

            ssd=str(max(capacities))+"GB"
    
    ssd_matches=re.findall(
        r'(\d+)(?:TB)',
        name
    )

    if ssd_matches:

        capacities=[]

        for x in ssd_matches:

            num=int(x)
            
            capacities.append(num*1024)

        if capacities :

            ssd=str(max(capacities))+"GB"

    # CPU
    
    cpu="Unknown"
    cpu_patterns=[
        r'R[3579]-\d{3,4}[A-Z]*',          # Ryzen
        r'Ultra\s*\d+\s*\d+[A-Z]*',        # Intel Ultra
        r'i[3579]-\d{4,5}[A-Z]*',          # i3/i5/i7/i9
        r'i[3579]',                        # 只寫i3/i5/i7/i9
        r'Celeron\s+\w+',                  # Celeron
        r'\bN\d+\b'                        # Intel N系列
        ]
    
    spec=[]

    for pattern in cpu_patterns:
        result=re.findall(
            pattern,
            name,
            re.IGNORECASE
        )
        
        if result:
            spec.extend(result)
    
    if spec:
        cpu=spec[0]


    laptops.append({

        "name":name,
        "brand":brand,
        "RAM":ram,
        "SSD":ssd,
        "CPU":cpu,
        "price":price,

    })

df=pd.DataFrame(laptops)

print(df.head())

df.to_csv(
    "frontend/laptop.csv",
    index=False,
    encoding="utf-8-sig"
)

print("CSV完成")