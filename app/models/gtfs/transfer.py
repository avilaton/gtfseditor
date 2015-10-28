#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types

from ..base import Base
from ..mixins import ToJSONMixin


class Transfer(Base, ToJSONMixin):

    __tablename__ = 'transfers'
    __versioned__ = {}

    from_stop_id = Column(types.Integer, primary_key=True)
    to_stop_id = Column(types.Integer)
    transfer_type = Column(types.String(50))
