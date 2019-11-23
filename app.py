from flask import Flask, render_template, redirect, url_for, flash, Blueprint, g, request, session
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_wtf import FlaskForm
app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})
import models
import forms
import auth
from forms import WriteReview
from models import *
from auth import *
app.register_blueprint(auth.bp)


@app.route('/all')
def all_drinkers():
    drinkers = db.session.query(models.Drinker).all()
    return render_template('all-drinkers.html', drinkers=drinkers)

def country_choices():
    return db.session.query(models.Program.country).distinct().all()

@app.route('/review', methods=['GET', 'POST'])
def review():
    courses = db.session.query(models.Course).all()
    programs = db.session.query(models.Program).all()
    countries = db.session.query(models.Program.country).distinct().all()
    form = forms.WriteReview()
    form.program.choices = [(p.program_name, p.program_name) for p in programs]
    form.country.choices = [(country.country, country.country) for country in countries]
    form.courseCode.choices = [(c.duke_code, c.duke_code) for c in courses]
    form.course.choices = [(c.course_name, c.course_name) for c in courses]
    if form.validate_on_submit():
        # m = Review()
        id = 456 #set later
        country = form.country.data
        program_name = form.program.data
        duke_code = form.courseCode.data
        u_email = form.userEmail.data
        course_name = form.course.data
        rating = form.rating.data
        difficulty = form.difficulty.data
        content = form.thoughts.data
        new_review = models.Review(id = id, country = country, program_name = program_name, duke_code = duke_code, u_email = u_email, course_name = course_name, rating = rating, difficulty = difficulty, content = content)
        db.session.add(new_review)
        db.session.flush()
        db.session.commit()
        flash('New entry was successfully posted')
        return render_template('submitted.html', form=form)
    return render_template('review.html', form=form)

    # try:
    #         form.errors.pop('database', None)
    #         models.Drinker.edit(name, form.name.data, form.address.data,
    #                             form.get_beers_liked(), form.get_bars_frequented())
    #         return redirect(url_for('drinker', name=form.name.data))
    #     except BaseException as e:
    #         form.errors['database'] = str(e)
    #         return render_template('edit-drinker.html', drinker=drinker, form=form)
    # else:
    #     return render_template('edit-drinker.html', drinker=drinker, form=form)

# @app.route('/confused', methods=['GET', 'POST'])
# def confused():
#     form = WriteReview()
#     if form.validate_on_submit():
#         # review = Review()
#         # form.populate_obj(review)
#         # db.session.add(review)
#         # db.session.commit()
#         # location = form.location.data
#         # program = form.program.data
#         # course = form.course.data
#         # rating = form.rating.data
#         # difficulty = form.difficulty.data
#         # thoughts = form.thoughts.data
#         # print(location)
#         # print(program)
#         # print(course)
#         # print(rating)
#         # print(difficulty)
#         # print(thoughts)
#         flash('Login requested for user {}, remember_me={}'.format(
#             form.username.data, form.remember_me.data))
#         return redirect('/index')
#         # print("\nData received. Now redirecting ...")
#         # return redirect(url_for('confused'))
#     return render_template('trying-shit-out.html', form=form)

# ----------- EXAMPLE -------------
@app.route('/login-example', methods=["GET", "POST"])
def login_example():
    form = forms.EmailPasswordForm()
    if form.validate_on_submit():
        # return "email: {}, password: {}".format(form.email.data, form.password.data)
        return render_template('submitted.html',
            email=form.email.data, password=form.password.data)
    return render_template('login-example.html', form=form)

# ---------------------------------

@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')

@app.route('/write-review', methods=['GET'])
def write_review():
    courses = db.session.query(models.Course).all()
    programs = db.session.query(models.Program).all()
    countries = db.session.query(models.Program.country).distinct().all()
    return render_template('write-review.html', courses=courses, programs=programs, countries=countries)


@app.route('/submitted')
def submit_review():
    return render_template('submitted.html')


@app.route('/filter', methods=['GET', 'POST'])
def filter_reviews():
    programs = db.session.query(models.Program).all()
    countries = db.session.query(models.Country).all()
    form = forms.FilterCourseForm()

    program_choices = [(p.program_name, p.program_name) for p in programs]
    program_choices.insert(0,("NA", "--"))
    form.program.choices = program_choices

    country_choices = [(c.id, c.country_name) for c in countries]
    country_choices.insert(0,(("NA","--")))
    form.country.choices = country_choices

    if form.is_submitted():
        if not form.validate():
            for fieldName, errorMessages in form.errors.items():
                print("field: {}, errormsg: {}".format(fieldName," ".join(errorMessages)))
                return form.program.data

    if form.validate_on_submit():
        return redirect(url_for('explore_courses', program=form.program.data))
    return render_template('filter.html', form=form)

@app.route('/filter/<program>')
def filter_country(program):
    countries = db.session.query(models.Country).filter(models.Program.program_name == program).all()
    return countries

@app.route('/explore-courses/<program>', methods=['GET'])
def explore_courses(program):
    if (program != "NA") :
        courses = db.session.query(models.Course) \
            .filter(models.Course.program_name == program)
    else :
        courses = db.session.query(models.Course)
    programs = db.session.query(models.Program).all()
    return render_template('explore-courses.html', courses=courses, programs=programs)


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
