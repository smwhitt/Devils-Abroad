# SQLALCHEMY_DATABASE_URI = 'postgresql://qiaoa98@localhost/devils_abroad'

#SQLALCHEMY_DATABASE_URI = 'postgresql://davidchen1337:1234@localhost/beers'

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:ihatethisclass@localhost/devils_abroad'
SQLALCHEMY_BINDS = {
    'devils_abroad': 'postgresql://postgres:ihatethisclass@localhost/devils_abroad'

}

#SQLALCHEMY_BINDS = {
 #   'devils_abroad': 'postgresql://davidchen1337:1234@localhost/devils_abroad'

#}

SQLALCHEMY_ECHO = True
DEBUG = True
