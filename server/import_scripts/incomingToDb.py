#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
lgr = logging.getLogger(__name__)
lgr.log("hello")
import database
import csv
import codecs
class Stop(object):
    """docstring for Stop"""
    def __init__(self, arg):
        self.fields = [
            'stop_id',
            'stop_name',
            'stop_lat',
            'stop_lon',
            'stop_calle',
            'stop_numero',
            'stop_entre',
            'stop_esquina'
            ]
        self.d = {}
        self.parse(arg)

    def __repr__(self):
        return str(self.d)

    def parse(self, dictParams):
        for k,v in dictParams.items():
            if str(k) in 'stop_id':
                v = int(v)
            if type(v) is str:
                v = codecs.decode(v, 'utf-8')
            if k in self.fields:
                self.d.update({k:v})
    def save(self, db):
        db.insert('stops', **self.d)

def saveStops(stops):
    db = database.dbInterface('../database/cba-1.0.1.sqlite')
    for stop_id, stop in stops.items():
        stop.save(db)
    db.close()

def addFromFile(stops, filename):
    repeated = {}
    with open('../incoming/'+ filename) as csvFile:
        reader = csv.DictReader(csvFile)
        for r in reader:
            stop_id = r['stop_id']
            stop = Stop(r)
            if stop_id in stops:
                if stop.d != stops[stop_id].d:
                    pass
                    repeated[stop_id] = stop
                    print("stop already in collection, skipping")
                    print(r)
                    print(stops[stop_id])
            else:
                stops[stop_id] = stop
    return repeated

def show(stops):
    for stop_id, stop in stops.items():
        print(stop_id, stop)
    
def main():
    stops = {}
    repeated = addFromFile(stops, 'asf/stops.csv')
    repeated.update(addFromFile(stops, 'ccba/stops.csv'))
    repeated.update(addFromFile(stops, 'coniferal/stops.csv'))
    repeated.update(addFromFile(stops, 'ersa/stops.csv'))

    
    # show(stops)
    show(repeated)

    saveStops(stops)


if __name__ == '__main__':
    main()