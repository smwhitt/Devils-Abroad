import functools
import models
from models import *
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app import db
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
bp = Blueprint('auth', __name__, url_prefix='/auth')
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        major = request.form['major']
        grad_year = request.form['grad_year']
        uname = request.form['username']
        pwd = request.form['password']
        error = None

        if not uname:
            error = 'Username is required.'
        elif not pwd:
            error = 'Password is required.'
        elif db.session.query(models.Users).filter(models.Users.username.like(uname)).first() is not None:
            error = 'User {} is already registered.'.format(uname)

        if error is None:
            hashed_pwd = generate_password_hash(pwd)
            new_account = models.Users(email=email, name=name, major=major, grad_year=grad_year, username=uname, password=hashed_pwd)
            db.session.add(new_account)
            db.session.flush()
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        uname = request.form['username']
        password = request.form['password']
        error = None
        user = db.session.query(models.Users).filter(models.Users.username.like(uname)).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
           error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_email'] = user.email
            return redirect(url_for('home_page'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_email = session.get('user_email')

    if user_email is None:
        g.user = None
    else:
        g.user = db.session.query(models.Users).filter(models.Users.email.like(user_email)).first()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_page'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view