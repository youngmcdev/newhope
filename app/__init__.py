import sys
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/newhope_logger.log', maxBytes=5242880,
                                       backupCount=30)
    file_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s [in %(module)s %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    # Test logging
    # app.logger.info('New Hope startup')
    # msg = "Server:" + app.config['MAIL_SERVER'] + ", Port:" + str(app.config['MAIL_PORT']) + ", User:" + app.config['MAIL_USERNAME'] + ", Sender:" + app.config['MAIL_SENDER']
    # app.logger.info(msg)

    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr=app.config['MAIL_SENDER'],
            toaddrs=app.config['ADMINS'], subject='New Hope Logger',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

from app import routes, models, errors