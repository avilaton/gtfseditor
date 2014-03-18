#!/usr/bin/python
# -*- coding: utf-8 -*-

import tablib
import ormgeneric as o
import gtfsdb
import config

def read():
    db = o.dbInterface(config.DATABASE)
    toolbox = gtfsdb.toolbox(db)

    trips = {trip['trip_id']:dict(trip) for trip in db.select('trips')}

    stops = toolbox.stops()
    # for stop in stops:
    #     stop_id = stop['stop_id']
    #     l = db.select('stop_seq',stop_id=str(stop_id))
    #     stop['trips'] = [trips[t['trip_id']] for t in l]

    return stops

def main():
    stops = read()
    book = tablib.Databook()
    stopsData = tablib.Dataset()
    stopsData.title = 'stops'
    headers = sorted(stops[0].keys())
    stopsData.headers = headers
    stopsRows = []
    for stop in stops:
        row = [stop[k] if stop[k] is not None else '' for k in headers]
        stopsRows.append(row)

    for stop in stopsRows:
        stopsData.append(stop)

    book.add_sheet(stopsData)

    with open('stops.xls', 'wb') as f:
        # f.write(stopsData.xlsx)
        f.write(book.xls)
    
    # with open('stops.ods', 'wb') as f:
    #     f.write(book.ods)

if __name__ == '__main__':
    main()
