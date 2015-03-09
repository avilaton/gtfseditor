#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import StringIO

class DictUnicodeProxy(object):
  def __init__(self, d):
    self.d = d
  def __iter__(self):
    return self.d.__iter__()
  def get(self, item, default=None):
    i = self.d.get(item, default)
    if isinstance(i, unicode):
      return i.encode('utf-8')
    return i

def to_csv(listOfObjects):
  rows = []
  fieldnames = None

  fieldnames = list(set(route.as_dict.keys() + trip.as_dict.keys())) + ['length']

  for route, trip in result:
    row = route.as_dict
    row.update(trip.as_dict)
    rows.append(row)

  fout = StringIO.StringIO()
  writer = csv.DictWriter(fout, fieldnames=fieldnames)
  writer.writeheader()

  for row in rows:
    length = db.query(func.max(StopSeq.shape_dist_traveled)).filter_by(trip_id=row['trip_id']).one()
    row.update({'length': length[0]})
    writer.writerow(DictUnicodeProxy(row))

  return fout.getvalue()
