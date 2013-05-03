#!/usr/bin/env python

import bottle
from bottle import route, static_file, post, request
import ormgeneric as o
import geojson

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

@route('/api/bboxold')
def bbox():
    bbox = request.query['bbox']
    w,s,e,n = map(float,bbox.split(','))
    q = """SELECT * FROM stops
            WHERE 
            stop_id IN (SELECT DISTINCT stop_id FROM stop_seq)
            AND (stop_lat BETWEEN {s} AND {n})
            AND (stop_lon BETWEEN {w} AND {e})
            LIMIT 300
            """.format(s=s,n=n,w=w,e=e)
    db.query(q)
    features = []
    for stop in db.cursor.fetchall():
        l = db.select('stop_seq',stop_id=stop['stop_id'])
        lineas = [{'trip_id':t['trip_id']} for t in l]
        f = geojson.geoJsonFeature(stop['stop_id'],
            stop['stop_lon'],
            stop['stop_lat'],
            {'stop_id':stop['stop_id'],
            'stop_lineas':lineas,
            'stop_calle':stop['stop_calle'],
            'stop_numero':stop['stop_numero'],
            'stop_esquina':stop['stop_esquina'],
            'stop_entre':stop['stop_entre']})
        features.append(f)
    resultGeoJson = geojson.geoJsonFeatCollection(features)
    return resultGeoJson

@route('/api/bbox')
def getBBOX():
    bbox = request.query['bbox']
    w,s,e,n = map(float,bbox.split(','))
    q = """SELECT * 
        FROM stops s INNER JOIN stop_seq sq ON s.stop_id=sq.stop_id
        WHERE 
            (stop_lat BETWEEN {s} AND {n})
            AND 
            (stop_lon BETWEEN {w} AND {e})
        LIMIT 300
        """.format(s=s,n=n,w=w,e=e)
    db.query(q)
    features = []
    rows = db.cursor.fetchall()
    d = {}
    for r in rows:
        stop = dict(r)
        linea = stop.pop('trip_id')
        stop_id = stop.pop('stop_id')
        print stop
        if stop_id in d:
            d[stop_id]['lineas'].append(linea)
        else:
            d[stop_id] = stop
            d[stop_id]['lineas'] = [linea]
    for stop_id,stop in d.items():
        f = geojson.geoJsonFeature(stop_id,
            stop['stop_lon'],
            stop['stop_lat'],
            {'stop_id':stop_id,
            'stop_lineas':stop['lineas'],
            'stop_calle':stop['stop_calle'],
            'stop_numero':stop['stop_numero'],
            'stop_esquina':stop['stop_esquina'],
            'stop_entre':stop['stop_entre']})
        features.append(f)
    resultGeoJson = geojson.geoJsonFeatCollection(features)
    return resultGeoJson

bottle.debug(True)
app = bottle.app()

if __name__ == '__main__':
    from bottle import run
    run(app,reloader=True)