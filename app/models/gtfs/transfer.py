#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types

from .gtfsbase import GTFSBase
from ..base import Base
from ..mixins import ToJSONMixin, Versioned


class Transfer(Base, ToJSONMixin, Versioned, GTFSBase):
    __tablename__ = 'transfers'

    from_stop_id = Column(types.Integer, primary_key=True)
    to_stop_id = Column(types.Integer)
    transfer_type = Column(types.String(50))
