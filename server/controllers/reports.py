#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, request, response, post, put, delete
# remove this global latter on
from server.transitfeededitor import tb

@route('/api/reports/unnamed')
def unnamed():
  response.content_type = 'text/plain'
  unnamed = tb.unnamedStops()
  result = 'There are '+str(len(unnamed))+' unnamed stops.\n'
  result += '\n'.join(unnamed)
  return result

@route('/api/reports/available')
def unnamed():
  response.content_type = 'text/plain'
  available = tb.availableStopIds()
  result = 'There are '+str(len(available))+' available stops ids.\n'
  result += '\n'.join(map(str,available))
  return result