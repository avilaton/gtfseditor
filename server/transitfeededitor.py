#!/usr/bin/env python
# -*- coding: utf-8 -*-

DEBUG = False

from bottle import hook, TEMPLATE_PATH
from cork import Cork

import database
import gtfsdb
import config

import bottle
bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024
app = bottle.app()
TEMPLATE_PATH.append("./server/views/")
TEMPLATE_PATH.remove("./views/")

# # heroku setup
# import urlparse
# import os
# urlparse.uses_netloc.append('postgres')
# url = urlparse.urlparse(os.environ['DATABASE_URL'])
# db = database.Postgress(
#   database = url.path[1:], 
#   user = url.username, 
#   password = url.password, 
#   host = url.hostname,
#   port = url.port
# )

# db = database.Postgress(
#   database='testdb', 
#   user='tester', 
#   password='tester', 
#   host='127.0.0.1'
# )

db = database.dbInterface(config.DATABASE)

tb = gtfsdb.toolbox(db)

@hook('after_request')
def after_request():
  pass
  # print("commit to db...")
  # db.connection.commit()

@hook('before_request')
def before_request():
  #db.open()
  return

from controllers import *
