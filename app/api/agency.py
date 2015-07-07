#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, url_for
from flask import json
from flask import Response
from .. import db
from ..models import Agency
from . import api
from .decorators import admin_required


@api.route('/agency')
@api.route('/agency/')
def get_agencys():
    agencys = Agency.query.all()
    return Response(json.dumps([item.to_json for item in agencys]),
        mimetype='application/json')


@api.route('/agency/<agency_id>')
def getAgency(agency_id):
    item = Agency.query.get_or_404(agency_id)
    return jsonify(item.to_json)


@api.route('/agency/<agency_id>', methods=['PUT'])
@admin_required
def updateAgency(agency_id):
    data = request.json
    item = Agency.query.get_or_404(data.get('agency_id'))
    item = Agency(**data)
    db.session.merge(item)
    db.session.commit()
    return jsonify(item.to_json)


@api.route('/agency/', methods=['POST'])
@admin_required
def createAgency():
    item = Agency(**request.json)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_json), 201,{'Location': url_for('api.getAgency', agency_id=item.agency_id, _external=True)}


@api.route('/agency/<agency_id>', methods=['DELETE'])
@admin_required
def delete_agency(agency_id):
    agency = Agency.query.filter_by(agency_id = agency_id).one()
    db.session.delete(agency)
    db.session.commit()
    return jsonify({'status': 'success'}), 200
