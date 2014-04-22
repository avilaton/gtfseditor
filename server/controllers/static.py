# -*- coding: utf-8 -*-

from bottle import static_file, route


@route('/:file#(favicon.ico|humans.txt)#')
def favicon(file):
    return static_file(file, root='project/static/misc')


@route('/:path#(images|css|js|fonts)\/.+#')
def server_static(path):
    return static_file(path, root='project/static')