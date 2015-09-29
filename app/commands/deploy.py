
from flask.ext.migrate import upgrade
from flask.ext.script import Command, Option

from app.models import Role


class Deploy(Command):
    """Run deployment tasks."""

    def get_options(self):
        return [
            Option('-a', '--addroles', dest='addroles', action="store_true", default=False),
        ]

    def run(self, addroles=False):
        # migrate database to latest revision
        upgrade()

        if addroles:
            Role.insert_roles()
