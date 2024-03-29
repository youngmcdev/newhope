import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or ''
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or ''
    MAIL_SENDER = os.environ.get('MAIL_SENDER', 'no_reply@nhbcallegan.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ''
    DATA_SECRET = os.environ.get('DATA_SECRET') or 'beriberi'
    ADMINS = ['galt_69@hotmail.com']
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False