# 筆電推薦系統 Project 1142

本專案為大一 Python 程式設計期末專題，主題是「筆電推薦系統」。系統會自動取得電商平台上的筆電資料，將商品名稱中的規格資訊整理成可分析的資料，並透過網站與 API 提供查詢、篩選、分析與推薦功能。

目前專案已完成從「爬蟲 → 資料庫 → API → 前端網站」的串接流程：

```text
PChome 搜尋 API
        ↓
backend/crawler.py
        ↓
資料清理：品牌 / CPU / RAM / SSD / 價格 / 商品網址
        ↓
Neon PostgreSQL
        ↓
Render FastAPI
        ↓
Vercel Flask 前端網站
```

前端目前已改為 **優先直接讀取 Render FastAPI**，若 API 暫時無法連線，才會自動改用本地 `frontend/laptop.csv` 作為備援資料。

---

## 已部署網址

| 類型 | 平台 | 網址 |
|---|---|---|
| 前端網站 | Vercel | https://project-1142.vercel.app/ |
| 後端 API | Render | https://project-1142-backend.onrender.com |
| API 文件 | Render Swagger | https://project-1142-backend.onrender.com/docs |

---

## 專案目標

使用者在選購筆電時，常需要比較品牌、CPU、RAM、SSD、價格與使用情境。本專案希望透過 Python 自動化整理電商資料，將原本混在商品名稱中的規格轉換成結構化資料，再依照用途、預算與規格條件提供推薦結果。

本專案目前可整理與展示的欄位包含：

- 商品名稱
- 品牌
- CPU
- RAM
- SSD
- 價格
- 商品原始網址
- 商品唯一識別碼 `product_id`
- 使用情境分類
- 推薦分數
- 推薦原因

---

## 系統架構

### 目前整體架構

```text
PChome 搜尋 API
        ↓
backend/crawler.py
        ↓
資料清理與 DataFrame 整理
        ↓
update_database.py
        ↓
Neon PostgreSQL laptops 資料表
        ↓
Render FastAPI
        ↓
frontend/app.py 呼叫 /api/laptops
        ↓
Flask + Jinja 模板顯示商品卡片
        ↓
Vercel 前端網站
```

### API 資料流程

```text
使用者開啟 Vercel 前端
        ↓
frontend/app.py
        ↓
requests.get("https://project-1142-backend.onrender.com/api/laptops")
        ↓
Render FastAPI 從 Neon PostgreSQL 讀取資料
        ↓
回傳 JSON
        ↓
前端進行用途分類、推薦評分、篩選與排序
        ↓
網頁顯示推薦結果
```

### CSV 備援流程

```text
若 Render API 無法連線
        ↓
frontend/app.py 例外處理
        ↓
改讀 frontend/laptop.csv
        ↓
前端仍可維持基本展示功能
```

CSV 目前作為備援與測試資料來源，主要正式資料來源已改為 Render FastAPI。

---

## 專案結構

```text
project-1142/
├── backend/
│   ├── main.py              # FastAPI 後端入口，提供 API endpoints
│   ├── crawler.py           # 爬蟲與資料清理主程式
│   ├── update_data.py       # 更新 frontend/laptop.csv，作為 CSV 備援資料
│   ├── update_database.py   # 觸發爬蟲後更新 PostgreSQL
│   ├── database.py          # PostgreSQL / Neon 資料庫連線
│   ├── models.py            # SQLAlchemy Laptop 資料表模型
│   ├── init_db.py           # 建立資料表
│   ├── import_csv_to_db.py  # 將既有 CSV 匯入資料庫
│   ├── brand_map.py         # 品牌與型號判斷規則
│   └── requirements.txt     # Render 後端部署套件需求
│
├── frontend/
│   ├── app.py               # Flask 前端，優先呼叫 Render FastAPI
│   ├── laptop.csv           # API 無法連線時的備援資料
│   ├── requirements.txt     # Vercel 前端部署套件需求
│   ├── static/
│   │   └── style.css        # 網站樣式
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── about.html
│       └── contact.html
│
├── feedback.csv             # 使用者回饋資料
├── requirements.txt         # 專案整體套件紀錄:">?
>
"?:
├── .gitignore               # 忽略 .env、__pycache__ 等檔案
└── README.md
```

---

## 使用技術

| 類別 | 技術 |
|---|---|
| 程式語言 | Python |
| 前端網站 | Flask、Jinja2、HTML、CSS |
| 前端資料串接 | requests 呼叫 Render FastAPI |
| 後端 API | FastAPI、Uvicorn |
| 資料庫 | PostgreSQL、Neon |
| ORM | SQLAlchemy |
| 資料處理 | pandas、Regular Expression |
| 資料來源 | PChome 搜尋 API |
| 部署 | Vercel、Render |
| 協作 | GitHub、branch、commit、pull request |
| AI 輔助 | 程式除錯、regex 調整、README 整理、部署問題排查 |

---

## 資料來源

本專案使用 PChome 搜尋 API 取得筆電商品資料，而不是直接解析 PChome 前端 HTML。原因是 PChome 商品資料多由 JavaScript 動態載入，直接用 BeautifulSoup 解析 HTML 時不容易取得完整商品資料。

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

目前 `crawler.py` 會抓取第 1 到第 10 頁資料，因此原始資料量約為 200 筆，再經過去重複與清理後輸出可使用的筆電資料。

---

## 資料清理流程

`backend/crawler.py` 主要負責資料取得與清理，流程如下：

```text
requests 取得 JSON
        ↓
讀取商品名稱與價格
        ↓
取得商品 ID 並組合商品網址
        ↓
利用 brand_map.py 判斷品牌
        ↓
利用 regex 擷取 CPU / RAM / SSD
        ↓
pandas 建立 DataFrame
        ↓
依價格排序
        ↓
根據商品名稱去重複
        ↓
回傳 DataFrame 給資料庫更新流程，或輸出 CSV 作為備援
```

### 品牌辨識

品牌判斷規則集中在：

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

若商品名稱中沒有明顯品牌或系列名稱，則會再透過型號規則補充判斷。

### CPU 擷取

目前支援常見格式，例如：

- Intel i3 / i5 / i7 / i9
- Intel Core 3 / Core 5 / Core 7
- Intel Ultra 5 / Ultra 7
- Ryzen 3 / Ryzen 5 / Ryzen 7
- R5、R7 等簡寫
- Celeron
- Intel N 系列

### RAM 擷取

可處理：

```text
8G
8GB
16G
8GB+8GB
```

並避免將 SSD 容量誤判為 RAM。

### SSD 擷取

可處理：

```text
128GB
256GB
512GB
1TB
```

其中 TB 會轉換為 GB，例如：

```text
1TB → 1024GB
```

---

## CSV 備援資料

雖然目前前端已改為優先讀取 Render FastAPI，但專案仍保留：

```text
frontend/laptop.csv
```

此 CSV 用於：

1. API 暫時無法連線時的備援資料
2. 本機測試前端畫面
3. 展示原本 CSV 流程的開發成果

CSV 欄位包含：

| 欄位 | 說明 |
|---|---|
| `name` | 商品完整名稱 |
| `brand` | 品牌，例如 ASUS、Acer、Lenovo、HP |
| `RAM` | 記憶體容量，例如 8GB、16GB |
| `SSD` | 儲存容量，例如 512GB、1024GB |
| `CPU` | 處理器型號，例如 i5-13420H、R7-8840HS、N150 |
| `price` | 商品價格 |
| `url` | 商品在 PChome 的原始網址 |

更新 CSV：

```bash
cd backend
python update_data.py
```

---

## PostgreSQL 資料庫設計

資料庫使用 Neon PostgreSQL。資料表模型定義在：

```text
backend/models.py
```

主要資料表：

```text
laptops
```

欄位：

| 欄位 | 說明 |
|---|---|
| `id` | 資料庫流水號 |
| `product_id` | 商品唯一識別碼，設為 unique |
| `name` | 商品名稱 |
| `brand` | 品牌 |
| `cpu` | CPU |
| `ram` | RAM |
| `ssd` | SSD |
| `price` | 價格 |
| `url` | 商品原始網址 |
| `updated_at` | 資料更新時間 |

`product_id` 的產生方式：

1. 優先使用資料中的 `product_id` / `Id`
2. 若沒有，則從商品網址中的 `/prod/` 後方擷取
3. 若網址仍無法取得，則使用 `name + price` 產生 fallback hash
4. 寫入資料庫前會移除空白 `product_id` 並依 `product_id` 去重複

此設計是為了解決 PostgreSQL unique constraint 錯誤，避免多筆空白 `product_id` 寫入造成重複鍵衝突。

---

## FastAPI 後端功能

後端入口：

```text
backend/main.py
```

目前 API endpoints：

| Method | Endpoint | 功能 |
|---|---|---|
| GET | `/` | 確認 API 是否啟動 |
| GET | `/api/health` | 檢查資料庫連線與目前筆電資料筆數 |
| GET | `/api/laptops` | 從 PostgreSQL 取得筆電資料，可依品牌、價格、RAM 篩選 |
| GET | `/api/recommend` | 依用途、預算、品牌與數量限制回傳推薦結果 |
| POST | `/api/update` | 觸發爬蟲，重新抓取資料並更新 PostgreSQL |

### `/api/laptops` 查詢參數

| 參數 | 說明 | 範例 |
|---|---|---|
| `brand` | 品牌篩選 | `ASUS` |
| `max_price` | 價格上限 | `30000` |
| `min_ram` | RAM 下限 | `16` |

範例：

```text
/api/laptops?brand=ASUS&max_price=30000&min_ram=16
```

### `/api/recommend` 查詢參數

| 參數 | 說明 | 預設值 |
|---|---|---|
| `usage` | 使用情境，例如文書、程式、遊戲 | 文書 |
| `max_price` | 預算上限 | 30000 |
| `brand` | 品牌篩選，可不填 | None |
| `limit` | 回傳數量 | 10 |

範例：

```text
/api/recommend?usage=程式&max_price=30000&limit=5
```

### `/api/update` 更新流程

```text
POST /api/update
        ↓
update_database_from_crawler(db)
        ↓
crawl_laptops(save_csv=False)
        ↓
整理 product_id
        ↓
移除空白 ID
        ↓
依 product_id 去重複
        ↓
清空舊資料
        ↓
寫入新資料
        ↓
回傳更新筆數
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

## 前端網站功能

前端入口：

```text
frontend/app.py
```

目前前端已完成「由 CSV 改為直接讀取 Render FastAPI」的串接。

核心設定：

```python
API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://project-1142-backend.onrender.com"
)

API_URL = f"{API_BASE_URL}/api/laptops"
```

資料讀取邏輯：

```text
load_laptops()
        ↓
優先執行 load_laptops_from_api()
        ↓
requests.get(API_URL)
        ↓
若成功，使用 API 回傳資料
        ↓
若失敗，進入 except，改用 load_laptops_from_csv()
```

前端提供以下功能：

- 顯示筆電商品卡片
- 依用途分類：日常 / 學習、商務、創作 / 專業、影音 / 娛樂
- 輸入預算進行篩選
- 依 RAM 範圍篩選
- 依 SSD 範圍篩選
- 依 CPU 關鍵字篩選
- 依品牌篩選
- 依推薦分數或價格排序
- 顯示商品分析圖表資料
- 顯示推薦原因
- 點擊「了解更多」前往商品原始網址
- API 失敗時自動使用 CSV 備援

---

## 本機執行方式

### 1. 建立環境變數

在專案根目錄或 `backend/` 建立 `.env`：

```env
DATABASE_URL=postgresql://使用者:密碼@主機/laptop_db?sslmode=require
```

`.env` 內含資料庫帳密，不應上傳 GitHub。

前端若要指定不同後端，也可以設定：

```env
API_BASE_URL=https://project-1142-backend.onrender.com
```

若未設定，`frontend/app.py` 會使用預設的 Render 後端網址。

---

### 2. 初始化資料庫

```bash
cd backend
python init_db.py
```

---

### 3. 更新 CSV 備援資料

```bash
cd backend
python update_data.py
```

此指令會重新爬取資料並更新：

```text
frontend/laptop.csv
```

---

### 4. 匯入既有 CSV 到資料庫

```bash
cd backend
python import_csv_to_db.py
```

---

### 5. 啟動 FastAPI 後端

```bash
cd backend
uvicorn main:app --reload
```

開啟：

```text
http://127.0.0.1:8000/docs
```

可在 Swagger 中測試：

```text
GET /api/health
GET /api/laptops
GET /api/recommend
POST /api/update
```

---

### 6. 啟動 Flask 前端

```bash
cd frontend
python app.py
```

開啟：

```text
http://127.0.0.1:5000
```

啟動後，前端會優先向 Render FastAPI 取得資料。若終端機出現：

```text
使用 API 讀取資料，筆數：...
```

代表前端已成功讀取 Render 後端資料。

若 API 讀取失敗，會出現：

```text
API 讀取失敗，改用 CSV：...
```

此時前端會自動改用 `frontend/laptop.csv`。

---

## Render 後端部署設定

本專案後端已部署至 Render，部署設定如下：

| 設定項目 | 值 |
|---|---|
| Service Type | Web Service |
| Runtime | Python |
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Environment Variable | `DATABASE_URL` |
| Database | Neon PostgreSQL |

部署完成後可測試：

```text
https://project-1142-backend.onrender.com/
https://project-1142-backend.onrender.com/api/health
https://project-1142-backend.onrender.com/api/laptops
https://project-1142-backend.onrender.com/docs
```

---

## Vercel 前端部署

前端已部署於 Vercel：

```text
https://project-1142.vercel.app/
```

目前 Vercel 前端會直接呼叫 Render FastAPI：

```text
https://project-1142-backend.onrender.com/api/laptops
```

建議在 Vercel 的 Environment Variables 設定：

```text
API_BASE_URL=https://project-1142-backend.onrender.com
```

這樣未來若後端網址更換，只需要改 Vercel 環境變數，不必修改程式碼。

---

## GitHub 協作與版本紀錄

本專案使用 GitHub 管理版本，開發過程包含多次 commit，紀錄了從爬蟲測試、API 路徑確認、品牌判斷、CPU 擷取、資料去重複、CSV 更新機制，到 FastAPI / PostgreSQL / Render 部署，以及前端改讀 Render API 、篩選機制變更的完整開發歷程。

---

## 目前完成進度

已完成：

- PChome 搜尋 API 資料取得
- 筆電商品名稱、價格、網址擷取
- 品牌、CPU、RAM、SSD 規格整理
- CSV 輸出與更新機制
- CSV 備援讀取機制
- Flask 前端網站
- 前端改為優先讀取 Render FastAPI
- 前端篩選、排序、推薦分數與商品分析
- Vercel 前端部署
- Neon PostgreSQL 資料庫
- SQLAlchemy 資料表模型
- CSV 匯入資料庫
- FastAPI 後端 API
- `POST /api/update` 觸發爬蟲更新資料庫
- Render 後端部署
- Vercel 前端串接 Render 後端 API

後續可改進：

- 將 CORS `allow_origins=["*"]` 改為只允許正式前端網址
- 增加定期自動更新資料庫機制
- 增加更多資料來源或商品平台
- 改善推薦演算法，例如加入 GPU、重量、螢幕尺寸與使用者偏好權重
- 將前端推薦邏輯逐步搬到後端 `/api/recommend`，讓前端更單純負責畫面呈現
- 增加使用者回饋資料分析

---

## 注意事項

1. `.env` 內含資料庫連線字串，不可上傳 GitHub。
2. 若 `.env` 曾經被 Git 追蹤，需執行：

```bash
git rm --cached .env
git commit -m "Remove env file from git tracking"
```

3. `__pycache__/`、`*.pyc` 與 `.git/` 不應放入繳交壓縮檔或手動上傳檔案。
4. Render Free 服務在一段時間沒有流量後可能休眠，因此第一次開啟 API 可能需要等待較久。
5. `/api/update` 會重新爬資料並寫入資料庫，執行時間會比一般查詢 API 更久。
6. 目前前端具備 CSV fallback，因此即使 API 暫時失敗，仍可維持基本展示。

---

## Demo 建議流程

1. 開啟前端網站：`https://project-1142.vercel.app/`
2. 展示前端頁面可正常載入 Render API 資料
3. 展示使用者可依用途、預算、RAM、SSD、CPU、品牌與排序方式查看推薦商品
4. 點擊「了解更多」，展示可連到 PChome 商品原始頁面
5. 開啟後端 API 文件：`https://project-1142-backend.onrender.com/docs`
6. 執行 `GET /api/health`，確認資料庫連線與資料筆數
7. 執行 `GET /api/laptops`，展示資料庫中的筆電資料
8. 執行 `GET /api/recommend`，展示後端推薦 API
9. 視時間執行 `POST /api/update`，展示可由 API 觸發爬蟲更新資料庫

---

## 專案總結

本專案從原本單純的 CSV 爬蟲與前端展示，逐步擴充為包含資料庫、API、前後端部署與前端 API 串接的完整系統。透過 PChome API、資料清理、CSV 備援、Flask、FastAPI、Neon PostgreSQL、Render 與 Vercel，完成了從資料取得、規格分析、資料儲存、API 查詢到網站展示的整合流程。

目前系統已具備期末專題所需的資料蒐集、資料處理、網頁展示、GitHub 協作、前端部署、後端部署與前後端串接成果。整體架構已從「讀取本地 CSV」升級為「前端直接讀取雲端 FastAPI」，更接近實際產品的資料流設計。
