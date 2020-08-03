"""add rider trip requests

Revision ID: 843297615262
Revises: 1d725a70df24
Create Date: 2020-06-04 08:24:52.721321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '843297615262'
down_revision = '1d725a70df24'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('rider_rides',
                    sa.Column('id', sa.String(36), primary_key=True),
                    sa.Column('created_at', sa.TIMESTAMP),
                    sa.Column('rider_name', sa.String(50)),
                    sa.Column('home_city', sa.String(100)),
                    sa.Column('campus', sa.String(100)),
                    sa.Column('total_miles', sa.Integer),
                    sa.Column('co2_emissions', sa.Integer),
                    sa.Column('rider_offer_low', sa.Float),
                    sa.Column('rider_offer_high', sa.Float),
                    sa.Column('donation', sa.Float),
                    sa.Column('src_raw_place', sa.JSON),
                    sa.Column('dst_raw_place', sa.JSON)
                    )
def downgrade():
    op.drop_table('rider_rides')
