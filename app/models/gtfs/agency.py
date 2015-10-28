#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy_continuum import version_class

from ..base import Base
from ..mixins import ToJSONMixin


class Agency(Base, ToJSONMixin):

    __tablename__ = 'agency'
    __versioned__ = {}

    agency_id = Column(types.Integer, primary_key=True)
    agency_name = Column(types.String(50))
    agency_url = Column(types.String(50))
    agency_timezone = Column(types.String(50))
    agency_lang = Column(types.String(50))
    agency_phone = Column(types.String(50))


AgencyVersion = version_class(Agency)