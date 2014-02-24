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

from optparse import OptionParser
import os
import glob
import zipfile

def convert(inputFile, outputdir):
    print "converting", inputFile
    with zipfile.ZipFile(inputFile, "r") as z:
        kml = z.read('doc.kml')

    baseFilename = os.path.basename(inputFile)
    filename, extension = os.path.splitext(baseFilename)

    outputFile = os.path.join(outputdir, filename + '.kml')
    with open(outputFile, 'w') as output:
        output.write(kml)

def main():
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
                      help="kmz FILE or DIR to be converted", metavar="FILE")
    parser.add_option("-o", "--output", dest="output",
                      help="output directory", metavar="DIR")

    (options, args) = parser.parse_args()
    print os.path.isdir(options.output), options

    if os.path.isdir(options.input):
        assert os.path.isdir(options.output)
        files = glob.glob(options.input+'*.kmz')
        files.extend(glob.glob(options.input+'*.KMZ'))
        files.sort()
        for filename in files:
            convert(filename, options.output)
    else:
        convert(options.input)

if __name__ == '__main__':
    main()