
from flask.ext.script import Command, Option
from flask.ext.script.commands import InvalidCommand

from app.tasks import buildFeed

class BuildFeed(Command):
    """Builds a feed"""

    def get_options(self):
        return [
            Option('-v', '--validate', dest='validate', action="store_true", default=False),
            Option('-e', '--extract', dest='extract', action="store_true", default=False),
            Option('-u', '--upload', dest='upload', action="store_true", default=False)
        ]

    def run(self, validate=False, extract=False, upload=False):
        buildFeed.run(validate=validate, extract=extract, upload=upload)
