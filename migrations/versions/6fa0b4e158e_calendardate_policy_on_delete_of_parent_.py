"""CalendarDate policy on delete of parent Calendar

Revision ID: 6fa0b4e158e
Revises: 4e04a592b373
Create Date: 2015-10-08 00:37:36.131004

"""

# revision identifiers, used by Alembic.
revision = '6fa0b4e158e'
down_revision = '4e04a592b373'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('calendar_dates_service_id_fkey', 'calendar_dates', type_='foreignkey')
    op.create_foreign_key(None, 'calendar_dates', 'calendar', ['service_id'], ['service_id'],
    	onupdate="CASCADE", ondelete="CASCADE")


def downgrade():
    op.drop_constraint('calendar_dates_service_id_fkey', 'calendar_dates', type_='foreignkey')
    op.create_foreign_key(None, 'calendar_dates', 'agency', ['service_id'], ['service_id'])
