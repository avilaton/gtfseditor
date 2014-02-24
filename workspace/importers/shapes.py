#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      shapes.py
#      
#      Copyright 2012 Gaston Avila <avila.gas@gmail.com>
#      
#      This program is free software; you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation; either version 2 of the License, or
#      (at your option) any later version.
#      
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#      
#      You should have received a copy of the GNU General Public License
#      along with this program; if not, write to the Free Software
#      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#      MA 02110-1301, USA.

import os
import glob
import zipfile
import csv
from xml.dom.minidom import parseString

class kmz(object):
    """Parser for kmz"""
    def __init__(self, filename):
        self.filename = filename

    def extract(self):
        with zipfile.ZipFile(self.filename, "r") as z:
            for filename in z.namelist():
                return z.read(filename)
    
    def parse(self):
        kml = self.extract()
        dom = parseString(kml)
        LineString = dom.getElementsByTagName("LineString")[0]
        coord = LineString.getElementsByTagName("coordinates")[0].firstChild.wholeText.strip()
        # coordList = map(str, map(unicode.strip, coord.split('\n')))
        coordList = map(str, map(unicode.strip, coord.split(' ')))
        coordList = filter(lambda x: bool(x), coordList)
        coordList = [map(float, r.split(',')) for r in coordList]
        coordDict = [{'lon':r[0], 'lat':r[1] } for r in coordList]
        self.coords = self.removeDuplicates(coordDict)
        return self.coords

    def removeDuplicates(self, coordDict):
        coords = []
        coords.append(coordDict[1])
        for p in coordDict[1:]:
            print p
            if p != coords[-1]:
                coords.append(p)
            else:
                continue
        return coords
        

def main():
    files = glob.glob('*.kmz')
    files.extend(glob.glob('*.KMZ'))
    files.sort()

    fieldnames = ['shape_id', 'shape_pt_lat', 'shape_pt_lon', 'shape_pt_sequence']

    with open('shapes.txt', 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        for filename in files:
            shape_id = filename[0:-4].replace(" ",".").lower()

            points = kmz(filename).parse()
            print(str(len(points))+"\t found parsing: \t"+filename)
            for i, point in enumerate(points):
                writer.writerow({
                    'shape_id':shape_id, 
                    'shape_pt_lat': point['lat'], 
                    'shape_pt_lon': point['lon'], 
                    'shape_pt_sequence': i+1})

    trips_fields = ['route_id', 'service_id', 'trip_id', 'trip_headsign', 
        'trip_short_name', 'direction_id', 'shape_id']
    with open('trips.txt', 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, trips_fields)
        writer.writeheader()
        for filename in files:
            shape_id = filename[0:-4].replace(" ",".").lower()
            route_id = '.'.join(shape_id.split('.')[0:-1])
            direction_id = int(shape_id.find('ida') is -1)
            print direction_id, shape_id
            writer.writerow({
                'route_id': route_id,
                'trip_id': shape_id,
                'shape_id': shape_id,
                'direction_id': direction_id
                })
    
    routes_fields = ['route_id' , 'agency_id', 'route_short_name', 
        'route_long_name', 'route_desc', 'route_type', 'route_color', 
        'route_text_color']
    with open('routes.txt', 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, routes_fields)
        writer.writeheader()
        route_ids = set([])
        for filename in files:
            shape_id = filename[0:-4].replace(" ",".").lower()
            route_id = '.'.join(shape_id.split('.')[0:-1])
            print route_id
            route_ids.add(route_id)
        routes = [{'route_id': r, 'route_short_name': r} for r in route_ids]
        rows = sorted(routes, key=lambda k: k['route_id']) 
        writer.writerows(rows)    


if __name__ == '__main__':
    main()