#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, request, post, put, delete
# remove this global latter on
from server.transitfeededitor import tb

@route('/api/shape/<shape_id>')
def shape(shape_id):
  return tb.shape(shape_id)

@put('/api/shape/<shape_id>')
def shape(shape_id):
  geojsonShape = request.json
  return tb.saveShape(shape_id, geojsonShape)
