#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, request, response, view
from server.models import Stop

@route('/api/reports/unnamed')
@view('unnamed')
def unnamed():
  unnamed = Stop.unnamed()
  return dict(stops=unnamed)

@route('/api/reports/available')
@view('available')
def unnamed():
  available = Stop.availableIds()
  return dict(available=available)