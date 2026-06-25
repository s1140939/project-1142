# 筆電推薦系統 Project 1142
本專案為大一 Python 程式設計期末專題，目標是建立一個可以依照筆電資料進行推薦與展示的網站。  
目前專案包含兩個主要部分：

1. `backend/`：負責取得筆電資料、清理規格、產生 `laptop.csv`
2. `frontend/`：負責 Flask 網頁顯示、讀取 CSV 資料並提供使用者操作介面

已部署網址：  
https://project-1142.vercel.app/

---

## 專案目標

使用者在選購筆電時，常需要同時比較品牌、CPU、RAM、SSD、價格與使用情境。本專案希望透過 Python 自動整理電商資料，將非結構化的商品名稱轉換成可分析的資料表，並在網頁中提供篩選、排序與推薦結果。

目前資料來源以 PChome 搜尋 API 為主，後端會自動取得商品資料，並從商品名稱中擷取：

- 品牌
- CPU
- RAM
- SSD
- 價格
- 商品原始網址

整理後輸出為：

```text
frontend/laptop.csv
```

前端網站會讀取此 CSV，依照預算、用途與推薦分數顯示筆電卡片。

---

## 專案結構

```text
project-1142/
├── backend/
│   ├── crawler.py          # 主要爬蟲與資料清理程式
│   ├── update_data.py      # 自動更新 CSV 的執行入口
│   └── brand_map.py        # 品牌與型號對應規則
│
├── frontend/
│   ├── app.py              # Flask 網站主程式
│   ├── laptop.csv          # 清理後的筆電資料
│   ├── requirements.txt    # Python 套件需求
│   ├── static/
│   │   └── style.css       # 網頁樣式
│   └── templates/
│       ├── base.html       # 共用版型
│       ├── index.html      # 首頁與推薦展示頁
│       ├── about.html      # 關於頁面
│       └── contact.html    # 聯絡頁面
│
├── feedback.csv            # 使用者回饋資料
└── README.md               # 專案說明文件
```

---

## 使用技術

- Python
- Flask
- requests
- pandas
- Regular Expression
- CSV
- HTML / CSS
- Vercel
- GitHub

---

## 取得資料

本專案目前使用 PChome 搜尋 API 取得商品資料，而不是直接解析前端 HTML。  
使用 API 的原因是 PChome 商品資料多由 JavaScript 動態載入，直接用 BeautifulSoup 解析 HTML 時不容易取得完整商品資訊。

API 範例：

```text
https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=筆電&page=1&sort=sale/dc
```

參數說明：

| 參數 | 說明 |
|---|---|
| `q=筆電` | 搜尋關鍵字為「筆電」 |
| `page=1` | 搜尋結果第 1 頁 |
| `sort=sale/dc` | 依銷售相關排序 |

目前 `crawler.py` 會抓取第 1 到第 10 頁資料。

---

## 後端資料處理流程

```text
PChome 搜尋 API
        ↓
requests 取得 JSON 資料
        ↓
讀取商品名稱、價格、商品 ID
        ↓
組合商品原始網址
        ↓
利用 brand_map.py 判斷品牌
        ↓
利用正規表示式擷取 CPU / RAM / SSD
        ↓
pandas 建立 DataFrame
        ↓
依價格排序
        ↓
根據商品名稱去除重複資料
        ↓
輸出 frontend/laptop.csv
```

---

## CSV 欄位說明

`frontend/laptop.csv` 目前包含以下欄位：

| 欄位 | 說明 |
|---|---|
| `name` | 商品完整名稱 |
| `brand` | 品牌，例如 ASUS、Acer、Lenovo、HP |
| `RAM` | 記憶體容量，例如 8GB、16GB |
| `SSD` | 儲存容量，例如 512GB、1024GB |
| `CPU` | 處理器型號，例如 i5-13420H、R7-8840HS、N150、Celeron N4500 |
| `price` | 商品價格 |
| `url` | 商品在 PChome 的原始網址，可用於「了解更多」連結 |

CSV 範例：

```csv
name,brand,RAM,SSD,CPU,price,url
Vivobook Go 14...,ASUS,4GB,128GB,Celeron N4500,7999,https://24h.pchome.com.tw/prod/...
```

---

## 後端功能

### 1. 取得筆電資料

主要檔案：

```text
backend/crawler.py
```

功能：

- 向 PChome 搜尋 API 發送請求
- 解析 JSON 商品資料
- 抓取多頁筆電商品
- 取得商品名稱、價格與商品 ID
- 由商品 ID 組合商品網址

商品網址產生方式：

```python
product_url = "https://24h.pchome.com.tw/prod/" + product_id
```

直接執行：

```bash
python backend/crawler.py
```

---

### 2. 品牌辨識

品牌判斷規則集中放在：

```text
backend/brand_map.py
```

例如：

```python
r"Vivobook": "ASUS"
r"Aspire": "Acer"
r"IdeaPad": "Lenovo"
r"Surface": "Microsoft"
```

若商品名稱中沒有明顯系列名稱，則使用 `model_map` 透過型號規則進行補充判斷。

---

### 3. 規格擷取

目前利用 Regular Expression 從商品名稱中擷取：

- CPU：支援 Intel i 系列、Intel Ultra、Intel Core、Ryzen、Celeron、Intel N 系列
- RAM：擷取 4GB、8GB、16GB、8GB+8GB 等格式
- SSD：擷取 128GB、256GB、512GB、1TB 等格式，並將 TB 轉換為 GB

---

### 4. 去除重複資料

為避免推薦結果出現同一商品重複顯示，資料輸出前會進行去重複處理。

處理方式：

1. 先依照價格由低到高排序
2. 再根據商品名稱 `name` 去除重複
3. 保留價格較低的商品資料
4. 檢查清理後是否仍有重複資料

執行時會在終端機顯示類似：

```text
原始筆數: 200
找到重複: 57
去重後: 165
剩餘重複: 0
CSV完成
```

---

### 5. 更新 CSV

`update_data.py` 會呼叫 `crawler.py` 中的 `run_crawler()`，重新抓取資料並更新：

```text
frontend/laptop.csv
```

執行方式：

```bash
python backend/update_data.py
```

執行成功時，終端機會顯示類似：

```text
開始更新資料
開始抓資料
                                                name brand   RAM    SSD            CPU  price
0  Aspire Lite 16吋Ultra 5 AI 輕薄長效筆電  (Ultra 5 115...  Acer  16GB  512GB   Ultra 5 115U  19900
1  Aspire Lite 17.3吋文書筆電 銀色(C3-N355/8G/512G/W11/A...  Acer   8GB  512GB           N355  17900
2  Aspire Lite 15.6吋文書筆電 灰色(C3-N355/8G/512G/W11/F...  Acer   8GB  512GB           N355  13900
3  Aspire Lite 14吋 文書效能筆電銀(N150/4G/128G/WIN11home...  Acer   4GB  128GB           N150   8999
4  Aspire Lite 15.6吋文書筆電 銀(Celeron N4500/4G/128G/...  Acer   4GB  128GB  Celeron N4500   7999
原始筆數: 200
找到重複: 58
去重後: 164
剩餘重複: 0
CSV完成
更新時間: 2026-05-26 12:36:23.476575
更新完成
```

---

## 前端功能

目前網站功能包含：

- 首頁 `/`
- 關於頁 `/about`
- 聯絡頁 `/contact`
- 讀取 `frontend/laptop.csv`
- 顯示筆電卡片
- 預算篩選
- 使用情境篩選
- 推薦分數排序
- 價格排序
- 顯示推薦理由
- 顯示商品原始連結

使用情境分類包含：

```text
日常/學習
商務
創作/專業
影音/娛樂
```

排序方式包含：

```text
推薦評分由高到低
推薦評分由低到高
價格由低到高
價格由高到低
```

主要檔案：

```text
frontend/app.py
frontend/templates/
frontend/static/style.css
```

---

## 安裝與執行方式

### 1. 下載專案

```bash
git clone <https://github.com/s1140939/project-1142.git>
cd project-1142
```

---

### 2. 安裝套件

```bash
pip install -r frontend/requirements.txt
```

---

### 3. 更新筆電資料

```bash
python backend/update_data.py
```

---

### 4. 啟動網站

```bash
python frontend/app.py
```

啟動後在瀏覽器開啟：

```text
http://127.0.0.1:5000
```

---

## 部署方式

本專案使用 Vercel 部署前端網站。

建議 Vercel 設定：

```text
Root Directory: frontend
```

部署時 Vercel 主要會讀取：

```text
frontend/app.py
frontend/requirements.txt
frontend/templates/
frontend/static/
frontend/laptop.csv
```

後端爬蟲不直接在 Vercel 上執行，而是在本地端更新 `laptop.csv` 後，將更新後的 CSV 推送到 GitHub，再由 Vercel 重新部署。

---

## GitHub 協作規劃

分支規劃：

```text
main      # 穩定版本
tingyu    # 後端爬蟲、資料整理、CSV 匯出、更新資料
Elva      # 前端網站、頁面設計、推薦顯示
```



---

## 目前進度

已完成：

- Flask 網站基本架構
- Vercel 部署
- PChome API 資料取得
- 多頁商品資料抓取
- 品牌判斷
- CPU / RAM / SSD 擷取
- 商品網址欄位 `url`
- 重複資料清理
- 自動更新 CSV 程式
- 預算篩選
- 用途分類
- 推薦分數與推薦理由說明
- 排序功能
- README 文件

後續可加強：

- 增加更多資料來源
- 改善品牌與 CPU 辨識規則
- 加入更完整的使用者回饋紀錄
- 後端雲端化
- 增加圖表分析
- 進階規格篩選(指定CPU、SSD、RAM等)
- 強化商品連結與前端顯示細節
- 增加更多測試資料與錯誤處理


---

## 注意事項

- `__pycache__/` 與 `.pyc` 檔案為 Python 自動產生的暫存檔。
- 若有使用 `.gitignore`，建議加入：

```gitignore
__pycache__/
*.pyc
```
- 若修改爬蟲規則，請重新執行：

```bash
python backend/update_data.py
```

並確認 `frontend/laptop.csv` 是否正確更新。


---

## 專題網址

https://project-1142.vercel.app/

---