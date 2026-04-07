import sys
import os
import pytest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import create_app
from src.database import db

@pytest.fixture
def app():
    app = create_app(
        testing=True,
        database_uri="sqlite:///:memory:"
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def session(app):
    return db.session
