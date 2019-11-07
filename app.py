from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import models
import forms

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})

# @app.route('/')
# def all_drinkers():
#     drinkers = db.session.query(models.Drinker).all()
#     return render_template('all-drinkers.html', drinkers=drinkers)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/filter')
def filter_reviews():
    courses = db.session.query(models.Course).all()
    return render_template('filter.html')
    # note, temporary render explore. change to render filter.html

@app.route('/write-review')
def write_review():
    return render_template('write-review.html')

@app.route('/explore', methods=['GET'])
def explore_courses():
    courses = db.session.query(models.Course).all()
    programs = db.session.query(models.Program).all()
    return render_template('explore.html', courses=courses, programs=programs)

@app.route('/course-review/<course_name>')
def course_review(course_name):
    course = db.session.query(models.Course)\
        .filter(models.Course.course_name == course_name).one()
    reviews = db.session.query(models.Review)\
        .filter(models.Review.course_name == course_name)
    return render_template('course-review.html', course=course, reviews=reviews)
# fix filtering - use keys (multiple variables)

@app.route('/drinker/<name>')
def drinker(name):
    drinker = db.session.query(models.Drinker)\
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
