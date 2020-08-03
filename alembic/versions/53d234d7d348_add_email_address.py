"""add email address

Revision ID: 53d234d7d348
Revises: e83f6a916cbd
Create Date: 2020-06-14 08:07:12.460147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53d234d7d348'
down_revision = 'e83f6a916cbd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('driver_rides', sa.Column('email', sa.String(50)))
    op.add_column('rider_rides', sa.Column('email', sa.String(50)))



def downgrade():
    op.drop_column('rider_rides', 'email')
    op.drop_column('driver_rides', 'email')
