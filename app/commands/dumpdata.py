
import inspect
import json
from flask.ext.script import Command, Option

from app.models import *
from app.models.entity import Entity
from app import db


class DumpData(Command):
    """Dumps fixture data"""

    def get_options(self):
        return [
            Option('-d', '--destination', dest='destination', default='./'),
            Option('-m', '--modelname', dest='modelname')
        ]

    def run(self, destination, modelname=None):
        self.destination = destination

        if modelname:
            Model = globals()[modelname]
            self.export_model(Model)
        else:
            for item in globals().values():
                if inspect.isclass(item):
                    if issubclass(item, Entity) and item is not Entity:
                        self.export_model(item)

    def export_model(self, Model):
        with open(self.destination + Model.__tablename__ + '.jsonlines','wb') as output:
            for row in db.session.query(Model).all():
                output.write(json.dumps(row.to_json) + '\n')
