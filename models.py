from sqlalchemy import sql, orm
from sqlalchemy_utils import aggregated
from sqlalchemy.dialects.postgresql import UUID
from app import db
import datetime


class Users(db.Model):
    __bind_key__ = 'devils_abroad'
    __tablename__ = 'users'
    email = db.Column('email', db.String(100), primary_key=True)
    name = db.Column('name', db.String(100))
    major = db.Column('major', db.String(50))
    term = db.Column('term', db.String(50))
    program_name = db.Column('program_name', db.String(50))
    username = db.Column('username', db.String())
    password = db.Column('password', db.String())

    # method to check if the user is authenticated
    #def is_authenticated(self):


    # user = orm.relationship('User')

class Contact(db.Model):
    __bind_key__ = 'devils_abroad'
    __tablename__ = 'contact'
    email = db.Column('email', db.String(100), primary_key=True)
    name = db.Column('name', db.String(100))
    major = db.Column('major', db.String(50))
    term = db.Column('term', db.String(50))
    program_name = db.Column('program_name', db.String(50))

class Program(db.Model):
    __bind_key__ = 'devils_abroad'
    __tablename__ = 'program'
    program_name = db.Column('program_name', db.String(100), primary_key=True)
    country = db.Column('country', db.String(100))
    course = orm.relationship('Course')


class Course(db.Model):
    __bind_key__ = 'devils_abroad'
    __tablename__ = 'course'
    uuid = db.Column('uuid', UUID(as_uuid=True), unique=True, nullable=False, primary_key=True)
    duke_code = db.Column('duke_code', db.String(100))
    course_name = db.Column('course_name', db.String(100))
    program_name = db.Column('program_name', db.String(100),
                             db.ForeignKey(Program.program_name))
    # @aggregated('reviews', db.Column(db.Integer))
    # def avg_rating(self):
    #     return db.func.avg(Review.rating)
    
    # reviews = db.orm.relationship(
    #     'Review'
    #     # backref='course'
    # )

class Review(db.Model):
    __bind_key__ = 'devils_abroad'
    __tablename__ = 'review'
    id = db.Column('id', db.String, primary_key = True)
    country = db.Column('country', db.String)
    course_uuid = db.Column('course_uuid', UUID(as_uuid=True))
    # program_name = db.Column('program_name', db.String)
    duke_major_code = db.Column('duke_major_code', db.String)
    # duke_code = db.Column('duke_code', db.String)
    # course_name = db.Column('course_name', db.String)
    u_email = db.Column('u_email', db.String)
    content = db.Column('content', db.String)
    rating = db.Column('rating', db.Integer)
    difficulty = db.Column('difficulty', db.Integer)



class MajorCodes(db.Model):
    __bind_key__ = 'devils_abroad'
    __tablename__ = 'majorcodes'
    duke_major_code = db.Column('duke_major_code', db.String(20), primary_key = True)

# class Likes(db.Model):
#     __bind_key__ = 'devils_abroad'
#     __tablename__ = 'likes'
#     u_email = db.Column('u_email', db.String(100), db.ForeignKey(User.email), primary_key=True)


class Country(db.Model):
    __bind_key__ = 'devils_abroad'
    __tablename__ = 'country'
    country_name = db.Column('country_name', db.String(50), primary_key=True)
    c_id = db.Column('c_id',db.String(3))

class Drinker(db.Model):
    __tablename__ = 'drinker'
    name = db.Column('name', db.String(20), primary_key=True)
    address = db.Column('address', db.String(20))
    likes = orm.relationship('Likes')
    frequents = orm.relationship('Frequents')

    @staticmethod
    def edit(old_name, name, address, beers_liked, bars_frequented):
        try:
            db.session.execute('DELETE FROM likes WHERE drinker = :name',
                               dict(name=old_name))
            db.session.execute('DELETE FROM frequents WHERE drinker = :name',
                               dict(name=old_name))
            db.session.execute('UPDATE drinker SET name = :name, address = :address'
                               ' WHERE name = :old_name',
                               dict(old_name=old_name, name=name, address=address))
            for beer in beers_liked:
                db.session.execute('INSERT INTO likes VALUES(:drinker, :beer)',
                                   dict(drinker=name, beer=beer))
            for bar, times_a_week in bars_frequented:
                db.session.execute('INSERT INTO frequents'
                                   ' VALUES(:drinker, :bar, :times_a_week)',
                                   dict(drinker=name, bar=bar,
                                        times_a_week=times_a_week))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Beer(db.Model):
    __tablename__ = 'beer'
    name = db.Column('name', db.String(20), primary_key=True)
    brewer = db.Column('brewer', db.String(20))


class Bar(db.Model):
    __tablename__ = 'bar'
    name = db.Column('name', db.String(20), primary_key=True)
    address = db.Column('address', db.String(20))
    serves = orm.relationship('Serves')


class Likes(db.Model):
    __tablename__ = 'likes'
    drinker = db.Column('drinker', db.String(20),
                        db.ForeignKey('drinker.name'),
                        primary_key=True)
    beer = db.Column('beer', db.String(20),
                     db.ForeignKey('beer.name'),
                     primary_key=True)


class Serves(db.Model):
    __tablename__ = 'serves'
    bar = db.Column('bar', db.String(20),
                    db.ForeignKey('bar.name'),
                    primary_key=True)
    beer = db.Column('beer', db.String(20),
                     db.ForeignKey('beer.name'),
                     primary_key=True)
    price = db.Column('price', db.Float())


class Frequents(db.Model):
    __tablename__ = 'frequents'
    drinker = db.Column('drinker', db.String(20),
                        db.ForeignKey('drinker.name'),
                        primary_key=True)
    bar = db.Column('bar', db.String(20),
                    db.ForeignKey('bar.name'),
                    primary_key=True)
    times_a_week = db.Column('times_a_week', db.Integer())
