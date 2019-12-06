SQLALCHEMY_DATABASE_URI = 'postgresql://vagrant:dbpasswd@localhost/beers'

SQLALCHEMY_BINDS = {
    'devils_abroad': 'postgresql://vagrant:dbpasswd@localhost/devils_abroad'
}

SQLALCHEMY_ECHO = True
DEBUG = True
