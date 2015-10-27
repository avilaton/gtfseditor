#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from .base import Base
from .entity import Entity
from .permission import Permission
from sqlalchemy import orm, Column, types, ForeignKey


class Role(Base):

    __tablename__ = 'roles'

    id = Column(types.Integer, primary_key=True)
    name = Column(types.String(64), unique=True)
    default = Column(types.Boolean, default=False, index=True)
    permissions = Column(types.Integer)
    users = orm.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.COMMENT | Permission.EDIT_TIMES, True),
            'Agency': (Permission.COMMENT, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name
