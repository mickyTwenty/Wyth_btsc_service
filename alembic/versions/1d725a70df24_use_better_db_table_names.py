"""use better db table names

Revision ID: 1d725a70df24
Revises: 59398d48ef19
Create Date: 2020-06-04 08:05:21.630878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d725a70df24'
down_revision = '59398d48ef19'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('rides', 'driver_rides')
    op.rename_table('ride_estimates', 'driver_ride_estimates')


def downgrade():
    op.rename_table('driver_rides', 'rides')
    op.rename_table('driver_ride_estimates', 'ride_estimates')
