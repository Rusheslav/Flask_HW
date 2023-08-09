from flask import Flask, render_template

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


@app.route('/textlen/<txt>/')
def text(txt):
    return f'Длина строки составляет {len(txt)}'


@app.route('/firsthtml/')
def print_html():
    return '<h1>Моя первая HTML страница</h1><p>Привет, мир!</p>'


@app.route('/sheet/')
def get_sheet():
    sheet = [
        {'first_name': 'Andrey', 'last_name': 'Ivanov', 'age': 20, 'avg_grade': 4.5},
        {'first_name': 'Sergey', 'last_name': 'Petrov', 'age': 21, 'avg_grade': 4.8},
        {'first_name': 'Saveliy', 'last_name': 'Sidorov', 'age': 22, 'avg_grade': 5.0}
    ]
    # sheet_header = sheet[0].keys()
    # sheet_content = [list(i.values()) for i in sheet]
    return render_template('sheet.html', sheet=sheet)


if __name__ == "__main__":
    app.run()
