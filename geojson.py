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


def geoJsonFeature(id,lon,lat,properties):
	jsonPoint ={
		"type":"Feature",
		"id":id,
		"properties":properties,
		"geometry":{
			"type":"Point", 
			"coordinates":[lon,lat]
		}
		#~ ,"crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:OGC:1.3:CRS84"}}
	}
	return jsonPoint
	
def geoJsonFeatCollection(features):
	""" Wraps an array of geoJson features as a Feature Collection """
	geoJson = {
		"type": "FeatureCollection",
		"crs":{
				"type":"name", 
				"properties":{
					"name":"urn:ogc:def:crs:OGC:1.3:CRS84"
				}
			}
		}
	geoJson.update({"features":features})
	return geoJson

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
	
def geoJsonLineString(id,coordList,properties):
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

def getGeoJsonTable(tableName):
	"""takes TABLE with lat,lon columns and outputs GeoJSON features"""
	features = []
	i=1
	for row in db.select(table=tableName):
		drow = dict(row)
		lat = drow.pop('lat')
		lon = drow.pop('lon')
		features.append(geoJsonFeature(i,lon,lat,drow))
		i += 1
	return geoJsonFeatCollection(features)

if __name__ == '__main__':
	print geoJsonPolygon('test',[[0,1],[5,9]])
