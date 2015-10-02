import logging

from flask.ext.migrate import upgrade
from flask.ext.script import Command, Option

from app.models import Role

logger = logging.getLogger(__name__)

class Deploy(Command):
    """Run deployment tasks."""

    def get_options(self):
        return [
            Option('-a', '--addroles', dest='addroles', action="store_true", default=True),
        ]

    def run(self, addroles=True):
        # migrate database to latest revision
        logger.info('Upgrading DB')
        upgrade()

        if addroles:
            logger.info('Inserting Roles into DB')
            Role.insert_roles()
