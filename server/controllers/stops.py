#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, request, post, put, delete
# remove this global latter on
from server.transitfeededitor import tb

@route('/api/stop/<stop_id>')
def findStop(stop_id):
  return tb.findStop(stop_id)

@post('/api/stop/<stop_id>')
def createStop(stop_id):
  return tb.createStop(stop_id, request.json)

@put('/api/stop/<stop_id>')
def updateStop(stop_id):
  return tb.updateStop(stop_id, request.json)

@delete('/api/stop/<stop_id>')
def deleteStop(stop_id):
  return tb.deleteStop(stop_id)

@route('/api/bbox')
def getBBOX():
  bbox = request.query['bbox']
  filterQuery = request.query['filter']
  return tb.bbox(bbox, filterQuery)
