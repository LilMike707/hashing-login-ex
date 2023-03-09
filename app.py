from flask import Flask, render_template, redirect, session
from models import connect_db, db, User, Feedback
from forms import RegForm, LoginForm, DeleteForm


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

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit(user)
        session['username'] = user.username

        return redirect(f'/users/{user.username}')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def show_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username=username, password=password)

        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid Username/Password']
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')


@app.route('/users/<username>')
def show_user(username):

    if 'username' not in session or username != session['username']:
        return redirect('/login')

    user = User.query.get(username)
    form = DeleteForm()

    return render_template('show_user.html', user=user, form=form)


@app.route('/users/<username>/delete', methods=['POST'])
def remove_user(username):
    if "username" not in session or username != session['username']:
        return redirect('/login')

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")


