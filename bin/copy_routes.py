# coding: utf-8


import json
import getpass
from client import Client

LOCAL = 'http://localhost:5000'
AUTAM = 'http://autam.herokuapp.com'
TPTMDZ = 'http://tptmdz.herokuapp.com'

origin = Client(AUTAM)


dest = Client(LOCAL)
dest_password = getpass.getpass()
dest.login("admin@gtfseditor.com", dest_password)


def routes(agencies_map):

    routes_map = {}

    routes = origin.getList('/routes/')

    for from_route in routes:

        from_id = from_route.pop('route_id')

        new_agency_id = agencies_map[str(from_route['agency_id'])]

        from_route.update({"agency_id": new_agency_id})

        response = dest.create('/routes/', from_route)
        to_agency = response.json()

        to_id = to_agency['agency_id']

        routes_map.update({from_id: to_id})
        print "saved", from_id, to_id

    with open('routes.json', 'w') as out:
        out.write(json.dumps(routes_map))

    return routes_map


if __name__ == '__main__':
    with open('agencies.json') as inFile:
        agencies_map = json.loads(inFile.read())

    routes(agencies_map)
    dest.save_cj()
