"""store raw place detail for src/dst

Revision ID: ca9e179f8c4a
Revises: 463c94d2a300
Create Date: 2020-06-03 19:22:22.833560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca9e179f8c4a'
down_revision = '463c94d2a300'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('rides', sa.Column('src_raw_place', sa.JSON))
    op.add_column('rides', sa.Column('dst_raw_place', sa.JSON))


def downgrade():
    op.drop_column('rides', 'src_raw_place')
    op.drop_column('rides', 'dst_raw_place')
