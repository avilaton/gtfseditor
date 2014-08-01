#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

DEBUG = False

# DATABASE_URL = 'sqlite:///dev.sqlite'
# DATABASE_URL = 'sqlite:///database/test.sqlite'
# DATABASE_URL = 'sqlite:///../cba.sqlite'
# DATABASE_URL = 'sqlite:///:memory:'
# DATABASE_URL = 'postgres:///mza'
# heroku setup
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres:///mza')

BUILD_MODE = 'cba'
