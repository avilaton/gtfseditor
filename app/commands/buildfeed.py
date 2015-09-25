
from flask.ext.script import Command, Option
from flask.ext.script.commands import InvalidCommand

from app.tasks import buildFeed

class BuildFeed(Command):
    """Builds a feed"""

    def get_options(self):
        return [
            Option('-v', '--validate', dest='validate'),
            Option('-e', '--extract', dest='extract'),
            Option('-u', '--upload', dest='upload')
        ]

    def run(self, validate=False, extract=False, upload=False):
        buildFeed.run(validate=validate, extract=extract, upload=upload)
