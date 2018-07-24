#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import Base
from sqlalchemy import orm

from sqlalchemy_continuum.plugins import FlaskPlugin
from sqlalchemy_continuum import make_versioned, version_class
from flask.globals import _app_ctx_stack, _request_ctx_stack


def fetch_current_user_id():
    from flask_login import current_user

    # Return None if we are outside of request context.
    if _app_ctx_stack.top is None or _request_ctx_stack.top is None:
        return
    try:
        return current_user.user_id
    except AttributeError:
        return


flask_plugin = FlaskPlugin(current_user_id_factory=fetch_current_user_id)
make_versioned(plugins=[flask_plugin])

from .permission import Permission
from .role import Role
from .user import User

from .gtfs import *

orm.configure_mappers()

from .tag import Tag
from .tag import AgencyTag