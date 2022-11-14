import os
import datetime
from ..extension.db import db

base_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig():
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", 'sqlite:///flaskr.sqlite')
    SESSION_COOKIE_NAME = 'sid'
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_REFRESH_EACH_REQUEST = False
    SECRET_KEY = 'secret'
    SESSION_TYPE = 'sqlalchemy'
    SESSION_SQLALCHEMY_TABLE = 'sessions'
    SESSION_SQLALCHEMY = db


class DevConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True
    ASSETS_DEBUG = True
    SQLALCHEMY_ECHO = True
    SESSION_COOKIE_SECURE = False
    # SESSION_TYPE = 'redis'
    # SESSION_REDIS = '127.0.0.1:6379 instance'
