import functools
import models
from models import *
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import aliased
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    programs = db.session.query(models.Program).all()
    programChoices = sorted([(p.program_name, p.program_name) for p in programs])
    programChoices.insert(0, ("--", "--"))
    majorCodes = db.session.query(models.MajorCodes).distinct().all()
    majorCodeChoices = sorted([(m.duke_major_code, m.duke_major_code) for m in majorCodes])
    majorCodeChoices.insert(0, ("--", "--"))
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        major = request.form['major']
        term = request.form['term']
        program_name = request.form['program_name']
        uname = request.form['username']
        pwd = request.form['password']
        confpwd = request.form['confirmpassword']
        error = None

        if email[-9:] != "@duke.edu":
            error = 'You must enter a valid Duke email'
        elif major == "--":
            error = 'You must choose a major.'
        elif program_name == "--":
            error = 'You must choose a program.'
        elif not uname:
            error = 'Username is required.'
        elif not pwd:
            error = 'Password is required.'
        elif not confpwd:
            error = 'Confirm your password'
        elif db.session.query(models.Users).filter(models.Users.username.contains(uname, autoescape=True)).first() \
                is not None:
            error = 'User {} is already registered.'.format(uname)
        elif pwd != confpwd:
            error = 'Passwords do not match'
        
        if error is None:
            hashed_pwd = generate_password_hash(pwd)
            new_account = models.Users(email=email, name=name, major=major, term=term, program_name=program_name, username=uname, password=hashed_pwd)
            db.session.add(new_account)
            db.session.flush()
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash(error)

    return render_template('auth/register.html', majors = majorCodeChoices, programs = programChoices)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        uname = request.form['username']
        password = request.form['password']
        error = None
        user = db.session.query(models.Users).filter(models.Users.username.contains(uname, autoescape=True)).first()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password) and (user.password != password):
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
        g.user = db.session.query(models.Users).filter(models.Users.email.contains(user_email, autoescape=True)).first()
        db.session.close()


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


@bp.route('/my_account')
def my_account():
    user_email = session.get('user_email')
    my_reviews = db.session.query(models.Review).filter(models.Review.u_email == user_email)\
        .join(models.Course, models.Course.id == models.Review.course_id).all()
    my_classes = db.session.query(models.Course).join(models.Review, models.Course.id == models.Review.course_id)\
        .filter(models.Review.u_email == user_email)
    db.session.close()
    return render_template('auth/my_account.html', my_reviews=my_reviews, my_classes=my_classes)


@bp.route('/delete_review/<review_id>', methods=('POST',))
def delete_review(review_id):
    review = db.session.query(models.Review).filter(models.Review.id.like(review_id)).one()
    db.session.delete(review)
    db.session.commit()
    return render_template('auth/my_account.html')
