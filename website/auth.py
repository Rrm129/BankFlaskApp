from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import func
import random

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Log in Successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect Credentials", category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up',  methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':

        email = request.form.get('email')
        full_name = request.form.get('fullname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email is to short', category='error')
            pass
        elif len(full_name) < 2:
            flash('Name is too short', category='error')
            pass
        elif password1 != password2:
            flash('Password does not match', category='error')
            pass
        elif len(password1) < 1:
            flash('Password is to short', category='error')
            pass
        else:
            
            accountNum = db.session.query(func.max(User.account_number)).first()
            if accountNum != None:
                accNum = accountNum[0] if accountNum[0] is not None else 10000
            else:
                accNum = 10000
            accNum = accNum + random.randint(1,37)
            
            new_user = User(email=email, full_name=full_name,\
                 password=generate_password_hash(password1, method='sha256'),\
                      account_number=accNum)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
