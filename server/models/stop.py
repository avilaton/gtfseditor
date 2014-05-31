#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, Sequence, String, Float
from server import Base

class Stop(Base):
  __tablename__ = 'stops'
  stop_id = Column(Integer, Sequence('id_seq'), primary_key=True)
  stop_code = Column(String(50))
  stop_desc = Column(String(50))
  stop_name = Column(String(50))
  stop_lat = Column(Float(precision=64))
  stop_lon = Column(Float(precision=64))
  stop_calle = Column(String(50))
  stop_numero = Column(String(50))
  stop_entre = Column(String(50))
  stop_esquina = Column(String(50))

  def __repr__(self):
    return "<Stop: '%s' (lat:'%s', lon:'%s')>" % (self.stop_id, 
      self.stop_lat, self.stop_lon)

  @property
  def as_dict(self):
    d = {}
    for column in self.__table__.columns:
      d[column.name] = unicode(getattr(self, column.name))
    return d



import server.geojson as geojson

current_db = ''

class StopOld(object):
  """docstring for stops"""
  db = current_db

  def __init__(self):
    self.db = current_db

  def update(self, stop_id, data):
    """ Stub - should carry out a full update, only updates stop_calle"""
    p = {'stop_id': stop_id}
    p['stop_calle'] = data['properties']['stop_calle'].encode('utf-8')
    p['stop_lon'] = data['geometry']['coordinates'][0]
    p['stop_lat'] = data['geometry']['coordinates'][1]
    result = self.db.query("""UPDATE stops 
      SET stop_calle='{stop_calle}', 
        stop_lat='{stop_lat}', stop_lon='{stop_lon}'
      WHERE stop_id='{stop_id}'"""
      .format(**p))
    self.db.connection.commit()
    return {'success': True, 'result': p}

  def delete(self, stop_id):
    """Deletes a stop by stop_id"""
    result = self.db.query("""DELETE FROM stops WHERE stop_id='{stop_id}'"""
      .format(stop_id=stop_id))
    self.db.connection.commit()
    return {'success': True, 'result': result}

  @classmethod
  def all(cls):
    stops = []
    cls.db.query("""SELECT * FROM stops WHERE stop_id IN 
      (SELECT DISTINCT stop_id FROM stop_seq)""")
    for r in cls.db.cursor.fetchall():
      stops.append(dict(r))
    return stops

  @classmethod
  def bbox(cls, bbox, filterQ):
    w,s,e,n = map(float,bbox.split(','))
    q = ["""SELECT * 
        FROM stops s INNER JOIN stop_seq sq ON s.stop_id=sq.stop_id
        WHERE
          (stop_lat BETWEEN {s} AND {n})
          AND 
          (stop_lon BETWEEN {w} AND {e}) """]

    if filterQ:
      if 'id:' in filterQ:
        stop_id = filterQ.split(':')[1]
        q.append("""AND s.stop_id='{f}'""")
        q.append("LIMIT 300")
        query = ''.join(q).format(s=s,n=n,w=w,e=e, f=stop_id)
      elif 'calle:' in filterQ:
        stop_calle = filterQ.split(':')[1]
        q.append("""AND s.stop_calle LIKE '%{f}%'""")
        q.append("LIMIT 300")
        query = ''.join(q).format(s=s,n=n,w=w,e=e, f=stop_calle)
      else:
        q.append("""AND s.stop_calle LIKE '%{f}%'""")
        q.append("LIMIT 300")
        query = ''.join(q).format(s=s,n=n,w=w,e=e, f=filterQ)
    else:
      q.append("LIMIT 300")
      query = ''.join(q).format(s=s,n=n,w=w,e=e)
    cls.db.query(query)

    d = {}
    for r in cls.db.cursor.fetchall():
      stop = dict(r)
      linea = stop.pop('trip_id')
      stop_id = stop.pop('stop_id')
      if stop_id in d:
        d[stop_id]['lineas'].append(linea)
      else:
        d[stop_id] = stop
        d[stop_id]['lineas'] = [linea]
    
    features = []
    for stop_id,stop in d.items():
      f = geojson.geoJsonFeature(stop_id,
        stop['stop_lon'],
        stop['stop_lat'],
        {'stop_id':stop_id,
        'stop_lineas':stop['lineas'],
        'stop_calle':stop['stop_calle'],
        'stop_numero':stop['stop_numero'],
        'stop_esquina':stop['stop_esquina'],
        'stop_entre':stop['stop_entre']})
      features.append(f)
    return geojson.geoJsonFeatCollection(features)

  @classmethod
  def find(cls, stop_id):
    data = cls.db.select('stops',stop_id=stop_id)
    if data:
      stop = data[0]
      l = db.select('stop_seq',stop_id=stop_id)
      lineas = [t['trip_id'] for t in l]
      f = geojson.geoJsonFeature(stop_id,
        stop['stop_lon'], stop['stop_lat'],
        {'stop_id':stop_id,
        'stop_lineas':lineas,
        'stop_calle':stop['stop_calle'],
        'stop_numero':stop['stop_numero'],
        'stop_esquina':stop['stop_esquina'],
        'stop_entre':stop['stop_entre']})
      response = geojson.geoJsonFeatCollection([f])
    else:
      response = {'success': False}
    return response

  @classmethod
  def unnamed(cls):
    cls.db.query("""SELECT stop_id FROM stops 
      WHERE 
        stop_id IN (SELECT DISTINCT stop_id FROM stop_seq) 
      AND stop_calle=''""")
    return [dict(r) for r in cls.db.cursor.fetchall()]

  @classmethod
  def availableIds(cls):
    cls.db.query("""SELECT stop_id FROM stops""")
    allIds = set(range(1,10000))
    usedIds = [int(r['stop_id']) for r in cls.db.cursor.fetchall()]
    availableIds = allIds.difference(usedIds)
    return availableIds