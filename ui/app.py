from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@app.route('/')
def home():
    """首頁"""
    return render_template('index.html')

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