from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import models
import forms
from forms import WriteReview


app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})

@app.route('/confused', methods=['GET', 'POST'])
def confused():
    form = WriteReview()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('submitted.html')



@app.route('/')
def login():
    return render_template('login.html')

@app.route('/homepage', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')


@app.route('/filter')
def filter_reviews():
    courses = db.session.query(models.Course).all()
    return render_template('filter.html')
    # note, temporary render explore. change to render filter.html


@app.route('/write-review', methods=['GET'])
def write_review():
    courses = db.session.query(models.Course).all()
    programs = db.session.query(models.Program).all()
    countries = db.session.query(models.Program.country).distinct().all()
    return render_template('write-review.html', courses=courses, programs=programs, countries=countries)


@app.route('/submitted')
def submit_review():
    return render_template('submitted.html')


@app.route('/explore', methods=['GET'])
def explore_courses():
    courses = db.session.query(models.Course).all()
    programs = db.session.query(models.Program).all()
    return render_template('explore.html', courses=courses, programs=programs)


@app.route('/drinker/<name>')
def drinker(name):
    drinker = db.session.query(models.Drinker) \
        .filter(models.Drinker.name == name).one()
    return render_template('drinker.html', drinker=drinker)


@app.route('/edit-drinker/<name>', methods=['GET', 'POST'])
def edit_drinker(name):
    drinker = db.session.query(models.Drinker).filter(models.Drinker.name == name).one()
    beers = db.session.query(models.Beer).all()
    bars = db.session.query(models.Bar).all()
    form = forms.DrinkerEditFormFactory.form(drinker, beers, bars)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.Drinker.edit(name, form.name.data, form.address.data,
                                form.get_beers_liked(), form.get_bars_frequented())
            return redirect(url_for('drinker', name=form.name.data))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('edit-drinker.html', drinker=drinker, form=form)
    else:
        return render_template('edit-drinker.html', drinker=drinker, form=form)


@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
