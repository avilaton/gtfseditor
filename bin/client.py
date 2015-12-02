import os
from glob import glob
import json
import logging
import requests
import cookielib

logger = logging.getLogger(__name__)

def dumpJson(obj):
    return json.dumps(obj, sort_keys=True, indent=4)


class Client(object):

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.api = url + '/api'

        self.cookie_file = './cookie-' + self.name
        logger.info("testing")
        self.cj = cookielib.LWPCookieJar(self.cookie_file)
        try:
            self.cj.load()
        except:
            pass

        self.session = requests.Session()
        self.session.cookies = self.cj

    def __enter__(self):
        try:
            self.cj.load()
        except:
            pass
        self.session = requests.Session()
        self.session.cookies = self.cj
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cj.save(ignore_discard=True)

    def login(self, email, password):
        self.session.get(self.url + '/auth/login')
        self.session.post(self.url + '/auth/login', data={"email": email, "password": password})

    def getList(self, resource, params=None):
        response = self.session.get(self.api + resource, params=params)
        return response.json()

    def getOne(self, resource, id, extension='.json'):
        response = self.session.get(self.api + resource + str(id) + extension)
        if response.ok:
            return response.json()
        else:
            raise ValueError('Not Found')

    def create(self, resource, payload):
        return self.session.post(self.api + resource, json=payload)
