#!/usr/bin/env python
# -*- coding: utf-8 -*-


# GET trips 

# SELECT * FROM stop_seq WHERE trip_id IN
# (SELECT trip_id FROM trips WHERE route_id='TA' OR route_id='TB' OR route_id='TC')

# GET STOPS

# SELECT * FROM stops WHERE stop_id IN
# 	(SELECT DISTINCT stop_id FROM stop_seq 
# 	    WHERE trip_id IN
# 	        (SELECT trip_id FROM trips 
# 	            WHERE route_id='TA' OR route_id='TB' OR route_id='TC'
# 	        )
# 	)

import database
import csv
import codecs

def unicodeDict(row):
    """ ugliest code ever """
    d = {}
    for k,v in row.items():
        if not v:
            d[k] = ''
        else:
            if type(v) is int:
                d[k] = unicode(v)
            elif type(v) is float:
                d[k] = unicode(v)
            elif type(v) is type(None):
                d[k] = str(v)
            else:
                d[k] = codecs.encode(v, 'utf-8')
    return d

def saveRowsToCsv(rows, filename):
    csvrows = []
    for row in rows:
        csvrows.append(unicodeDict(row))
    
    fieldnames = rows[0].keys()

    with open(filename, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        writer.writerows(csvrows)

    return csvrows

def getTrips(db):
    db.query("""SELECT trip_id, stop_id, stop_sequence FROM stop_seq 
        WHERE trip_id IN
            (SELECT trip_id FROM trips 
                WHERE route_id='TA' OR route_id='TB' OR route_id='TC')""")
    rows = []
    for r in db.cursor.fetchall():
        row = dict(r)
        row['trip_id'] = row['trip_id'].replace('vuelta','reg')
        rows.append(row)
    return rows

def getStops(db):
    db.query("""SELECT * FROM stops WHERE stop_id IN
          (SELECT DISTINCT stop_id FROM stop_seq 
              WHERE trip_id IN
                  (SELECT trip_id FROM trips 
                      WHERE route_id='TA' OR route_id='TB' OR route_id='TC'
                  )
          )""")
    l = 6000
    rows = []
    lookup = {}
    for r in db.cursor.fetchall():
        row = dict(r)
        stop_id_old = row['stop_id']
        lookup[stop_id_old] = l
        row['stop_id'] = l
        row['stop_code'] = ''
        rows.append(row)
        l += 1

    return rows, lookup

def getShapes(db):
    db.query("""SELECT * FROM shapes 
        WHERE shape_id IN(SELECT shape_id FROM trips 
                WHERE route_id='TA' OR route_id='TB' OR route_id='TC')""")
    rows = []
    for r in db.cursor.fetchall():
        row = dict(r)
        row['shape_id'] = row['shape_id'].replace('vuelta', 'reg')
        rows.append(row)
    return rows

def renumberTrips(trips, lookup):
    for seq in trips:
        seq['stop_id'] = lookup[seq['stop_id']]
    pass

def main():
    db = database.dbInterface('cba-0.1.5.sqlite')
    
    stops, lookup = getStops(db)
    saveRowsToCsv(stops, 'stops.csv')

    trips = getTrips(db)
    renumberTrips(trips, lookup)
    saveRowsToCsv(trips, 'stop_seq.csv')

    shapes = getShapes(db)
    saveRowsToCsv(shapes, 'shapes.csv')

if __name__ == '__main__':
    main()