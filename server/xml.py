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

class Kml(object):
    """docstring for Kml"""
    def __init__(self):
        super(Kml, self).__init__()

    def renderStops(self, stops):
        renderer = pystache.Renderer()
        with codecs.open('server/templates/stops.mustache', 'r', 'utf-8') as templateFile:
                template = templateFile.read()
                parsed = pystache.parse(template)

        return renderer.render(parsed, {'stops': stops})

def main():
    db = o.dbInterface(config.DATABASE)
    toolbox = gtfsdb.toolbox(db)

    stops = toolbox.stops()
    kml = Kml()
    kmlString = kml.renderStops(stops)

    outFilename = 'compiled/stops.kml'
    with codecs.open(outFilename, 'w', 'utf-8') as outFile:
        outFile.write(kmlString)

if __name__ == '__main__':
    main()