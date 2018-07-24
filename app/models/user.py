#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime

from .base import Base
from sqlalchemy import Column, types, ForeignKey

from app import db
from app import login_manager
from app.models import Role
from .permission import Permission

class User(Base):

    __tablename__ = "users"

    id = Column('user_id', types.Integer , primary_key=True)
    password_hash = Column(types.String(128))
    email = Column('email',types.String(50),unique=True , index=True)
    registered_on = Column(types.DateTime(), default=datetime.utcnow)
    role_id = Column(types.Integer, ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % (self.email)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

