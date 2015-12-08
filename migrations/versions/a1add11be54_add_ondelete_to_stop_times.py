"""add ondelete to stop_times

Revision ID: a1add11be54
Revises: 4121d141186e
Create Date: 2015-12-08 13:17:27.282257

"""

# revision identifiers, used by Alembic.
revision = 'a1add11be54'
down_revision = '4121d141186e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('stop_times_trip_id_fkey', 'stop_times', type_='foreignkey')
    op.create_foreign_key(None, 'stop_times', 'trips', ['trip_id'], ['trip_id'],
        onupdate="CASCADE", ondelete="CASCADE")


def downgrade():
    op.drop_constraint('stop_times_trip_id_fkey', 'stop_times', type_='foreignkey')
    op.create_foreign_key(None, 'stop_times', 'trips', ['trip_id'], ['trip_id'],
        onupdate="CASCADE")
