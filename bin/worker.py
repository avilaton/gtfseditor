# coding: utf-8

import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

import getpass

from client import Client

LOCAL = 'http://localhost:5000'
AUTAM = 'http://autam.herokuapp.com'
TPTMDZ = 'http://tptmdz.herokuapp.com'


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Push and pull resources from the gtfseditor API')

    parser.add_argument('action', help='either push or pull')
    parser.add_argument('resource', help='the resource you want to act on')

    args = parser.parse_args()

    if args.action in ["pull"]:

        origin = Client('autam', AUTAM)
        if args.resource in ["agency"]:
            origin.pull('/agency/', 'agency_id')
        elif args.resource in ["routes"]:
            origin.pull('/routes/', 'route_id')
        elif args.resource in ["trips"]:
            origin.pull('/trips/', 'trip_id')
        elif args.resource in ["shapes"]:
            origin.pullShapes()
        else:
            raise NotImplementedError
    elif args.action in ["push"]:

        dest = Client('local', LOCAL)
        dest_password = getpass.getpass()
        dest.login("admin@gtfseditor.com", dest_password)
        if args.resource in ["agency"]:
            dest.push('/agency/', 'agency_id')
        else:
            raise NotImplementedError

        dest.save_cj()
    else:
        raise NotImplementedError

