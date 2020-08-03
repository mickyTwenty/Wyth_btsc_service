"""handle low/high for estimates

Revision ID: 463c94d2a300
Revises: 72cb40fcf785
Create Date: 2020-06-03 15:01:42.248705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '463c94d2a300'
down_revision = '72cb40fcf785'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('rides', 'driver_fare')
    op.add_column('rides', sa.Column('driver_fare_low', sa.Float))
    op.add_column('rides', sa.Column('driver_fare_high', sa.Float))


def downgrade():
    op.drop_column('rides', 'driver_fare_low')
    op.drop_column('rides', 'driver_fare_high')
    op.add_column('rides', sa.Column('driver_fare', sa.Float))


