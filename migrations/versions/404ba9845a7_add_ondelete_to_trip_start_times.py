"""add ondelete to trip start times

Revision ID: 404ba9845a7
Revises: 8d37ec247e2
Create Date: 2015-12-07 23:06:03.957129

"""

# revision identifiers, used by Alembic.
revision = '404ba9845a7'
down_revision = '8d37ec247e2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('trips_start_times_service_id_fkey', 'trips_start_times', type_='foreignkey')
    op.drop_constraint('trips_start_times_trip_id_fkey', 'trips_start_times', type_='foreignkey')
    op.create_foreign_key(None, 'trips_start_times', 'trips', ['trip_id'], ['trip_id'],
        onupdate="CASCADE", ondelete="CASCADE")
    op.create_foreign_key(None, 'trips_start_times', 'calendar', ['service_id'], ['service_id'],
        onupdate="CASCADE", ondelete="CASCADE")


def downgrade():
    op.drop_constraint('trips_start_times_service_id_fkey', 'trips_start_times', type_='foreignkey')
    op.drop_constraint('trips_start_times_trip_id_fkey', 'trips_start_times', type_='foreignkey')
    op.create_foreign_key(None, 'trips_start_times', 'trips', ['trip_id'], ['trip_id'],
        onupdate="CASCADE")
    op.create_foreign_key(None, 'trips_start_times', 'calendar', ['service_id'], ['service_id'],
        onupdate="CASCADE")
