#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import CalendarDate
from . import api
from .decorators import admin_required


@api.route('/calendar_date/')
def get_calendars_date():
    calendar_date = CalendarDate.query.all()
    return jsonify({
        'calendar_date': [item.to_json for item in calendar_date]
    })


@api.route('/calendar_date/<id>')
def get_calendar_date(id):
    item = CalendarDate.query.filter_by(service_id = id).first()
    return jsonify(item.to_json)


@api.route('/calendar_date/', methods=['POST'])
@admin_required
def add_calendar_date():
    item = CalendarDate(**request.json)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_json), 201, \
        {'Location': url_for('api.get_calendar_date', id=item.service_id, _external=True)}


@api.route('/calendar_date/<id>', methods=['PUT'])
@admin_required
def edit_calendar_date(id):
    data = request.json
    item = CalendarDate.query.get_or_404(data.get('service_id'))
    item = CalendarDate(**data)
    db.session.merge(item)
    return jsonify(item.to_json)



@api.route('/calendar_date/<id>', methods=['DELETE'])
@admin_required
def delete_calendar_date(id):
    calendar_date = CalendarDate.query.filter_by(service_id = id).one()
    db.session.delete(calendar_date)
    db.session.commit()
    return jsonify({'status': 'success'}), 200
