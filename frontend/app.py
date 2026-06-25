from flask import Flask, render_template, request
import csv
import os
import requests

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
DATA_PATH = os.path.join(os.path.dirname(__file__), 'laptop.csv')
API_URL = "http://127.0.0.1:8000/api/laptops"

"""
篩選分類(全部用途、日常學習、商務、創作專業、影音娛樂)
"""
def get_number(text):
    text = str(text).upper().replace('GB','').strip()
    try:
        return int(text)
    except :
        return 0

def classify_use_case(row):
    name=row.get('name', '').lower()
    cpu=row.get('CPU', '').lower()
    ram=get_number(row.get('RAM', 0))
    ssd=get_number(row.get('SSD', 0))

    """
    創作專業:高階CPU or 大記憶體
    """
    if(
        'i7' in cpu or 'i9' in cpu or 'r7' in cpu or 'ryzen 7' in cpu or 'r9' in cpu or 'ryzen 9' in cpu or 'core 7' in cpu or ram >=16 and not('celeron' in cpu or 'n4500' in cpu or 'n150' in cpu or 'n100' in cpu or 'n200' in cpu or 'n6000' in cpu)

    ):
        return '創作/專業'

    """
    影音娛樂:中階CPU + 大容量
    """
    if(
        ('i5' in cpu or 'r5' in cpu or 'ryzen 5' in cpu or 'core 5' in cpu or 'ultra 5' in cpu or 'ultra5' in cpu ) and ssd >=512
    ):
        return '影音/娛樂'

    """
    商務:中低階，適合辦公、多工
    """
    if(
        '商' in name or 'business' in name or 'i3' in cpu or 'r3' in cpu or 'ryzen 3' in cpu or 'core 3'in cpu or 'c3' in cpu or 'c5' in cpu or (ram >= 8 and ssd >= 256)
    ):
        return '商務'

    """
    日常學習:入門文書機
    """
    return '日常/學習'

def get_recommend_score(row):
    score = 0
    reasons = []

    use_case = row.get("UseCase", "")
    cpu = row.get("CPU", "").lower()
    ram = get_number(row.get("RAM", "0"))
    ssd = get_number(row.get("SSD", "0"))
    price = row.get("price", 0)

    # ---------- 日常 / 學習 ----------
    if use_case == "日常/學習":
        if ram >= 8:
            score += 30
            reasons.append("RAM 達 8GB 以上，可應付文書處理、線上課程與多分頁瀏覽。")
        else:
            score += 15
            reasons.append("RAM 容量較低，較適合基本文書與輕量網頁瀏覽。")

        if ssd >= 256:
            score += 30
            reasons.append("SSD 容量足以存放課堂資料、報告檔案與常用軟體。")
        else:
            score += 15
            reasons.append("SSD 容量較小，適合檔案量不大的學習用途。")

        if price <= 25000:
            score += 25
            reasons.append("價格落在學生族群較容易接受的範圍內，適合作為學習用筆電。")
        else:
            score += 15
            reasons.append("價格較高，但規格可提供更穩定的日常使用體驗。")

        score += 15
        reasons.append("整體配置適合上課、查資料、寫報告與一般日常使用。")

    # ---------- 商務 ----------
    elif use_case == "商務":
        if ram >= 16:
            score += 30
            reasons.append("RAM 16GB 以上，可支援多個辦公軟體與瀏覽器分頁同時執行。")
        elif ram >= 8:
            score += 25
            reasons.append("RAM 8GB 以上，可應付一般辦公、簡報與視訊會議需求。")
        else:
            score += 10
            reasons.append("RAM 較低，較適合基本辦公使用。")

        if ssd >= 512:
            score += 25
            reasons.append("SSD 512GB 以上，適合存放工作文件、簡報與常用商務軟體。")
        else:
            score += 15
            reasons.append("SSD 容量可支援基本文件儲存，但大量資料可能較受限制。")

        if any(key in cpu for key in ["i5", "i7", "i9", "ryzen 5", "ryzen 7", "ryzen 9", "core 5", "core 7"]):
            score += 30
            reasons.append("處理器效能足以應付多工辦公、資料處理與線上會議。")
        else:
            score += 15
            reasons.append("處理器適合基本辦公，但大量多工時效能可能較有限。")

        score += 15
        reasons.append("整體規格適合作為辦公、簡報與日常商務使用。")

    # ---------- 創作 / 專業 ----------
    elif use_case == "創作/專業":
        if ram >= 32:
            score += 35
            reasons.append("RAM 達 32GB 以上，適合大型專案、多工處理與專業軟體使用。")
        elif ram >= 16:
            score += 30
            reasons.append("RAM 16GB 以上，可支援創作軟體、程式開發與多工操作。")
        elif ram >= 8:
            score += 18
            reasons.append("RAM 8GB 可支援基礎創作工作，但較大型專案可能較吃力。")
        else:
            score += 8
            reasons.append("RAM 較低，較不適合長時間專業創作或大型軟體使用。")

        if ssd >= 1024:
            score += 25
            reasons.append("1TB SSD 提供充足空間，適合存放專案檔、素材與大型軟體。")
        elif ssd >= 512:
            score += 22
            reasons.append("SSD 512GB 以上，可存放常用創作軟體與一般專案檔案。")
        else:
            score += 10
            reasons.append("SSD 容量較小，若存放素材或專案檔可能需要外接儲存設備。")

        if any(key in cpu for key in ["i7", "i9", "ryzen 7", "ryzen 9", "core 7", "ultra 7"]):
            score += 35
            reasons.append("高階處理器具備較佳運算能力，適合影像處理、程式開發與多工工作。")
        elif any(key in cpu for key in ["i5", "ryzen 5", "core 5", "ultra 5"]):
            score += 25
            reasons.append("中階處理器可應付基礎創作與一般專業工作。")
        else:
            score += 12
            reasons.append("處理器較偏入門，較適合輕量創作或基本工作。")

        score += 5
        reasons.append("整體配置會依 RAM、SSD 與 CPU 表現判斷是否適合創作與專業用途。")

    # ---------- 影音 / 娛樂 ----------
    elif use_case == "影音/娛樂":

        if ram >= 8:
            score += 30
            reasons.append("RAM 8GB 以上，可支援影音播放、瀏覽器與娛樂應用同時使用。")
        else:
            score += 15
            reasons.append("RAM 較低，適合基本影音播放，但多工表現較有限。")

        if ssd >= 512:
            score += 30
            reasons.append("SSD 512GB 以上，可存放影片、音樂與常用娛樂軟體。")
        else:
            score += 15
            reasons.append("SSD 容量可支援基本娛樂使用，但大量影音檔案可能較不足。")

        if any(key in cpu for key in ["i5", "i7", "i9", "ryzen 5", "ryzen 7", "core 5", "core 7"]):
            score += 40
            reasons.append("處理器效能足以應付影音播放、串流平台與一般娛樂需求。")
        else:
            score += 20
            reasons.append("處理器適合基本影音播放與日常娛樂使用。")

    # ---------- 沒分類時 ----------
    else:
        score = 70
        reasons.append("此商品尚未明確分類，系統會以一般規格進行基本推薦。")
        reasons.append("可依 RAM、SSD、CPU 與價格判斷是否符合使用需求。")

    return min(score, 100), reasons[:3]

def load_laptops_from_api():
    response = requests.get(API_URL, timeout=5)
    response.raise_for_status()
    data = response.json()
    laptops = data.get("data", [])

    for row in laptops:
        row['price'] = int(row.get('price', '0') or '0')
        row['UseCase'] = classify_use_case(row)
        row['Score'], row['Reason'] = get_recommend_score(row)

    return laptops

def load_laptops_from_csv():
    laptops = []
    if not os.path.exists(DATA_PATH):
        return laptops

    with open(DATA_PATH, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['price'] = int(row.get('price', '0') or '0')
            row['UseCase'] = classify_use_case(row)
            row['Score'], row['Reason'] = get_recommend_score(row)
            laptops.append(row)

    return laptops

def load_laptops():
    try:
        return load_laptops_from_api()
    except Exception as e:
        print("API 讀取失敗，改用 CSV：", e)
        return load_laptops_from_csv()


def filter_laptops(laptops, use_case, budget, ram_filter, ssd_filter, cpu_filter, brand_filter):
    filtered = laptops
    if use_case and use_case != '全部用途':
        filtered = [item for item in filtered if item.get('UseCase') == use_case]

    if budget:
        try:
            max_price = int(budget)
            filtered = [item for item in filtered if item.get('price', 0) <= max_price]
        except ValueError:
            pass

    if ram_filter:
        filtered = [item for item in filtered if item.get('RAM') == ram_filter]

    if ssd_filter:
        filtered = [item for item in filtered if item.get('SSD') == ssd_filter]

    if brand_filter:
        filtered = [item for item in filtered if item.get('brand') == brand_filter]

    if cpu_filter:
        filtered = [
            item for item in filtered
            if cpu_filter.lower() in item.get('CPU', '').lower()
        ]
    return filtered


@app.route('/')
def home():
    use_case = request.args.get('use_case', '').strip()
    budget = request.args.get('budget', '').strip()
    sort_by = request.args.get('sort', 'score_desc')
    ram_filter = request.args.get('ram', '').strip()
    ssd_filter = request.args.get('ssd', '').strip()
    cpu_filter = request.args.get('cpu', '').strip()
    brand_filter = request.args.get('brand', '').strip()

    laptops = load_laptops()

    filtered = filter_laptops(laptops,use_case,budget,ram_filter,ssd_filter,cpu_filter,brand_filter)

    if sort_by == 'score_desc':
        filtered = sorted(filtered,key=lambda x: x.get('Score', 0),reverse=True)

    elif sort_by == 'score_asc':
        filtered = sorted(filtered,key=lambda x: x.get('Score', 0))

    elif sort_by == 'price_asc':
        filtered = sorted(filtered,key=lambda x: x.get('price', 0))

    elif sort_by == 'price_desc':
        filtered = sorted(filtered,key=lambda x: x.get('price', 0),reverse=True
)

    return render_template(
        'index.html',
        laptops=filtered,
        selected_use_case=use_case,
        budget=budget,
        selected_sort=sort_by,
        selected_ram=ram_filter,
        selected_ssd=ssd_filter,
        selected_cpu=cpu_filter,
        selected_brand=brand_filter,
    )

@app.route('/about')
def about():
    """關於頁面"""
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """聯絡頁面"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # 這裡可以添加處理表單的邏輯
        return render_template('contact.html', success=True)
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)