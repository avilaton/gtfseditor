
import os
import logging
import glob
import inspect
import json
from flask_script import Command, Option

from app.models import *
from app.models.base import Base
from app import db

logger = logging.getLogger(__name__)

class DumpData(Command):
    """Dumps fixture data"""

    def get_options(self):
        return [
            Option('-d', '--destination', dest='destination', default='app/fixtures/'),
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
                    if issubclass(item, GTFSBase) and item is not GTFSBase:
                        self.export_model(item)

    def export_model(self, Model):
        logger.info("exporting Model: {0}".format(Model.__tablename__))
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

    def run(self, origin='app/fixtures/', modelname=None):
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
                if Model and issubclass(Model, GTFSBase) and Model is not GTFSBase:
                    Models.append(Model)

        for Model in Models:
            self.import_model(Model)

        # update sequences to their max values.
        # https://wiki.postgresql.org/wiki/Fixing_Sequences
        logger.info("Updating primary key sequences")
        statements = db.session.execute("""
                SELECT 'SELECT SETVAL(' ||
                       quote_literal(quote_ident(PGT.schemaname) || '.' || quote_ident(S.relname)) ||
                       ', COALESCE(MAX(' ||quote_ident(C.attname)|| '), 1) ) FROM ' ||
                       quote_ident(PGT.schemaname)|| '.'||quote_ident(T.relname)|| ';'
                FROM pg_class AS S,
                     pg_depend AS D,
                     pg_class AS T,
                     pg_attribute AS C,
                     pg_tables AS PGT
                WHERE S.relkind = 'S'
                    AND S.oid = D.objid
                    AND D.refobjid = T.oid
                    AND D.refobjid = C.attrelid
                    AND D.refobjsubid = C.attnum
                    AND T.relname = PGT.tablename
                ORDER BY S.relname;""")
        for stmt in statements:
            db.session.execute(stmt[0])

    def import_model(self, Model):
        logger.info("importing Model: {0}".format(Model.__tablename__))

        with open(self.origin + Model.__tablename__ + '.jsonl','rb') as inputfile:
            for line in inputfile:
                source = json.loads(line)
                model = Model(**source)
                db.session.add(model)

        db.session.commit()


def get_class_by_tablename(tablename):
  """Return class reference mapped to table.

  :param tablename: String with name of table.
  :return: Class reference or None.
  """
  for c in Base._decl_class_registry.values():
    if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
      return c