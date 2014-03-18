#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      export.py
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

import ormgeneric as o
import gtfsdb
import pystache
import codecs
import config
import zipfile

class Kml(object):
    """docstring for Kml"""
    def __init__(self, template):
        super(Kml, self).__init__()
        self.renderer = pystache.Renderer()
        self.templateFile = codecs.open(template, 'r', 'utf-8')
        self.template = pystache.parse(self.templateFile.read())

    def renderKml(self, data, filename):
        kmlString = self.renderer.render(self.template, data)

        with codecs.open(filename, 'w', 'utf-8') as outFile:
            outFile.write(kmlString)

    def renderKmz(self, data, filename):
        kmlString = self.renderer.render(self.template, data)

        with zipfile.ZipFile(filename, mode="w", compression=zipfile.ZIP_DEFLATED) as kmz:
            kmz.writestr('doc.kml', kmlString.encode('utf-8'))

def main():
    db = o.dbInterface(config.DATABASE)
    toolbox = gtfsdb.toolbox(db)

    trips = {trip['trip_id']:dict(trip) for trip in db.select('trips')}

    stops = toolbox.stops()
    for stop in stops:
        stop_id = stop['stop_id']
        l = db.select('stop_seq',stop_id=str(stop_id))
        stop['trips'] = [trips[t['trip_id']] for t in l]

    kml = Kml('server/templates/stops.mustache')
    kml.renderKml({'stops': stops}, 'public/kml/stops.kml')
    kml.renderKmz({'stops': stops}, 'public/kml/stops.kmz')

if __name__ == '__main__':
    main()