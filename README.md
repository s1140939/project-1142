# Python Flask 網站

一個基本的 Python Flask 網站示範，包含多個頁面和功能。

網址:https://project-1142.vercel.app/

## 🚀 快速開始

### 1. 安裝依賴
```bash
pip install -r frontend/requirements.txt
```

### 2. 運行網站
```bash
cd frontend
python app.py
```

### 3. 訪問網站
在瀏覽器中打開：`http://127.0.0.1:5000`

## 📁 項目結構

```
project-1142/
├── crawler/              # 網路爬蟲模塊
│   └── crawler.py
├── recommendation/       # 推薦系統模塊
│   └── recommendation.py
├── ui/                   # Flask 應用 (主要的網站)
│   ├── app.py           # Flask 應用主文件
│   ├── templates/       # HTML 模板
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── about.html
│   │   └── contact.html
│   └── static/          # 靜態資源 (CSS, JS, 圖片等)
├── data/                # 數據文件
│   ├── laptop.csv
│   └── feedback.csv
└── requirements.txt     # Python 依賴列表
```

## 🌐 網站功能

- **首頁** (`/`) - 展示網站介紹
- **關於** (`/about`) - 關於頁面
- **聯絡** (`/contact`) - 聯絡表單

## 📝 功能特點

- ✅ 基於 Flask 框架
- ✅ 響應式設計 (支持移動設備)
- ✅ 表單提交功能
- ✅ 簡潔的 HTML 和 CSS
- ✅ 易於擴展

## 🛠️ 開發提示

### 添加新頁面
1. 在 `app.py` 中添加路由
2. 在 `templates/` 中創建 HTML 文件
3. 確保使用 `{% extends "base.html" %}` 繼承基礎模板

### 添加靜態資源
將 CSS、JavaScript 和圖片放在 `static/` 文件夾中。

### 在 HTML 中引用靜態文件
```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<img src="{{ url_for('static', filename='image.png') }}" alt="Image">
```

## 🔗 相關資源

- [Flask 官方文檔](https://flask.palletsprojects.com/)
- [Jinja2 模板引擎](https://jinja.palletsprojects.com/)

## 📧 支持

如有問題，請通過聯絡頁面 (`/contact`) 與我們聯繫。

---
**創建日期：** 2026 年 5 月 22 日
