#!/usr/bin/python
# -*- coding: utf-8 -*-

import tablib
import ormgeneric as o
import gtfsdb
import config

db = o.dbInterface(config.DATABASE)
toolbox = gtfsdb.toolbox(db)

def getStops():
    trips = {trip['trip_id']:dict(trip) for trip in db.select('trips')}

    stops = toolbox.stops()
    # for stop in stops:
    #     stop_id = stop['stop_id']
    #     l = db.select('stop_seq',stop_id=str(stop_id))
    #     stop['trips'] = [trips[t['trip_id']] for t in l]

    headers = sorted(stops[0].keys())
    stopsRows = []
    for stop in stops:
        row = [stop[k] if stop[k] is not None else '' for k in headers]
        stopsRows.append(row)
    return headers, stopsRows

def getTrips():
    trips = []
    routes = toolbox.routes()['routes']
    for route in routes:
        route_id = route['route_id']
        for trip in toolbox.trips(route_id)['trips']:
            trips.append(trip['trip_id'])
    return trips

def getTripStops(trip_id):
    db.query("""SELECT * FROM stop_seq 
        WHERE trip_id="{trip_id}" 
        ORDER BY stop_sequence""".format(trip_id=trip_id))

    rows = []
    for stop in db.cursor.fetchall():
        rows.append(dict(stop))
    return rows

def makeSheet(title, headers, rows):
    stopsData = tablib.Dataset()
    stopsData.title = title
    stopsData.headers = headers
    for stop in rows:
        stopsData.append(stop)
    return stopsData

def saveBook(sheets):
    book = tablib.Databook()
    for sheet in sheets:
        book.add_sheet(sheet)

    with open('stops.xls', 'wb') as f:
        f.write(book.xls)

def main():
    sheets = []
    headers, stopsRows = getStops()
    print stopsRows[0]
    stopsSheet = makeSheet('stops', headers, stopsRows)
    sheets.append(stopsSheet)

    for trip_id in getTrips():
        rows = getTripStops(trip_id)
        headers = rows[0].keys()

        onlyStops = [r['stop_id'] for r in rows]
        arrayRows = []
        for stop in rows:
            nRow = [stop[k] if stop[k] is not None else '' for k in headers]
            arrayRows.append(nRow)
        print rows[0]
        print arrayRows[0]
        seqSheet = makeSheet(trip_id, headers, arrayRows)
        sheets.append(seqSheet)


    saveBook(sheets)

if __name__ == '__main__':
    main()
