# !/usr/bin/env python

import os
from dotenv import load_dotenv

load_dotenv()

# Find the absolute file path to the top level project directory
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration class. Contains default configuration settings + configuration settings applicable to all environments.
    """
    # Default settings
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    SECRET_KEY = os.getenv('SECRET_KEY', default='A very terrible secret key.')
    UPLOAD_FOLDER = './uploads'
    MAX_CONTENT_LENGTH = 24 * 1000 * 1000

    JWT_SECRET_KEY = "JOHNNY"
    PROPAGATE_EXCEPTIONS = True
    #  swagger openapi
    API_TITLE = "Project: PyUndrgrnd"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/openapi"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', default='')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', default='')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME', default='')
    MAIL_SUPPRESS_SEND = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSONIFY_PRETTYPRINT_REGULAR = True


    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL ')
    RESULT_BACKEND = os.getenv('RESULT_BACKEND')

    TWITTER_TOKEN = None
    TWITTER_TOKEN_RES = None


class DevelopmentConfig(Config):
    FLASK_DEBUG = 1
    POSTGRESQL_DEVDB = os.getenv('POSTGRESQL_DEVDB')
    SQLALCHEMY_DATABASE_URI = POSTGRESQL_DEVDB


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'test.db')


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    FLASK_DEBUG = 0
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URI', default="sqlite:///" + os.path.join(basedir, 'prod.db'))


class APSchedulerConfig:
    from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
    from src.extensions.db import db
    # POSTGRESQL_DEVDB = os.getenv('POSTGRESQL_DEVDB')
    # SCHEDULER_JOBSTORES = {
    #     'default': SQLAlchemyJobStore(url=POSTGRESQL_DEVDB, tablename="apscheduler_jobs")
    # }
    SCHEDULER_API_ENABLED = True
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': True,
        'max_instances': 1
    }