"""first btsc database

Revision ID: 72cb40fcf785
Revises: 
Create Date: 2020-06-03 12:22:15.218824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72cb40fcf785'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('rides',
                    sa.Column('id', sa.String(36), primary_key=True),
                    sa.Column('created_at', sa.TIMESTAMP),
                    sa.Column('driver_name', sa.String(50)),
                    sa.Column('home_city', sa.String(100)),
                    sa.Column('campus', sa.String(100)),
                    sa.Column('available_seats', sa.Integer),
                    sa.Column('total_miles', sa.Integer),
                    sa.Column('co2_emissions', sa.Integer),
                    sa.Column('driver_fare', sa.Float),
                    sa.Column('donation', sa.Float),
                    sa.Column('wyth_fare', sa.Float)
                    )

def downgrade():
    op.drop_table('riders')
