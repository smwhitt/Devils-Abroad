from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField





class EmailPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# class WriteReviewFormFactory:
#     @staticmethod
#     def form():

class FilterCourseForm(FlaskForm):
    # example of static choices for SelectField
    # language = SelectField(
    #     'Programming Language',
    #     choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')],
    #     default='default string'
    # )
    # example of dynamic choices for SelectField - choices list needs to be assigned in app.py
    program = SelectField(label='Program', default="Choose a program")
    country = SelectField(label='Country', default="Choose a country")

    # note sure why the default string isn't working its so annoying aldfkjakjdfh
    # might be better to change to SelectMultipleField so user can select more than one choice

class WriteReview(FlaskForm):
    
    country = SelectField('country', choices = [], coerce = str, validators=[DataRequired()])
    userEmail = StringField('User Email',  validators=[DataRequired()])
    program = SelectField('program', choices = [], coerce = str, validators=[DataRequired()])
    courseCode = SelectField('Duke Code', choices = [], coerce = str, validators=[DataRequired()])
    course = SelectField('course', choices = [], coerce = str, validators=[DataRequired()])
    other = StringField('enter the name of your ourse if it does not appear above',  validators=[DataRequired()])
    rating = SelectField('rating', choices = [(1,1), (2,2), (3,3), (4,4), (5,5)], coerce = int, validators=[DataRequired()])
    difficulty = SelectField('difficulty', choices = [(1,1), (2,2), (3,3), (4,4), (5,5)], coerce = int,  validators=[DataRequired()])
    thoughts = StringField('thoughts', validators=[DataRequired()])
    

class DrinkerEditFormFactory:
    @staticmethod
    def form(drinker, beers, bars):
        class F(FlaskForm):
            name = StringField(default=drinker.name)
            address = StringField(default=drinker.address)
            @staticmethod
            def beer_field_name(index):
                return 'beer_{}'.format(index)
            def beer_fields(self):
                for i, beer in enumerate(beers):
                    yield beer.name, getattr(self, F.beer_field_name(i))
            def get_beers_liked(self):
                for beer, field in self.beer_fields():
                    if field.data:
                        yield beer
            @staticmethod
            def bar_field_name(index):
                return 'bar_{}'.format(index)
            def bar_fields(self):
                for i, bar in enumerate(bars):
                    yield bar.name, getattr(self, F.bar_field_name(i))
            def get_bars_frequented(self):
                for bar, field in self.bar_fields():
                    if field.data != 0:
                        yield bar, field.data
        beers_liked = [like.beer for like in drinker.likes]
        for i, beer in enumerate(beers):
            field_name = F.beer_field_name(i)
            default = 'checked' if beer.name in beers_liked else None
            setattr(F, field_name, BooleanField(default=default))
        bars_frequented = {frequent.bar: frequent.times_a_week\
                           for frequent in drinker.frequents}
        for i, bar in enumerate(bars):
            field_name = F.bar_field_name(i)
            default = bars_frequented[bar.name] if bar.name in bars_frequented else 0
            setattr(F, field_name, IntegerField(default=default))
        return F()


