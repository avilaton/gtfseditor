#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	   geojson.py
#	   
#	   Copyright 2012 Gaston Avila <avila.gas@gmail.com>
#	   
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU General Public License as published by
#	   the Free Software Foundation; either version 2 of the License, or
#	   (at your option) any later version.
#	   
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU General Public License for more details.
#	   
#	   You should have received a copy of the GNU General Public License
#	   along with this program; if not, write to the Free Software
#	   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#	   MA 02110-1301, USA.


def feature(id=None, feature_type="Point", coords=[], properties={}):
	result ={
		"type":"Feature",
		"id":id,
		"properties":properties,
		"geometry":{
			"type": feature_type, 
			"coordinates": coords
		}
		#~ ,"crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:OGC:1.3:CRS84"}}
	}
	return result
	
def featureCollection(features):
	""" Wraps an array of geoJson features as a Feature Collection """
	result = {
		"type": "FeatureCollection",
		"crs":{
				"type":"name", 
				"properties":{
					"name":"urn:ogc:def:crs:OGC:1.3:CRS84"
				}
			}
		}
	result.update({"features":features})
	return result

def geoJsonPolygon(id,coordList):
	""" takes a table of coordinates and returns a geoJson polygon """
	geoJsonFeature = {
		"type":"Feature",
		"id":id,
		#~ "properties":properties,
		"geometry":{
			"type":"Polygon", 
			"coordinates" : coordList
		}
	}
	return geoJsonFeature
	
def lineString(id,coordList,properties):
	""" takes a table of coordinates and returns a geoJson LineString """
	if not properties:
		properties = {}
	geoJsonFeature = {
		"type":"Feature",
		"id":id,
		"properties":properties,
		"geometry":{
			"type":"LineString", 
			"coordinates" : coordList
		}
	}
	return geoJsonFeature

if __name__ == '__main__':
	print geoJsonPolygon('test',[[0,1],[5,9]])
