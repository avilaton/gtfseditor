"""add ondelete to frequencies_trip_id_fkey

Revision ID: 4121d141186e
Revises: 9c7e1e3244a
Create Date: 2015-12-08 12:57:38.039284

"""

# revision identifiers, used by Alembic.
revision = '4121d141186e'
down_revision = '9c7e1e3244a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('frequencies_trip_id_fkey', 'frequencies', type_='foreignkey')
    op.create_foreign_key(None, 'frequencies', 'trips', ['trip_id'], ['trip_id'],
        onupdate="CASCADE", ondelete="CASCADE")


def downgrade():
    op.drop_constraint('frequencies_trip_id_fkey', 'frequencies', type_='foreignkey')
    op.create_foreign_key(None, 'frequencies', 'trips', ['trip_id'], ['trip_id'],
        onupdate="CASCADE")
