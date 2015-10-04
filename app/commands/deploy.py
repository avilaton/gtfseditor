import logging

from flask.ext.migrate import upgrade
from flask.ext.script import Command, Option, prompt_pass, prompt

from app.models import Role
from app.models import User
from app import db

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

        admin_role = Role.query.filter_by(name='Administrator').one()
        admin_email = prompt('Admin email', default='admin@gtfseditor.com')
        admin = User(email=admin_email)
        admin.password = prompt_pass('Admin password')
        db.session.add(admin)
        db.session.commit()