#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, types

from .gtfsbase import GTFSBase
from ..base import Base
from ..mixins import ToJSONMixin, Versioned


class Shape(Base, ToJSONMixin, Versioned, GTFSBase):
    __tablename__ = 'shapes'

    shape_id = Column(types.Integer, primary_key=True)
    shape_pt_lat = Column(types.Float(precision=53))
    shape_pt_lon = Column(types.Float(precision=53))
    shape_pt_time = Column(types.String(50))
    shape_pt_sequence = Column(types.Integer, primary_key=True)

    @classmethod
    def vertices(cls, shape_id):
        return db.session.query(cls)\
            .filter(cls.shape_id == shape_id)\
            .order_by(cls.shape_pt_sequence)

    @classmethod
    def get_vertices_array(cls, shape_id):
        return [[pt.shape_pt_lon, pt.shape_pt_lat] for pt in cls.vertices(shape_id).all()]
