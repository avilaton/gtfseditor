# coding: utf-8

import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

import os
from glob import glob
import json
import getpass

from client import Client

LOCAL = 'http://localhost:5000'
AUTAM = 'http://autam.herokuapp.com'
TPTMDZ = 'http://tptmdz.herokuapp.com'


def dumpJson(obj):
    return json.dumps(obj, sort_keys=True, indent=4)


def pull(client, name, primary_key):
    logger.info("Pulling resource {0}".format(name))

    if not os.path.isdir('origin' + name):
        os.makedirs('origin' + name)

    for resource in client.getList(name):
        with open('origin' + name + str(resource.get(primary_key)) + '.json', 'w') as out:
            out.write(dumpJson(resource))
            logger.info("Saved {0}: {1}".format(name, resource.get(primary_key)))


def pullShapes(client):
    logger.info("Pulling shapes")

    primary_key = "shape_id"

    if not os.path.isdir('origin/shapes/'):
        os.makedirs('origin/shapes/')

    for resource in client.getList('/trips/'):
        trip = client.getOne('/trips/', resource.get('trip_id'), extension='')

        if not trip.get(primary_key):
            continue
        shape_id = str(trip.get(primary_key))
        with open('origin/shapes/' + shape_id + '.json', 'w') as out:
            try:
                shape = client.getOne('/shapes/', shape_id)
            except ValueError, e:
                logger.info('Shape not found')
                continue
            out.write(dumpJson(shape))
            logger.info("Saved {0}: {1}".format('shape', resource.get(primary_key)))


def pullStops(client):
    logger.info("Pulling stops")

    if not os.path.isdir('origin/stops/'):
        os.makedirs('origin/stops/')

    for stop in client.getList('/stops/', params={'limit': 3000}):
        stop_id = str(stop.get('stop_id'))
        with open('origin/stops/' + stop_id + '.json', 'w') as out:
            out.write(dumpJson(stop))
            logger.info("Saved {0}: {1}".format('stop', stop_id))


def push(client, name, primary_key, resource_mapping={}):
    logger.info("Pushing {0}".format(name))

    result_resource_map = {}
    resources = []

    for filename in glob('origin' + name + '*.json'):
        with open(filename) as inputFile:
            logger.info('Reading resource {0}'.format(filename))
            resources.append(json.loads(inputFile.read()))

    for original_resource in resources:

        original_res_id = original_resource.pop(primary_key)

        for key, mapping in resource_mapping.items():
            original_value = str(original_resource[key])
            if not original_resource[key]:
                continue

            logger.info("Mapping {name}{original_res_id}, {key} {original_value} --> {new_id}".\
                format(name=name,
                       key=key,
                       original_res_id=original_res_id,
                       original_value=original_value,
                       new_id=mapping[original_value]))
            original_resource[key] = mapping[original_value]

        response = client.create(name, original_resource)

        result_resource = response.json()
        result_resource_id = result_resource[primary_key]
        result_resource_map.update({original_res_id: result_resource_id})

        logger.info("Saved {0} to {1}".format(original_res_id, result_resource_id))

    with open('maps' + name[:-1] + '.json', 'w') as out:
        out.write(dumpJson(result_resource_map))


def getMap(name):

    with open('maps/' + name + '.json') as map_file:
        logger.info('Reading map {0}'.format(name))
        return json.loads(map_file.read())


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Push and pull resources from the gtfseditor API')

    parser.add_argument('action', help='either push or pull')
    parser.add_argument('resource', help='the resource you want to act on')

    args = parser.parse_args()

    if args.action in ["pull"]:

        with Client('autam', AUTAM) as client:

            if args.resource in ["agency"]:
                pull(client, '/agency/', 'agency_id')

            elif args.resource in ["routes"]:
                pull(client, '/routes/', 'route_id')

            elif args.resource in ["trips"]:
                pull(client, '/trips/', 'trip_id')

            elif args.resource in ["shapes"]:
                pullShapes(client)

            elif args.resource in ["stops"]:
                pullStops(client)

            elif args.resource in ["all"]:
                pull(client, '/agency/', 'agency_id')
                pull(client, '/routes/', 'route_id')
                pull(client, '/trips/', 'trip_id')
                pullShapes(client)
                pullStops(client)

            else:
                raise NotImplementedError

    elif args.action in ["push"]:

        with Client('local', LOCAL) as client:
            # client_password = getpass.getpass()
            # client.login("admin@gtfseditor.com", client_password)

            if args.resource in ["agency"]:
                push(client, '/agency/', 'agency_id')

            elif args.resource in ["stops"]:
                push(client, '/stops/', 'stop_id')

            elif args.resource in ["routes"]:
                agency_map = getMap('agency')
                push(client, '/routes/', 'route_id', resource_mapping={'agency_id': agency_map})

            elif args.resource in ["shapes"]:
                push(client, '/shapes/', 'shape_id')

            elif args.resource in ["trips"]:
                routes_map = getMap('routes')
                shapes_map = getMap('shapes')
                push(client, '/trips/', 'trip_id', resource_mapping={'route_id': routes_map,
                                                                     'shape_id': shapes_map})

            elif args.resource in ["all"]:
                push(client, '/agency/', 'agency_id')
                push(client, '/stops/', 'stop_id')
                push(client, '/shapes/', 'shape_id')

                agency_map = getMap('agency')
                push(client, '/routes/', 'route_id', resource_mapping={'agency_id': agency_map})

                routes_map = getMap('routes')
                shapes_map = getMap('shapes')
                push(client, '/trips/', 'trip_id', resource_mapping={'route_id': routes_map,
                                                                     'shape_id': shapes_map})

            else:
                raise NotImplementedError
    else:
        raise NotImplementedError

