from flask_app import app, bcrypt
from flask import render_template, request, redirect, session, flash

from flask_app.models.user_model import User


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["POST"])
def login():

    logged_in_user = User.validate_login(request.form)

    if not logged_in_user:
        return redirect("/")

    session['uid'] = logged_in_user.id

    return redirect('/dashboard')


@app.route('/new_user', methods=['POST'])
def new_user():

    # print(request.form)

    hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "password": hash
    }
    User.register(data)
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')


@app.route("/dashboard")
def dashboard():

    if not 'uid' in session:
        flash("access denied")
        return redirect("/")

    return render_template('dashboard.html')
