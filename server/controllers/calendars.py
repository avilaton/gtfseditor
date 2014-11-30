#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request
import json
from server.models import Calendar
from server import app

BASE = '/api/calendars'

@app.get(BASE)
@app.get(BASE + '/')
def all(db):
  return {'rows': [row.as_dict for row in db.query(Calendar).all()]}

@app.route(BASE + '/<service_id>', method=['OPTIONS', 'PUT'])
def update(db, service_id):
  data = request.json
  model = Calendar(**data)
  db.merge(model)
  return model.as_dict

@app.route(BASE, method=['OPTIONS', 'POST'])
def create(db):
  data = request.json
  model = Calendar(**data)
  db.add(model)
  return model.as_dict

@app.route(BASE + '/<service_id>', method=['OPTIONS', 'DELETE'])
def deleteRoute(db, service_id):
  model = db.query(Calendar).filter(Calendar.service_id == service_id).one()
  db.delete(model)
  return {'success': True}