# -*- coding: utf-8 -*-
__version__ = '0.0.1'

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('logs.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

import config
from bottle import Bottle, TEMPLATE_PATH
from sqlalchemy import create_engine

TEMPLATE_PATH.append("./server/views/")
TEMPLATE_PATH.remove("./views/")

engine = create_engine(config.DATABASE_URL, echo=config.DEBUG)

from models import Base

# Base.metadata.create_all(engine)


from cors import EnableCors

app = Bottle()

import bottle
from bottle import request

@app.error(405)
def method_not_allowed(res):
    if request.method == 'OPTIONS':
        new_res = bottle.HTTPResponse()
        new_res.set_header('Access-Control-Allow-Origin', '*')
        new_res.set_header('Access-Control-Allow-Headers', 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token')

        return new_res
    res.headers['Allow'] += ', OPTIONS'
    return request.app.default_error_handler(res)

@app.hook('after_request')
def enableCORSAfterRequestHook():
    bottle.response.set_header('Access-Control-Allow-Origin', '*')

def initialize():
	
	from bottle.ext import sqlalchemy

	sqlAlchemyPlugin = sqlalchemy.Plugin(
		engine, # SQLAlchemy engine created with create_engine function.
		Base.metadata, # SQLAlchemy metadata, required only if create=True.
		keyword='db', # Keyword used to inject session database in a route (default 'db').
		create=True, # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
		commit=True, # If it is true, plugin commit changes after route is executed (default True).
		use_kwargs=False # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
	)

	corsPlugin = EnableCors()

	app.install(sqlAlchemyPlugin)
	app.install(corsPlugin)

	from controllers import stops
	from controllers import routes
	from controllers import shapes
	from controllers import trips
	from controllers import feed
	from controllers import reports
	from controllers import static

	logger.info("Controllers Loaded")
	return app
