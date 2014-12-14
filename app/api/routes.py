#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Route
from . import api


@api.route('/routes/')
def get_routes():
    routes = Route.query.all()
    return jsonify({
        'routes': [item.to_json for item in routes]
    })


@api.route('/routes/<id>')
def get_route(id):
    item = Route.query.get_or_404(id)
    return jsonify(item.to_json)


@api.route('/routes/', methods=['POST'])
def add_route():
    item = Route(**request.json)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_json), 201, \
        {'Location': url_for('api.get_route', id=item.route_id, _external=True)}


@api.route('/routes/<id>', methods=['PUT'])
def edit_route(id):
    data = request.json
    item = Route.query.get_or_404(data.get('route_id'))
    item = Route(**data)
    db.session.merge(item)
    return jsonify(item.to_json)


@api.route('/routes/<id>', methods=['DELETE'])
def delete_route(id):
    route = Route.query.filter_by(route_id = id).one()
    db.session.delete(route)
    db.session.commit()
    return jsonify({'status': 'success'}), 200
