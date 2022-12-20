from flask import Flask, render_template, request, session, send_from_directory
import os

from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_smorest import Api

# Flask extension objects
from src.extensions.scheduler import scheduler
from src.extensions.db import db

import os


def configure_logging(app):
    import logging
    from flask.logging import default_handler
    from logging.handlers import RotatingFileHandler

    root = logging.getLogger()
    # deactivate the default flask logger (no duplicate messages)
    root.removeHandler(default_handler)
    app.logger.removeHandler(default_handler)
    # new logger
    file_handler = RotatingFileHandler('logs/flaskapp.log', maxBytes=16384, backupCount=20)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(lineno)d]')
    file_handler.setFormatter(file_formatter)
    app.logger.addHandler(file_handler)

    root.addHandler(file_handler)
    root.info("new config for logs...")


# It is better to register error handlers with the application instance
#       so that they can view used by all view functions in all blueprints.
def register_error_pages(app):
    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('400.html'), 400

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('405.html'), 405

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500


def register_blueprints(api):
    from src.resources import MainBlueprint
    from src.resources import RedditBlueprint
    from src.resources import TwitterBlueprint
    api.register_blueprint(MainBlueprint)
    api.register_blueprint(RedditBlueprint)
    api.register_blueprint(TwitterBlueprint)


def initialize_extensions(app):
    from src.jobs import RedditJob
    from src.jobs import subreddit_job
    # from src.jobs import TweetJob

    # connect SQLAlchemy to application and create all tables
    with app.app_context():
        db.init_app(app)
        db.create_all()

    # connect flask-migrate
    # migrate = Migrate(app, db)
    # connect APScheduler extension, start

    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(**RedditJob)
    # connect flask-smorest extension to flask application, register blueprints
    api = Api(app)
    register_blueprints(api)
    # jwt config and instantiation
    jwt = JWTManager(app)
    # connect flask-CORS
    CORS(app, origins='*', methods='DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT',
         allow_headers=['Content-Type', 'Content-Length', 'Accept', 'Accept-Encoding', 'Host', 'Connection',
                        'User-Agent'], send_wildcard=True,
         expose_headers=['Content-Type', 'Content-Length', 'Accept', 'Accept-Encoding', 'Host', 'Connection',
                         'User-Agent', 'Authorization'], vary_header=True)


# application factory function
def create_app(db_url=None):
    app = Flask(__name__)
    APP_CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    APSCHEDULER_CONFIG = os.getenv('APSCHEDULER_CONFIG')
    app.config.from_object(APP_CONFIG_TYPE)
    app.config.from_object(APSCHEDULER_CONFIG)

    # configure_logging(app)
    app.secret_key = os.urandom(24)

    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    register_error_pages(app)
    initialize_extensions(app)
    return app

