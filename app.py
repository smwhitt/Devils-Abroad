from flask import Flask, render_template, redirect, url_for, flash, Blueprint, g, session
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, make_response
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
from datetime import datetime



@app.route('/all')
def all_drinkers():
    drinkers = db.session.query(models.Drinker).all()
    return render_template('all-drinkers.html', drinkers=drinkers)

def country_choices():
    return db.session.query(models.Program.country).distinct().all()
   

@app.route('/review', methods=['GET', 'POST'])
@login_required
def review():

    majorCodes = db.session.query(models.MajorCodes).all()
    programs = db.session.query(models.Program).all()
    allUsers = db.session.query(models.Users).all()
    # countries = db.session.query(models.Program.country).distinct().all()
    form = forms.WriteReview()
    # form.program.choices = [(p.program_name, p.program_name) for p in programs]
    # form.country.choices = [(country.country, country.country) for country in countries]
    form.majorCode.choices = [(m.duke_major_code, m.duke_major_code) for m in majorCodes]
    # form.course.choices = [(course.course_name, course.course_name) for course in courses] + [("Other", "Other")]
    # form.courseCode.choices = [(c.duke_code, c.duke_code) for c in courses]
        
    if form.validate_on_submit():
        
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        id = timestampStr
        # country = form.country.data
        # db.session.query(models.Users).filter(models.Users.username.like(uname)).first()
        u_email = session.get('user_email')

        program_name_full = db.session.query(models.Users).filter(Users.email == u_email).all()
        program_name = program_name_full[0].program_name

        # for p in allUsers:
        #     if p.email == u_email:
        #         program_name = p.program_name
        for p in programs:
            if p.program_name == program_name:
                country = p.country 
        duke_major_code = form.majorCode.data
        # duke_code = form.courseCode.data
        duke_code = str(duke_major_code) + " " + str(form.courseNumber.data)
        # u_email = form.userEmail.data
        course_name = form.course.data

        error = None
        if request.method == 'POST':
            specifcUserReviews = db.session.query(models.Review).filter(Review.u_email == u_email).filter(Review.course_name == course_name).all()
            if len(specifcUserReviews) != 0:
                error = 'You have already written a review for this class.'
                flash(error)
                return redirect(url_for('review'))
        rating = form.rating.data
        difficulty = form.difficulty.data
        content = form.thoughts.data
        new_review = models.Review(id=id, country=country, program_name=program_name, duke_major_code=duke_major_code, duke_code=duke_code, u_email=u_email, course_name=course_name, rating=rating, difficulty=difficulty, content=content)
        new_course = models.Course(duke_code=duke_code, course_name=course_name, program_name=program_name)
        db.session.add(new_review)
        db.session.add(new_course)
        db.session.flush()
        db.session.commit()
        flash('New entry was successfully posted')
        return render_template('submitted.html', form=form)
    return render_template('review.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')

@app.route('/write-review', methods=['GET'])
@login_required
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
    countries = db.session.query(models.Country).all()
    programs = db.session.query(models.Program).all()
    majorCodes = db.session.query(models.MajorCodes).distinct().all()
    form = forms.FilterCourseForm()

    country_choices = [(c.country_name, c.country_name) for c in countries]
    country_choices.insert(0,(("NA","--")))
    form.country.choices = country_choices

    program_choices = [(p.program_name, p.program_name) for p in programs]
    program_choices.insert(0,("NA", "--"))
    form.program.choices = program_choices

    majorCodeChoices = [(m.duke_major_code, m.duke_major_code) for m in majorCodes]
    majorCodeChoices.insert(0, ("NA", "--"))
    form.majorCode.choices = majorCodeChoices

    if form.is_submitted():
        if not form.validate():
            for fieldName, errorMessages in form.errors.items():
                print("field: {}, errormsg: {}".format(fieldName," ".join(errorMessages)))
                return form.program.data
    
    error = None
    if request.method == 'POST':
        if form.program.data == "NA":
            error = 'Please select a program'
            flash(error)
            return redirect(url_for('filter_reviews'))

    if form.validate_on_submit():
        return redirect(url_for('explore_courses', majorChoice = form.majorCode.data, country = form.country.data, program=form.program.data, major = form.majorCode.data))
    return render_template('filter.html', form=form)
   
@app.route('/filter/<country>')
def filter_country(country):
    programs = db.session.query(models.Program).filter(models.Program.country == country)
    programArray = []
    for program in programs:
        programArray.append(program.program_name)
    
    return jsonify({'programs': programArray})

@app.route('/explore-courses/<program>/<majorChoice>', methods=['GET'])
def explore_courses(program, majorChoice):
    courses = db.session.query(models.Course)\
            .filter(Course.program_name == program)
    
    if majorChoice != "NA":
        coursesFixed = []
        for course in courses:
            if course.duke_code.split(" ")[0] == majorChoice:
                coursesFixed.append(course)  
        courses = coursesFixed
    return render_template('explore-courses.html', courses=courses)


@app.route('/course-review/<course_uuid>')
def course_review(course_uuid):
    course = db.session.query(models.Course)\
        .filter(models.Course.uuid == course_uuid).one()
    reviews = db.session.query(models.Review)\
        .filter(models.Review.course_uuid == course_uuid)
    return render_template('course-review.html', course=course, reviews=reviews)
# fix filtering - use keys (multiple variables)

@app.route('/contacts')
def contacts():
    contact_list = db.session.query(models.Contact).all()
    return render_template('contacts.html', contact_list=contact_list)

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
