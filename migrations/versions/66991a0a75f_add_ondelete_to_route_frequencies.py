"""add ondelete to route_frequencies

Revision ID: 66991a0a75f
Revises: a1add11be54
Create Date: 2015-12-08 13:20:47.276469

"""

# revision identifiers, used by Alembic.
revision = '66991a0a75f'
down_revision = 'a1add11be54'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('route_frequencies_route_id_fkey', 'route_frequencies', type_='foreignkey')
    op.drop_constraint('route_frequencies_service_id_fkey', 'route_frequencies', type_='foreignkey')
    op.create_foreign_key(None, 'route_frequencies', 'routes', ['route_id'], ['route_id'],
        onupdate="CASCADE", ondelete="CASCADE")
    op.create_foreign_key(None, 'route_frequencies', 'calendar', ['service_id'], ['service_id'],
        onupdate="CASCADE", ondelete="CASCADE")


def downgrade():
    op.drop_constraint('route_frequencies_route_id_fkey', 'route_frequencies', type_='foreignkey')
    op.drop_constraint('route_frequencies_service_id_fkey', 'route_frequencies', type_='foreignkey')
    op.create_foreign_key(None, 'route_frequencies', 'routes', ['route_id'], ['route_id'],
        onupdate="CASCADE")
    op.create_foreign_key(None, 'route_frequencies', 'calendar', ['service_id'], ['service_id'],
        onupdate="CASCADE")
