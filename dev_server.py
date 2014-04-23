#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from server import transitfeededitor as tfe
from bottle import debug, run

debug(True)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    run(tfe.app, reloader=True, host='0.0.0.0', port=port)
