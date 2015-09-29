
import os
import glob
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
        with open(self.destination + Model.__tablename__ + '.jsonl','wb') as output:
            for row in db.session.query(Model).all():
                output.write(json.dumps(row.to_json) + '\n')

class LoadData(Command):
    """Loads fixture data"""

    def get_options(self):
        return [
            Option('-o', '--origin', dest='origin', default='app/fixtures/'),
            Option('-m', '--modelname', dest='modelname')
        ]

    def run(self, origin, modelname=None):
        self.origin = origin
        Models = []
        if modelname:
            Model = globals()[modelname]
            Models.append(Model)
        else:
            for filename in glob.glob(self.origin + '*.jsonl'):
                modelname, ext = os.path.splitext(os.path.basename(filename))

            for table in db.metadata.sorted_tables:
                Model = get_class_by_tablename(table.name)
                if issubclass(Model, Entity) and Model is not Entity:
                    Models.append(Model)

        for Model in Models:
            self.import_model(Model)

    def import_model(self, Model):
        print("importing Model: {0}".format(Model.__tablename__))
        with open(self.origin + Model.__tablename__ + '.jsonl','rb') as inputfile:
            for line in inputfile:
                source = json.loads(line)
                model = Model(**source)
                db.session.add(model)
            db.session.commit()


Base = db.Model

def get_class_by_tablename(tablename):
  """Return class reference mapped to table.

  :param tablename: String with name of table.
  :return: Class reference or None.
  """
  for c in Base._decl_class_registry.values():
    if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
      return c