#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types, ForeignKey, UniqueConstraint

from .gtfsbase import GTFSBase
from ..base import Base
from ..mixins import ToJSONMixin, Versioned


class CalendarDate(Base, ToJSONMixin, Versioned, GTFSBase):
    __tablename__ = 'calendar_dates'

    service_id = Column(types.Integer,
                        ForeignKey("calendar.service_id",
                                   onupdate="CASCADE",
                                   ondelete="CASCADE"),
                        primary_key=True)
    date = Column(types.String(50), primary_key=True)
    exception_type = Column(types.String(50), primary_key=True)

    # __table_args__ = (UniqueConstraint(service_id, date,exception_type),)