#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'sqlite:///database/1.0.9.sqlite'
# DATABASE_URL = 'sqlite:///:memory:'
DEBUG = True

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=DEBUG)

from server.models import *

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
db = Session()

import unittest

class tripModelTest(unittest.TestCase):
	def testData(self):
		trip_id = '18.ida'
		sequence = db.query(Stop).join(StopSeq, Stop.stop_id == StopSeq.stop_id)\
			.filter(StopSeq.trip_id == trip_id)\
			.order_by(StopSeq.stop_sequence).all()
		self.assertEqual(1,1)

	def testGeoJSON(self):
		trip_id = '18.ida'
		rows = db.query(Stop, StopSeq).join(StopSeq, Stop.stop_id == StopSeq.stop_id)\
			.filter(StopSeq.trip_id == trip_id)\
			.order_by(StopSeq.stop_sequence).all()

		from server import geojson
		features = []

		for row in rows:
			stop = row.Stop
			stop_seq = row.StopSeq
			properties = stop.as_dict
			properties.update({'stop_seq': stop_seq.stop_sequence})
			f = geojson.feature(id = stop.stop_id,
				coords = [stop.stop_lon, stop.stop_lat], 
				properties = properties)
			features.append(f)
		print geojson.featureCollection(features)

if __name__ == '__main__':
    unittest.main()