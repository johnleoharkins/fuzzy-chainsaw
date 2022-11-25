import pytest

from passlib.hash import pbkdf2_sha256
import os

print(os.getcwd())

from src.app import create_app
from src.extensions import db


# Fixtures for the application, test client, and CLI runner
# Pytest fixtures allow writing pieces of code that are reusable across tests.
# ests are functions that start with test_, in Python modules that start with test_.
# Tests can also be further grouped in classes that start with Test.
# Run tests // $ python -m pytest tests/

@pytest.fixture()
def app():
    from config import TestingConfig
    # app = application

    app = create_app()
    app.config.from_object(TestingConfig)

    # other setup can go here


    yield app
    # clean up / reset resources here



@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.mark.fixture
def app_ctx(app):
    with app.app_context():
        yield


@pytest.mark.usefixtures("app_ctx")
def seed_db(application):
    # user1 = UserModel(username="WhY S0 S3Ri0uS", password=pbkdf2_sha256.hash("password"))
    # db.session.add(user1)
    # db.session.commit()
    #
    # post1 = PostModel(author_id=1, title="First Post!", body="this is my first post - enjoi")
    # db.session.add(post1)
    # db.session.commit()
    pass


@pytest.mark.usefixtures("app_ctx")
def clear_db(app):
    app.db.drop_all()


