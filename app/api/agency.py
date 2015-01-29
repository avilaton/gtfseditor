#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Agency
from . import api
from app.tasks import sendEmail
from app.tasks import buildFeed


@api.route('/agency')
@api.route('/agency/')
def get_agencys():
    agencys = Agency.query.all()
    return jsonify({
        'agencys': [item.to_json for item in agencys]
    })


@api.route('/mail')
@api.route('/mail/')
def get_agencys():
    job = sendEmail.delay("test")
    return jsonify({"task": job.id})


@api.route('/feed')
@api.route('/feed/')
def get_agencys():
    job = buildFeed.delay()
    return jsonify({'task': job.id})


@api.route('/agency/<agency_id>')
def getAgency(agency_id):
    item = Agency.query.get_or_404(agency_id)
    return jsonify(item.to_json)


@api.route('/agency/<agency_id>', methods=['PUT'])
def updateAgency(agency_id):
    data = request.json
    item = Agency.query.get_or_404(data.get('agency_id'))
    item = Agency(**data)
    db.session.merge(item)
    return jsonify(item.to_json)


@api.route('/agency/', methods=['OPTIONS', 'POST'])
def createAgency():
    item = Agency(**request.json)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_json), 201,{'Location': url_for('api.getAgency', agency_id=item.agency_id, _external=True)}


@api.route('/agency/<agency_id>', methods=['DELETE'])
def delete_agency(agency_id):
    agency = Agency.query.filter_by(agency_id = agency_id).one()
    db.session.delete(agency)
    db.session.commit()
    return jsonify({'status': 'success'}), 200

