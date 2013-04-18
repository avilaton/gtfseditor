#!/usr/bin/env python

import bottle
from bottle import route, static_file, post
import ormgeneric as o

db = o.dbInterface('dbRecorridos.sqlite')


@route('/')
def index():
    return static_file('index.html',root='./')

@route('/assets/<filepath:path>')
def server_files(filepath):
    return static_file(filepath, root='./assets/')

@route('/api/routes/')
@route('/api/routes')
def routes():
    routes = []
    for row in db.select('routes'):
        data = {}
        for k in ['route_id', 'agency_id', 'route_short_name', 
            'route_long_name', 'route_desc', 'route_type', 
            'route_color']:
            data.update({k:row[k]})
        routes.append(data)
    return {'routes': routes}

@route('/api/route/<route_id>/trips')
@route('/api/route/<route_id>/trips/')
def routeTrips(route_id):
    trips = []
    for row in db.select('trips',route_id=route_id):
        trips.append({
            'service_id':row['service_id'],
            'trip_id':row['trip_id'],
            'trip_headsign':row['trip_headsign'],
            'trip_short_name':row['trip_short_name'],
            'direction_id':row['direction_id'],
            'shape_id':row['shape_id']
            })
    return {'trips':trips}

@post('/')
def responderpost():
    print 'post received'
    return {'success':True}

bottle.debug(True)
app = bottle.app()

if __name__ == '__main__':
    from bottle import run
    run(app,reloader=True)