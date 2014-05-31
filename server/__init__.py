# -*- coding: utf-8 -*-
__version__ = '0.0.1'
import config
from bottle import Bottle, TEMPLATE_PATH
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

TEMPLATE_PATH.append("./server/views/")
TEMPLATE_PATH.remove("./views/")

app = Bottle()



# import database
# db = database.dbInterface(config.DATABASE)

Base = declarative_base()
engine = create_engine(config.DATABASE_URL, echo=config.DEBUG)

from models import *

Base.metadata.create_all(engine)

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
