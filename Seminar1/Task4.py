from flask import Flask

app = Flask(__name__)


@app.route('/')
def greet():
    return 'Hello, world!'


@app.route('/about/')
def about():
    return 'This is about page'


@app.route('/contact/')
def contact():
    return 'This is contact page'


@app.route('/sum/<int:num1>-<int:num2>/')
def sum_num(num1, num2):
    return f'Сумма чисел {num1} и {num2} равно {num1 + num2}'


@app.route('/textlen/<text>/')
def text(txt):
    return f'Длина строки составляет {len(txt)}'


if __name__ == "__main__":
    app.run()
