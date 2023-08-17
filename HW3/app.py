from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from forms import LoginForm
from models import db, User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registration.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    emails = [user.email for user in User.query.all()]
    context = {'emails': emails}
    if request.method == 'POST' and form.validate():
        name = form.name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        user = User(name=name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
    return render_template('login.html', form=form, **context)
