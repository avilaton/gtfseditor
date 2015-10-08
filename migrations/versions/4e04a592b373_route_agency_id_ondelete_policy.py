"""route_agency_id ondelete policy

Revision ID: 4e04a592b373
Revises: 10d8e7a6ebe9
Create Date: 2015-10-07 23:19:17.844566

"""

# revision identifiers, used by Alembic.
revision = '4e04a592b373'
down_revision = '10d8e7a6ebe9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('routes_agency_id_fkey', 'routes', type_='foreignkey')
    op.create_foreign_key(None, 'routes', 'agency', ['agency_id'], ['agency_id'],
    	onupdate="CASCADE", ondelete="SET NULL")

def downgrade():
    op.drop_constraint('routes_agency_id_fkey', 'routes', type_='foreignkey')
    op.create_foreign_key(None, 'routes', 'agency', ['agency_id'], ['agency_id'])
