"""add contact us table

Revision ID: 8c29becf9fa4
Revises: 53d234d7d348
Create Date: 2020-06-21 11:11:58.906978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c29becf9fa4'
down_revision = '53d234d7d348'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('contact_us',
                    sa.Column('id', sa.String(36), primary_key=True),
                    sa.Column('created_at', sa.TIMESTAMP),
                    sa.Column('name', sa.String(100)),
                    sa.Column('email', sa.String(100)),
                    sa.Column('subject', sa.String(100)),
                    sa.Column('message', sa.Text),
                    )


def downgrade():
    op.drop_table('contact_us')