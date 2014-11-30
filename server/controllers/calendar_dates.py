#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request
import json
from server.models import CalendarDate as Model
from server import app

BASE = '/api/' + Model.__tablename__

@app.get(BASE)
@app.get(BASE + '/')
def all(db):
  return {'rows': [row.as_dict for row in db.query(Model).all()]}

@app.route(BASE + '/<p_key_id>', method=['OPTIONS', 'PUT'])
def update(db, p_key_id):
  data = request.json
  model = Model(**data)
  db.merge(model)
  return model.as_dict

@app.route(BASE, method=['OPTIONS', 'POST'])
def create(db):
  data = request.json
  model = Model(**data)
  db.add(model)
  return model.as_dict

@app.route(BASE + '/<p_key_id>', method=['OPTIONS', 'DELETE'])
def deleteRoute(db, p_key_id):
  model = db.query(Model).filter(Model.service_id == p_key_id).one()
  db.delete(model)
  return {'success': True}