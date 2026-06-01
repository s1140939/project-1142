from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
DATA_PATH = os.path.join(os.path.dirname(__file__), 'laptop.csv')

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




def load_laptops():
    laptops = []
    if not os.path.exists(DATA_PATH):
        return laptops

    with open(DATA_PATH, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['price'] = int(row.get('price', '0') or '0')
            row['UseCase'] = classify_use_case(row)
            laptops.append(row)
    return laptops


def filter_laptops(laptops, use_case, budget):
    filtered = laptops
    if use_case and use_case != '全部用途':
        filtered = [item for item in filtered if item.get('UseCase') == use_case]
    if budget:
        try:
            max_price = int(budget)
            filtered = [item for item in filtered if item.get('price', 0) <= max_price]
        except ValueError:
            pass
    return filtered


@app.route('/')
def home():
    use_case = request.args.get('use_case', '').strip()
    budget = request.args.get('budget', '').strip()

    laptops = load_laptops()

    filtered = filter_laptops(laptops, use_case, budget)

    filtered = sorted(filtered, key=lambda x: x.get('price', 0))

    return render_template(
        'index.html',
        laptops=filtered,
        selected_use_case=use_case,
        budget=budget,
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