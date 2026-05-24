from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
DATA_PATH = os.path.join(os.path.dirname(__file__), 'laptop.csv')


def load_laptops():
    laptops = []
    if not os.path.exists(DATA_PATH):
        return laptops

    with open(DATA_PATH, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['Price'] = int(row.get('Price', '0') or '0')
            laptops.append(row)
    return laptops


def filter_laptops(laptops, use_case, budget):
    filtered = laptops
    if use_case:
        filtered = [item for item in filtered if item.get('UseCase') == use_case]
    if budget:
        try:
            max_price = int(budget)
            filtered = [item for item in filtered if item.get('Price', 0) <= max_price]
        except ValueError:
            pass
    return filtered


@app.route('/')
def home():
    use_case = request.args.get('use_case', '').strip()
    budget = request.args.get('budget', '').strip()

    laptops = load_laptops()
    filtered = filter_laptops(laptops, use_case, budget)

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