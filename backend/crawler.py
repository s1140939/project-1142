import requests
import pandas as pd
import re

print("開始抓資料")

all_products=[]

for page in range(1,11):

    url=f"https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=筆電&page={page}&sort=sale/dc"

    response=requests.get(url)

    data=response.json()

    all_products.extend(
        data["prods"]
    )

laptops=[]

for p in all_products:

    name = p["name"]
    price = p["price"]

    # 品牌

    from brand_map import brand_map
    from brand_map import model_map

    brand="Unknown"

    for pattern,value in brand_map.items():
        
        if re.search(
            pattern,
            name,
            re.IGNORECASE
        ):

            brand=value
            break

    if brand=="Unknown":

        for pattern,value in model_map.items():

            if re.search(
                pattern,
                name,
                re.IGNORECASE
            ):

                brand=value
                break


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

        # Intel i系列
        r'i[3579]-\d{4,5}[A-Z]{0,3}',
        r'i[3579]',

        # Intel Core新命名
        r'Core\s*[3579]\s*\d+[A-Z]{1,3}',

        # Intel Core簡寫
        r'C[3579][-\s]?\d+[A-Z]{0,3}',  

        # Intel Ultra
        r'Ultra\s*[3579]-?\s*\d+[A-Z]{1,3}',

        # Intel Ultra簡寫
        r'U[3579][-\s]?\d+[A-Z]{0,3}', 

        # Ryzen完整寫法
        r'Ryzen\s*[3579]\s*\d+[A-Z]{0,3}',

        # Ryzen簡寫
        r'R[3579][-\s]?\d+[A-Z]{0,3}',

        # Celeron
        r'Celeron\s+\w+',

        # Intel N系列
        r'\bN\d+\b'
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