from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        response = make_response(redirect(url_for('greet_page')))
        response.set_cookie('name', name)
        response.set_cookie('email', email)
        return response
    return render_template('login.html')


@app.route('/greet/', methods=['POST', 'GET'])
def greet_page():
    if request.method == 'POST' and request.form.get('quit'):
        response = make_response(redirect(url_for('login_page')))
        response.set_cookie('name', max_age=0)
        response.set_cookie('email', max_age=0)
        return response

    context = {
        'name': request.cookies.get('name')
    }
    return render_template('greet.html', **context)


if __name__ == "__main__":
    app.run(debug=True)
