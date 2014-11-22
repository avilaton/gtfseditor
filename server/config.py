#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

ENV = os.environ.get('ENV', 'dev')
MODES = ["frequency", "initial-times", "full-spec"]

if ENV == "dev":
	DEBUG = True
	DATABASE_URL = 'sqlite:///dev.sqlite'

if ENV == "staging":
	DEBUG = True
	DATABASE_URL = 'postgres:///mza'

if ENV == "prod":
	DEBUG = False
	DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres:///mza')

# To be moved into a column in the routes table
BUILD_MODE = MODES[1]
