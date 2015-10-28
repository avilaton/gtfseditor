#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types, ForeignKey

from ..base import Base
from ..mixins import ToJSONMixin


class CalendarDate(Base, ToJSONMixin):

    __tablename__ = 'calendar_dates'
    __versioned__ = {
        'base_classes': (Base, ToJSONMixin, )
    }

    service_id = Column(types.Integer,
                        ForeignKey("calendar.service_id",
                                   onupdate="CASCADE",
                                   ondelete="CASCADE"),
                        primary_key=True)
    date = Column(types.String(50), primary_key=True)
    exception_type = Column(types.String(50), primary_key=True)
