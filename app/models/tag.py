#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types, ForeignKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_continuum import version_class

from .base import Base
from .gtfs import Agency

AgencyVersion = version_class(Agency)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(types.Integer, primary_key=True)
    name = Column(types.String(50))
    agency_versions = relationship("AgencyVersion", secondary="agency_tags", backref="tags")


class AgencyTag(Base):
    __tablename__ = 'agency_tags'

    agency_id = Column(types.Integer, primary_key=True)
    transaction_id = Column(types.Integer)
    tag_id = Column(types.Integer, ForeignKey('tags.id'), primary_key=True)

    __table_args__ = (ForeignKeyConstraint([agency_id, transaction_id],
                                           [AgencyVersion.agency_id, AgencyVersion.transaction_id]),
                      {})

