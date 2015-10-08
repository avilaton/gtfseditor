#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import Base
from .entity import Entity
from sqlalchemy import orm, Column, types, ForeignKey


class CalendarDate(Base, Entity):

    __tablename__ = 'calendar_dates'

    service_id = Column(types.Integer, ForeignKey("calendar.service_id",
                                                  onupdate="CASCADE"),
                                      primary_key=True)
    date = Column(types.String(50), primary_key=True)
    exception_type = Column(types.String(50), primary_key=True)
