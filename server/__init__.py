# -*- coding: utf-8 -*-
__version__ = '0.0.1'

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('server.log')
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
from sqlalchemy.ext.declarative import declarative_base

TEMPLATE_PATH.append("./server/views/")
TEMPLATE_PATH.remove("./views/")

Base = declarative_base()
engine = create_engine(config.DATABASE_URL, echo=config.DEBUG)

from models import *

Base.metadata.create_all(engine)

app = Bottle()

def initialize():
	
	from bottle.ext import sqlalchemy

	plugin = sqlalchemy.Plugin(
		engine, # SQLAlchemy engine created with create_engine function.
		Base.metadata, # SQLAlchemy metadata, required only if create=True.
		keyword='db', # Keyword used to inject session database in a route (default 'db').
		create=True, # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
		commit=True, # If it is true, plugin commit changes after route is executed (default True).
		use_kwargs=False # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
	)

	app.install(plugin)

	from controllers import stops
	from controllers import static
	from controllers import routes
	from controllers import shapes
	from controllers import trips

	logger.info("Controllers Loaded")
	return app
