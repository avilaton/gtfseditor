#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..base import Base
from ..mixins import ToJSONMixin
from sqlalchemy import Column, types


class Transfer(Base, ToJSONMixin):

    __tablename__ = 'transfers'

    from_stop_id = Column(types.Integer, primary_key=True)
    to_stop_id = Column(types.Integer)
    transfer_type = Column(types.String(50))
