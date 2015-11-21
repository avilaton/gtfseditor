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

    def login(self, email, password):
        self.session.get(self.url + '/auth/login')
        self.session.post(self.url + '/auth/login', data={"email": email, "password": password})

    def getList(self, resource):
        response = self.session.get(self.api + resource)
        return response.json()

    def getOne(self, resource, id):
        response = self.session.get(self.api + resource + str(id) + '.json')
        return response.json()

    def create(self, resource, payload):
        return self.session.post(self.api + resource, json=payload)

    def save_cj(self):
        self.cj.save(ignore_discard=True)

    def pull(self, name, primary_key):
        logger.info("Pulling resource {0}".format(name))

        if not os.path.isdir('origin' + name):
            os.makedirs('origin' + name)

        for resource in self.getList(name):
            with open('origin' + name + str(resource.get(primary_key)) + '.json', 'w') as out:
                out.write(dumpJson(resource))
                logger.info("Saved {0}: {1}".format(name, resource.get(primary_key)))

    def pullShapes(self):
        logger.info("Pulling shapes")

        primary_key = "shape_id"

        if not os.path.isdir('origin/shapes/'):
            os.makedirs('origin/shapes/')

        for resource in self.getList('/trips/'):
            trip = self.getOne('/trips/', resource.get('trip_id'))
            print trip
            shape_id = str(trip.get(primary_key))
            with open('origin/shapes/' + shape_id + '.json', 'w') as out:
                self.getOne('/shapes/', shape_id)
                out.write(dumpJson(resource))
                logger.info("Saved {0}: {1}".format(name, resource.get(primary_key)))

    def push(self, name, primary_key):
        logger.info("Pushing {0}".format(name))

        resource_map = {}
        resources = []

        for filename in glob('origin' + name + '*.json'):
            with open(filename) as inputFile:
                resources.append(json.loads(inputFile.read()))
                logger.info('Read resource {0}'.format(filename))

        for from_resource in resources:

            from_id = from_resource.pop(primary_key)

            response = self.create(name, from_resource)
            to_resource = response.json()

            to_id = to_resource[primary_key]

            resource_map.update({from_id: to_id})
            logger.info("Saved {0} to {1}".format(from_id, to_id))

        with open('maps' + name[:-1] + '.json', 'w') as out:
            out.write(dumpJson(resource_map))

        return resource_map

