# coding: utf-8

import getpass
import json
from glob import glob

from client import Client

import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

LOCAL = 'http://localhost:5000'
AUTAM = 'http://autam.herokuapp.com'
TPTMDZ = 'http://tptmdz.herokuapp.com'

origin = Client('autam', AUTAM)


dest = Client('local', LOCAL)
dest_password = getpass.getpass()
dest.login("admin@gtfseditor.com", dest_password)


def dumpJson(obj):
    return json.dumps(obj, sort_keys=True, indent=4)


def pullAgencies():
    logger.info("Pulling agencies")

    for resource in origin.getList('/agency/'):
        with open('origin/agencies/' + str(resource.get('agency_id')) + '.json', 'w') as out:
            out.write(dumpJson(resource))
            logger.info("saved agency_id: {0}".format(resource.get('agency_id')))


def pushAgencies():
    logger.info("Pushing agencies")

    agency_map = {}
    agencies = []

    for filename in glob('origin/agencies/*.json'):
        with open(filename) as inputFile:
            agencies.append(json.loads(inputFile.read()))


    for from_agency in agencies:

        from_id = from_agency.pop('agency_id')

        response = dest.create('/agency/', from_agency)
        to_agency = response.json()

        to_id = to_agency['agency_id']

        agency_map.update({from_id: to_id})
        logger.info("saved {0} to {1}".format(from_id, to_id))

    with open('maps/agencies.json', 'w') as out:
        out.write(dumpJson(agency_map))

    return agency_map

    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Push and pull resources from the gtfseditor API')

    parser.add_argument('action', help='either push or pull')
    parser.add_argument('resource', help='the resource you want to act on')

    args = parser.parse_args()


    if args.action in ["pull"]:
        if args.resource in ["agencies"]:
            pullAgencies()
        else:
            print "not implemented"
    elif args.action in ["push"]:
        if args.resource in ["agencies"]:
            pushAgencies()
        else:
            raise NotImplementedError
    else:
        raise NotImplementedError

    dest.save_cj()
