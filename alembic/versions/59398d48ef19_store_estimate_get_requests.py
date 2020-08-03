"""store estimate get requests

Revision ID: 59398d48ef19
Revises: ca9e179f8c4a
Create Date: 2020-06-03 19:44:53.359079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59398d48ef19'
down_revision = 'ca9e179f8c4a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('ride_estimates',
                    sa.Column('id', sa.String(36), primary_key=True),
                    sa.Column('created_at', sa.TIMESTAMP),
                    sa.Column('home_city', sa.String(100)),
                    sa.Column('campus', sa.String(100)),
                    sa.Column('available_seats', sa.Integer),
                    sa.Column('total_miles', sa.Integer),
                    sa.Column('co2_emissions', sa.Integer),
                    sa.Column('driver_fare_low', sa.Float),
                    sa.Column('driver_fare_high', sa.Float),
                    sa.Column('donation', sa.Float),
                    sa.Column('wyth_fare', sa.Float),
                    sa.Column('src_raw_place', sa.JSON),
                    sa.Column('dst_raw_place', sa.JSON)
                    )


def downgrade():
    op.drop_table('ride_estimates')
