from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello/')
def hello_page():
    context = {
        'name': request.args.get('name')
    }
    return render_template('hello.html', **context)


@app.route('/form/', methods=['GET', 'POST'])
def form_page():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        if name == "Andrey" and password == "123":
            print(name)
            return redirect(url_for('hello_page', name=name))
        return render_template('form.html', error=True)
    return render_template('form.html', error=None)


@app.route('/input/', methods=['GET', 'POST'])
def input_text():
    if request.method == 'POST':
        text = request.form.get('text')
        return redirect(url_for('get_result', number=str(len(text.split()))))
    return render_template('input.html')


@app.route('/calc/', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        num1 = request.form.get('num1')
        num2 = request.form.get('num2')
        operation = request.form.get('math')
        if operation == '+':
            return redirect(url_for('get_result', number=str(float(num1)+float(num2))))
        elif operation == '-':
            return redirect(url_for('get_result', number=str(float(num1)-float(num2))))
        elif operation == '*':
            return redirect(url_for('get_result', number=str(float(num1)*float(num2))))
        elif operation == '/':
            return redirect(url_for('get_result', number=str(float(num1)/float(num2))))
    return render_template('calc.html')


@app.route('/result/')
def get_result():
    return render_template('result.html', number=request.args.get('number'))


if __name__ == "__main__":
    app.run(debug=True)
