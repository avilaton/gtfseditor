# -*- coding: utf-8 -*-

from bottle import static_file, route

# @route('/:file#(favicon.ico|humans.txt)#')
# def favicon(file):
#   return static_file(file, root='project/static/misc')

# @route('/:path#(images|css|js|fonts)\/.+#')
# def server_static(path):
#   return static_file(path, root='project/static')

@route('/assets/<filepath:path>')
def server_files(filepath):
  return static_file(filepath, root='./assets/')

@route('/bower_components/<filepath:path>')
def server_files(filepath):
  return static_file(filepath, root='./bower_components/')

@route('/<filepath:path>')
def server_files(filepath):
  return static_file(filepath, root='./public/')

@route('/')
def index():
  return static_file('index.html', root='./public/')
