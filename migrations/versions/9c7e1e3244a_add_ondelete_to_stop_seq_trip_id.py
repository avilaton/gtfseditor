"""add ondelete to stop_seq trip_id

Revision ID: 9c7e1e3244a
Revises: 404ba9845a7
Create Date: 2015-12-08 11:53:22.992498

"""

# revision identifiers, used by Alembic.
revision = '9c7e1e3244a'
down_revision = '404ba9845a7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('stop_seq_trip_id_fkey', 'stop_seq', type_='foreignkey')
    op.create_foreign_key(None, 'stop_seq', 'trips', ['trip_id'], ['trip_id'],
        onupdate="CASCADE", ondelete="CASCADE")


def downgrade():
    op.drop_constraint('stop_seq_trip_id_fkey', 'stop_seq', type_='foreignkey')
    op.create_foreign_key(None, 'stop_seq', 'trips', ['trip_id'], ['trip_id'],
        onupdate="CASCADE")
