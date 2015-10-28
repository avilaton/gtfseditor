#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types

from ..base import Base
from ..mixins import ToJSONMixin


class Calendar(Base, ToJSONMixin):

    __tablename__ = 'calendar'
    __versioned__ = {
        'base_classes': (Base, ToJSONMixin, )
    }

    service_id = Column(types.Integer, primary_key=True)
    service_name = Column(types.String(50))
    start_date = Column(types.String(50))
    end_date = Column(types.String(50))
    monday = Column(types.String(50))
    tuesday = Column(types.String(50))
    wednesday = Column(types.String(50))
    thursday = Column(types.String(50))
    friday = Column(types.String(50))
    saturday = Column(types.String(50))
    sunday = Column(types.String(50))
