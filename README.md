# 筆電推薦系統 Project 1142

本專案為大一 Python 程式設計期末專題，主題是「筆電推薦系統」。  
系統透過爬蟲取得 PChome 筆電商品資料，進行品牌、CPU、RAM、SSD、價格與商品連結等欄位整理，並提供前端網頁做篩選、排序與推薦展示。

目前專案已從原本的「CSV 靜態資料流」進一步擴充為「FastAPI + Neon PostgreSQL」後端架構：

```text
PChome 搜尋 API
        ↓
backend/crawler.py
        ↓
資料清理與規格擷取
        ↓
CSV 備份 / Neon PostgreSQL
        ↓
FastAPI API
        ↓
前端網站 / 推薦展示
```

前端部署網址：

```text
https://project-1142.vercel.app/
```

---

## 專案目標

使用者在挑選筆電時，常需要同時比較品牌、CPU、RAM、SSD、價格與使用情境。本專案希望透過 Python 自動取得並整理電商資料，將商品名稱中的非結構化規格轉換成可推薦、可篩選、可排序的資料。

目前系統支援：

- 自動抓取 PChome 筆電資料
- 品牌辨識
- CPU / RAM / SSD 規格擷取
- 商品價格擷取
- 商品原網址產生
- 重複商品清理
- CSV 更新
- PostgreSQL 資料庫更新
- FastAPI 查詢與推薦 API
- Flask 前端展示
- 預算篩選
- 使用情境分類
- 推薦分數與推薦理由
- 「了解更多」連回商品原頁

---

## 專案結構

```text
project-1142/
├── backend/
│   ├── brand_map.py          # 品牌與型號對應規則
│   ├── crawler.py            # PChome API 爬蟲與資料清理
│   ├── database.py           # SQLAlchemy 與 DATABASE_URL 連線設定
│   ├── import_csv_to_db.py   # 將 frontend/laptop.csv 匯入 PostgreSQL
│   ├── init_db.py            # 建立資料庫資料表
│   ├── main.py               # FastAPI 主程式
│   ├── models.py             # SQLAlchemy Laptop 資料表模型
│   ├── update_data.py        # 更新 frontend/laptop.csv
│   └── update_database.py    # FastAPI 觸發爬蟲並更新 PostgreSQL
│
├── frontend/
│   ├── app.py                # Flask 前端網站
│   ├── laptop.csv            # CSV 版筆電資料
│   ├── requirements.txt      # 前端執行所需套件
│   ├── static/
│   │   └── style.css         # 網頁樣式
│   └── templates/
│       ├── base.html         # 共用版型
│       ├── index.html        # 首頁與推薦展示頁
│       ├── about.html        # 關於頁
│       └── contact.html      # 聯絡頁
│
├── feedback.csv              # 使用者回饋資料
├── requirements.txt          # 後端 / 全專案套件需求
├── .gitignore                # Git 忽略規則
└── README.md                 # 專案說明文件
```

---

## 使用技術

### 後端與資料處理

- Python
- requests
- pandas
- Regular Expression
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL
- Neon PostgreSQL
- python-dotenv

### 前端

- Flask
- HTML
- CSS
- Jinja2 Template

### 協作與部署

- GitHub
- Git branch / commit / pull request
- Vercel
- Neon PostgreSQL
- Render（可作為 FastAPI 後端部署目標）

---

## 資料來源

本專案目前使用 PChome 搜尋 API 取得商品資料，而不是直接解析前端 HTML。  
原因是 PChome 商品列表頁面多由 JavaScript 動態載入，直接用 BeautifulSoup 解析 HTML 時不容易取得完整商品資料。

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

目前 `crawler.py` 抓取第 1 到第 10 頁資料。

---

## 後端資料處理流程

```text
PChome 搜尋 API
        ↓
requests 取得 JSON 商品資料
        ↓
讀取商品名稱、價格與商品 ID
        ↓
組合商品原始網址
        ↓
brand_map.py 判斷品牌
        ↓
Regular Expression 擷取 CPU / RAM / SSD
        ↓
pandas 建立 DataFrame
        ↓
依價格排序
        ↓
根據商品名稱去除重複資料
        ↓
輸出 CSV 或回傳 DataFrame 給資料庫更新程式
```

`crawler.py` 中主要函式：

```python
crawl_laptops(save_csv=True)
```

用途：

| 呼叫方式 | 功能 |
|---|---|
| `crawl_laptops(save_csv=True)` | 更新 `frontend/laptop.csv` |
| `crawl_laptops(save_csv=False)` | 不輸出 CSV，直接回傳 DataFrame 給資料庫更新流程 |
| `run_crawler()` | 預設執行 CSV 更新流程 |

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
Vivobook 15...,ASUS,16GB,1024GB,Core 7 150U,23999,https://24h.pchome.com.tw/prod/...
```

---

## 品牌辨識

品牌判斷規則集中放在：

```text
backend/brand_map.py
```

主要使用「系列名稱 → 主品牌」的方式整理，例如：

| 系列 / 關鍵字 | 對應品牌 |
|---|---|
| Vivobook / Zenbook / ROG / TUF | ASUS |
| Aspire / AL 系列 / Swift / Nitro | Acer |
| IdeaPad / ThinkPad / ThinkBook / Legion | Lenovo |
| Pavilion / Victus / Omen / EliteBook | HP |
| Surface | Microsoft |
| MacBook | Apple |

若商品名稱中沒有明顯系列名稱，則透過 `model_map` 使用型號規則進行補充判斷，例如：

| 型號規則 | 推測品牌 |
|---|---|
| `X\d+` | ASUS |
| `AL\d+` | Acer |
| `83[A-Z0-9]+` | Lenovo |

---

## 規格擷取

`crawler.py` 透過 Regular Expression 從商品名稱中擷取規格。

目前支援：

### CPU

- Intel i 系列：`i5-13420H`、`i7-13620H`
- Intel Core 新命名：`Core 5 120U`、`Core 7 150U`
- Intel Ultra：`Ultra 5 125H`、`Ultra5-125H`
- Ryzen：`Ryzen 5 7430U`、`R5-7430U`、`R7 8840HS`
- Celeron：`Celeron N4500`
- Intel N 系列：`N150`、`N355`

### RAM

- `4G`
- `8G`
- `16G`
- `8GB+8GB`

系統會避免將 SSD 容量誤判為 RAM，並將可加總的 RAM 做整理。

### SSD

- `128G / 128GB`
- `256G / 256GB`
- `512G / 512GB`
- `1TB`

其中 `1TB` 會轉換成：

```text
1024GB
```

---

## 重複資料處理

商品資料可能因為排序或頁面重複而出現相同商品，因此輸出前會進行去重複處理。

目前 CSV 版流程：

1. 先依價格由低到高排序
2. 再根據商品名稱 `name` 去重複
3. 保留價格較低的商品資料
4. 驗證去重後是否仍有重複商品

執行時會在終端機顯示：

```text
原始筆數: 200
找到重複: 57
去重後: 165
剩餘重複: 0
```

資料庫版流程則會進一步處理：

1. 從 `url` 擷取 PChome 商品 ID
2. 產生 `product_id`
3. 若 `product_id` 為空，使用 `name + price` 產生備用 ID
4. 依 `product_id` 去重複
5. 寫入 PostgreSQL

這樣可以避免 PostgreSQL 的 `unique constraint` 衝突。

---

## PostgreSQL 資料庫設計

資料庫模型位於：

```text
backend/models.py
```

資料表名稱：

```text
laptops
```

主要欄位：

| 欄位 | 說明 |
|---|---|
| `id` | 資料庫內部流水號 |
| `product_id` | 商品唯一識別碼，優先由 PChome 商品網址擷取 |
| `name` | 商品名稱 |
| `brand` | 品牌 |
| `cpu` | CPU |
| `ram` | RAM |
| `ssd` | SSD |
| `price` | 價格 |
| `url` | 商品原網址 |
| `updated_at` | 建立 / 更新時間 |

`product_id` 設定為唯一值，用於避免相同商品重複寫入資料庫。

---

## FastAPI 後端

FastAPI 主程式：

```text
backend/main.py
```

啟動方式：

```bash
cd backend
uvicorn main:app --reload
```

啟動後可打開：

```text
http://127.0.0.1:8000/docs
```

### API 端點

| 方法 | 路徑 | 功能 |
|---|---|---|
| GET | `/` | 確認 API 是否啟動 |
| GET | `/api/health` | 檢查資料庫連線與資料筆數 |
| GET | `/api/laptops` | 取得筆電資料，可依品牌、最高價格、最低 RAM 篩選 |
| GET | `/api/recommend` | 根據用途、預算、品牌取得推薦結果 |
| POST | `/api/update` | 觸發爬蟲，直接更新 PostgreSQL 資料庫 |

### `/api/laptops` 查詢範例

```text
http://127.0.0.1:8000/api/laptops
```

依品牌與價格篩選：

```text
http://127.0.0.1:8000/api/laptops?brand=ASUS&max_price=30000
```

依最低 RAM 篩選：

```text
http://127.0.0.1:8000/api/laptops?min_ram=16
```

### `/api/recommend` 查詢範例

```text
http://127.0.0.1:8000/api/recommend?usage=程式&max_price=35000&brand=ASUS
```

回傳內容包含：

- 使用情境
- 預算上限
- 品牌
- 推薦資料筆數
- 商品資料
- 推薦分數 `score`

### `/api/update`

可在 Swagger UI 中執行：

```text
POST /api/update
```

用途：

```text
FastAPI
    ↓
update_database.py
    ↓
crawler.py
    ↓
PChome API
    ↓
資料清理
    ↓
Neon PostgreSQL
```

成功回傳範例：

```json
{
  "status": "success",
  "message": "資料庫更新完成",
  "count": 165
}
```

---

## 資料庫環境變數

本專案使用 `.env` 儲存 Neon PostgreSQL 連線字串。

`.env` 範例：

```env
DATABASE_URL=postgresql://使用者:密碼@主機名稱/資料庫名稱?sslmode=require
```

注意：

- `.env` 含有資料庫密碼，不可上傳 GitHub
- `.gitignore` 已加入 `.env`
- 若 `.env` 曾經被 Git 追蹤過，需使用下列指令取消追蹤：

```bash
git rm --cached .env
```

---

## 安裝與執行方式

### 1. 下載專案

```bash
git clone https://github.com/s1140939/project-1142.git
cd project-1142
```

### 2. 安裝套件

建議先安裝主要套件：

```bash
pip install flask requests beautifulsoup4 pandas fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
```

或使用 requirements：

```bash
pip install -r requirements.txt
```

若只執行前端，可使用：

```bash
pip install -r frontend/requirements.txt
```

---

## 使用方式

### 更新 CSV

在專案根目錄執行：

```bash
python backend/update_data.py
```

此指令會重新產生：

```text
frontend/laptop.csv
```

### 建立資料表

第一次使用 PostgreSQL 時執行：

```bash
cd backend
python init_db.py
```

### 將 CSV 匯入資料庫

```bash
cd backend
python import_csv_to_db.py
```

### 啟動 FastAPI

```bash
cd backend
uvicorn main:app --reload
```

開啟：

```text
http://127.0.0.1:8000/docs
```

### 透過 FastAPI 更新資料庫

在 Swagger UI 執行：

```text
POST /api/update
```

或使用 curl：

```bash
curl -X POST http://127.0.0.1:8000/api/update
```

### 啟動 Flask 前端

```bash
python frontend/app.py
```

開啟：

```text
http://127.0.0.1:5000
```

---

## 前端功能

目前前端位於：

```text
frontend/app.py
```

網站功能包含：

- 首頁 `/`
- 關於頁 `/about`
- 聯絡頁 `/contact`
- 讀取 `frontend/laptop.csv`
- 顯示筆電商品卡片
- 預算篩選
- 使用情境篩選
- 推薦分數排序
- 價格排序
- 推薦理由說明
- 商品原網址連結

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

目前前端仍以 CSV 為主要讀取來源；FastAPI + PostgreSQL 已完成後端資料層，後續可將前端改為直接呼叫 `/api/laptops` 或 `/api/recommend`。

---

## 部署方式

### 前端部署

本專案前端目前使用 Vercel 部署。

建議 Vercel 設定：

```text
Root Directory: frontend
```

Vercel 主要讀取：

```text
frontend/app.py
frontend/requirements.txt
frontend/templates/
frontend/static/
frontend/laptop.csv
```

### 後端部署

FastAPI 後端目前可在本地端執行，也可部署到 Render 等後端服務。

若部署 FastAPI，需要在部署平台設定環境變數：

```text
DATABASE_URL = Neon PostgreSQL 連線字串
```

後端部署後，前端可改為呼叫雲端 API：

```text
https://你的後端網址/api/laptops
```

---

## GitHub 協作規劃

分支規劃：

```text
main      # 穩定版本
tingyu    # 後端爬蟲、資料清理、CSV / PostgreSQL / FastAPI
Elva      # 前端網站、頁面設計、推薦顯示
```

---

## 目前進度

已完成：

- Flask 前端網站基本架構
- Vercel 前端部署
- PChome API 資料取得
- 多頁商品資料抓取
- 品牌辨識
- CPU / RAM / SSD 擷取
- 商品網址欄位 `url`
- 重複資料清理
- CSV 更新程式
- Neon PostgreSQL 資料庫連線
- SQLAlchemy 資料表模型
- CSV 匯入 PostgreSQL
- FastAPI 後端
- `/api/health`
- `/api/laptops`
- `/api/recommend`
- `/api/update`
- FastAPI 觸發爬蟲並更新資料庫
- README 文件整理

後續可加強：

- 將前端資料來源由 CSV 改為 FastAPI
- 將 FastAPI 部署到 Render
- 增加更多資料來源
- 改善品牌與 CPU 辨識規則
- 加入更完整的使用者回饋紀錄
- 增加圖表分析
- 增加進階規格篩選，例如指定 CPU、SSD、RAM
- 增加更新時間顯示
- 改善錯誤處理與 API 權限控制

---

## 注意事項

### 不要上傳 `.env`

`.env` 內含 Neon PostgreSQL 的帳號密碼，不應上傳 GitHub。  
目前 `.gitignore` 建議包含：

```gitignore
.env
__pycache__/
*.pyc
.venv/
venv/
```

### 不要上傳 Python 暫存檔

以下檔案不需要進入 GitHub：

```text
__pycache__/
*.pyc
```

### 重新更新資料後要測試

若修改爬蟲規則，請依序測試：

```bash
python backend/update_data.py
cd backend
uvicorn main:app --reload
```

並在 Swagger 測試：

```text
POST /api/update
GET /api/health
GET /api/laptops
```

---

## 專題網址

前端網址：

```text
https://project-1142.vercel.app/
```

---

## 簡要成果

本專題已完成從資料取得、資料清理、CSV 輸出、前端推薦展示，到 FastAPI + PostgreSQL 後端資料流的階段性整合。  
目前後端可透過 `/api/update` 觸發爬蟲並更新雲端資料庫，代表系統已從單純 CSV 架構升級為可雲端化的 API 架構。
