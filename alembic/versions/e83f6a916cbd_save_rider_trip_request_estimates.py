"""save rider trip request estimates

Revision ID: e83f6a916cbd
Revises: 843297615262
Create Date: 2020-06-04 09:05:45.419566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e83f6a916cbd'
down_revision = '843297615262'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('ride_request_estimates',
                    sa.Column('id', sa.String(36), primary_key=True),
                    sa.Column('created_at', sa.TIMESTAMP),
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
    op.drop_table('ride_request_estimates')
