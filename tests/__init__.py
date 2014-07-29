#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from server.models import *

DATABASE_URL = 'sqlite:///dev.sqlite'
# DATABASE_URL = 'sqlite:///:memory:'
DEBUG = True

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=DEBUG)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

class ServerTestCase(TestCase):

    def _create_app(self):
        raise NotImplementedError

    def _create_fixtures(self):
        self.user = UserFactory()

    def setUp(self):
        self.db = Session()
        # self.app = self._create_app()
        # self.client = self.app.test_client()
        # self.app_context = self.app.app_context()
        # self.app_context.push()
        # db.create_all()
        # self._create_fixtures()
        # self._create_csrf_token()

    def tearDown(self):
        # db.drop_all()
        # self.app_context.pop()
        pass

