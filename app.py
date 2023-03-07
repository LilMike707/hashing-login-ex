from flask import Flask, render_template, redirect, session
from models import connect_db, db, User
from forms import RegForm, LoginForm


app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///login_ex"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "mike123"


connect_db(app)


@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def show_register():
    form = RegForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()

        return redirect('/secret')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def show_login():


@app.route('/secret')
def show_secret():
