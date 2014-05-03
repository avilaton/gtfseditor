#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, request, post, put, delete
from server.models import Stop

@route('/api/stop/<stop_id>')
def findStop(stop_id):
  return Stop.get(stop_id)

@post('/api/stop/<stop_id>')
def createStop(stop_id):
  # Should be
  # stop = Stop(stop_id, request.json)
  # return stop.save()
  return Stop().create(stop_id, request.json)

@put('/api/stop/<stop_id>')
def updateStop(stop_id):
  # Should be
  # stop = Stop.get(stop_id)
  # stop.update(request.json)
  # return stop.save()
  return Stop().update(stop_id, request.json)

@delete('/api/stop/<stop_id>')
def deleteStop(stop_id):
  # Should be
  # stop = Stop.get(stop_id)
  # return stop.delete()
  return Stop().delete(stop_id)

@route('/api/bbox')
def getBBOX():
  bounds = request.query['bbox']
  filterQuery = request.query['filter']
  return Stop.bbox(bounds, filterQuery)
