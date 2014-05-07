#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, request, put
from server.models import Shape

@route('/api/shape/<shape_id>')
def shape(shape_id):
  return Shape.get(shape_id)

@put('/api/shape/<shape_id>')
def shape(shape_id):
  geojsonShape = request.json
  return Shape.set(shape_id, geojsonShape)
