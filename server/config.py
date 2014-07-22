#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

DATABASE_URL = 'sqlite:///database/dev.sqlite'
# DATABASE_URL = 'sqlite:///database/test.sqlite'
# DATABASE_URL = 'sqlite:///database/1.0.9.sqlite'
# DATABASE_URL = 'sqlite:///:memory:'
# DATABASE_URL = 'postgres:///mza'
# heroku setup
# DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres:///mza')
DEBUG = False