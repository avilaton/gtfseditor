#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom import minidom

class Kml(object):
	"""docstring for kml"""
	def __init__(self, filename):
		self.filename = filename
		self.dom = minidom.parse(self.filename)
		self.collections = {}
		self.placemarks = []

	def findPlacemarks(self):
		for node in self.dom.getElementsByTagName("Placemark"):
			placemark = {}
			placemark['name'] = node.getElementsByTagName('name')[0].firstChild.wholeText
			description = node.getElementsByTagName('description')
			if description.length:
				placemark['description'] = description[0].firstChild.wholeText
			point = node.getElementsByTagName('Point')[0]
			coords = point.getElementsByTagName('coordinates')[0].firstChild.wholeText
			lon, lat, alt = map(float, coords.split(','))
			placemark['lat'] = float(lat)
			placemark['lon'] = float(lon)
			placemark['alt'] = alt
			self.placemarks.append(placemark)

	def findTag(self, tagName):
		self.collections[tagName] = self.doc.getElementsByTagName(tagName)