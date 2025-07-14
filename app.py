from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Trả về file HTML

@app.route('/hello/<name>')
def hello(name):
    return f"Hello, {name}!"

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    return redirect(url_for('hello', name=name))

if __name__ == '__main__':
    app.run(debug=True)
