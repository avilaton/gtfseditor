#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(types.Integer, primary_key=True)
    name = Column(types.String(50))
    agencies = relationship("AgencyTag", backref="tag")


class AgencyTag(Base):
    __tablename__ = 'agency_tag'

    id = Column(types.Integer, primary_key=True)
    agency_id = Column(types.Integer, ForeignKey('agency_version.agency_id'), primary_key=True)
    transaction_id = Column(types.Integer, ForeignKey('agency_version.transaction_id'), primary_key=True)
    tag_id = Column(types.Integer, ForeignKey('tags.id'))

