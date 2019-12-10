from flask import Flask, render_template, redirect, url_for, flash, Blueprint, g, session
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, make_response
from statistics import mean 
from flask_wtf import FlaskForm
from sqlalchemy import func
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

@app.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    majorCodes = db.session.query(models.MajorCodes).all()
    programs = db.session.query(models.Program).all()
    allUsers = db.session.query(models.Users).all()
    db.session.close()
    form = forms.WriteReview()

    # setting up the form
    form.majorCode.choices = sorted([(m.duke_major_code, m.duke_major_code) for m in majorCodes])
    
    if form.validate_on_submit():
        
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        id = timestampStr
        u_email = session.get('user_email')

        # get form responses 
        duke_major_code = form.majorCode.data
        duke_code = str(duke_major_code) + " " + str(form.courseNumber.data)
        course_name = form.course.data
        rating = form.rating.data
        difficulty = form.difficulty.data
        content = form.thoughts.data

        user = db.session.query(models.Users).filter(Users.email == u_email).one()
        program_name = user.program_name

        for p in programs:
            if p.program_name == program_name:
                country = p.country
                break

        # check for errors
        if request.method == 'POST':
            error = None
            user = db.session.query(models.Users).filter(Users.email == u_email).first()
            specifcUserReviews = db.session.query(models.Review).filter(Review.u_email == u_email)\
                .join(models.Course, Course.id == Review.course_id).filter(Course.course_name == course_name).all()
            if len(specifcUserReviews) != 0:
                error = 'You have already written a review for this class.'
                flash(error)
                return redirect(url_for('review'))

        # check if the course already exists
        courses = db.session.query(models.Course).filter(Course.course_name == course_name)\
            .filter(Course.program_name == program_name).filter(Course.duke_code == duke_code).all()

        course_id = None
        for course in courses:
            if course.course_name == course_name and course.program_name == program_name and course.duke_code == duke_code:
                course_id = course.id
                break

        if course_id == None:
            new_course = models.Course(duke_code=duke_code, course_name=course_name, program_name=program_name)
            db.session.add(new_course)
            db.session.flush()
            db.session.commit()
            course_id = new_course.id

        new_review = models.Review(id=id, country=country, duke_major_code=duke_major_code, u_email=u_email, course_id=course_id , rating=rating, difficulty=difficulty, content=content)
        db.session.add(new_review)
        db.session.flush()
        db.session.commit()
        flash('New entry was successfully posted')
        return render_template('submitted.html', form=form)
    return render_template('review.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')

@app.route('/submitted')
def submit_review():
    return render_template('submitted.html')

@app.route('/filter', methods=['GET', 'POST'])
def filter_reviews():
    countries = db.session.query(models.Country).all()
    programs = db.session.query(models.Program).all()
    majorCodes = db.session.query(models.MajorCodes).distinct().all()
    db.session.close()
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
        return redirect(url_for('explore_courses', majorChoice = form.majorCode.data, program=form.program.data))
    return render_template('filter.html', form=form)
   
@app.route('/filter/<country>')
def filter_country(country):
    programs = db.session.query(models.Program).filter(models.Program.country == country)
    db.session.close()
    programArray = []
    for program in programs:
        programArray.append(program.program_name)
    
    return jsonify({'programs': programArray})

@app.route('/explore-courses/<program>/<majorChoice>', methods=['GET'])
def explore_courses(program, majorChoice):
    courses = db.session.query(models.Course)\
            .filter(Course.program_name == program)
    db.session.close()
    
    if majorChoice != "NA":
        coursesFixed = []
        for course in courses:
            if course.duke_code.split(" ")[0] == majorChoice:
                coursesFixed.append(course)  
        courses = coursesFixed

    course_with_ratings = []
    for course in courses:
        reviews = db.session.query(models.Review)\
            .filter(models.Review.course_id == course.id)
        ratings = []
        for review in reviews:
            ratings.append(review.rating)
        num_reviews = len(ratings)
        if num_reviews <= 0:
            avg_rating = 0
        else: 
            avg_rating = mean(ratings)
        course_with_rating = (course, avg_rating, num_reviews)
        course_with_ratings.append(course_with_rating)
    return render_template('explore-courses.html', courses=course_with_ratings)

@app.route('/course-review/<course_id>')
def course_review(course_id):
    course = db.session.query(models.Course)\
        .filter(models.Course.id == course_id).one()
    reviews = db.session.query(models.Review)\
        .filter(models.Review.course_id == course_id)
    db.session.close()
    return render_template('course-review.html', course=course, reviews=reviews)

@app.route('/contacts')
def contacts():
    contact_list = db.session.query(models.Contact).all()
    return render_template('contacts.html', contact_list=contact_list)

@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
