import os
from laptop import app

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laptops.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


