# coding: utf-8


import json
import getpass
from client import Client

LOCAL = 'http://localhost:5000'
AUTAM = 'http://autam.herokuapp.com'
TPTMDZ = 'http://tptmdz.herokuapp.com'

origin = Client(AUTAM)
# origin_password = getpass.getpass()
# origin.login("admin@gtfseditor.com", origin_password)

dest = Client(LOCAL)
dest_password = getpass.getpass()
dest.login("admin@gtfseditor.com", dest_password)


def agencies():

    agency_map = {}

    agencies = origin.getList('/agency/')

    for from_agency in agencies:

        from_id = from_agency.pop('agency_id')

        response = dest.create('/agency/', from_agency)
        to_agency = response.json()

        to_id = to_agency['agency_id']

        agency_map.update({from_id: to_id})
        print "saved", from_id, to_id

    with open('agencies.json', 'w') as out:
        out.write(json.dumps(agency_map))

    return agency_map


if __name__ == '__main__':
    agency_map = agencies()
    dest.save_cj()

