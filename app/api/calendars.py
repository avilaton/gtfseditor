#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Calendar
from . import api

@api.route('/calendars/')
def get_calendars():
    calendars = Calendar.query.all()
    return jsonify({
        'calendars': [item.to_json for item in calendars]
    })


@api.route('/calendars/<id>')
def get_calendar(id):
    item = Calendar.query.get_or_404(id)
    return jsonify(item.to_json)

@api.route('/calendars/', methods=['POST'])
def add_calendar():
    item = Calendar(**request.json)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_json), 201, \
        {'Location': url_for('api.get_calendar', id=item.service_id, _external=True)}

@api.route('/calendars/<id>', methods=['PUT'])
def edit_calendar(id):
    data = request.json
    # item = Calendar.query.get_or_404(data.get('service_id'))
    item = Calendar(**data)
    db.session.merge(item)
    return jsonify(item.to_json)


@api.route('/calendars/<id>', methods=['DELETE'])
def delete_calendar(id):
    calendar = Calendar.query.filter_by(service_id = id).one()
    db.session.delete(calendar)
    db.session.commit()
    return jsonify({'status': 'success'}), 200
