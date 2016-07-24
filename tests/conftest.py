import os
import pytest

from app import create_app
from app import db as _db


TEST_DATABASE_URI = 'postgres:///gtfseditor_testing'


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    app = create_app('testing')

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    print('app in')

    def teardown():
        print('app out')
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""

    def teardown():
        print('db before drop all')
        _db.session.rollback()
        _db.drop_all()
        print('db after drop all')

    print('db in')
    _db.app = app
    _db.create_all()
    print('db create all')

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection)
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session