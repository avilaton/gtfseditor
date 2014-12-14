#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request
import json
from server.models import Agency
from server import app

@app.get('/api/agency')
@app.get('/api/agency/')
def agency(db):
  agencys = db.query(Agency).order_by(Agency.agency_name).all()
  return {'agency': [agency.as_dict for agency in agencys]}

@app.route('/api/agency/<agency_id>')
def getAgency(db, agency_id):
  print "Entre"
  agency = db.query(Agency).filter(Agency.agency_id == agency_id).first()
  if agency:
    return agency.as_dict
  else:
    abort(404, 'no such agency_id')

@app.route('/api/agency/<agency_id>', method=['OPTIONS', 'PUT'])
def updateAgency(db, agency_id):
  data = request.json
  agency = Agency(**data)
  db.merge(agency)
  return agency.as_dict

@app.route('/api/agency', method=['OPTIONS', 'POST'])
def createAgency(db):
  data = request.json
  agency = Agency(**data)
  db.add(agency)
  return agency.as_dict

@app.route('/api/agency/<agency_id>', method=['OPTIONS', 'DELETE'])
def deleteAgency(db, agency_id):
  agency = db.query(Agency).filter(Agency.agency_id == agency_id).one()
  db.delete(agency)
  return {'success': True}

