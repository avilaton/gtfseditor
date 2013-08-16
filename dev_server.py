#!/usr/bin/python
# -*- coding: utf-8 -*-

from server import transitfeededitor as tfe

if __name__ == "__main__":
    tfe.app.run(host='localhost', port=8080, debug=True, reloader=True)
