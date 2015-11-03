#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from sqlalchemy import Column, types

from .gtfsbase import GTFSBase
from ..base import Base
from ..mixins import ToJSONMixin, Versioned


class ShapePath(Base, ToJSONMixin, Versioned, GTFSBase):
    __tablename__ = 'shape_paths'

    shape_id = Column(types.Integer, primary_key=True)
    shape_path = Column(types.UnicodeText) # Stores json Array of Lon, Lat pairs

    @property
    def shape_path_array(self):
        return json.loads(self.shape_path)

    @property
    def shape_path_obj_array(self):
        shape_lat_lon = lambda pt: {'lon': pt[0], 'lat': pt[1]}
        array = json.loads(self.shape_path)
        return map(shape_lat_lon, array)
