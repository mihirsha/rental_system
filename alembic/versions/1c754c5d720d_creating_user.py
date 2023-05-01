"""creating user

Revision ID: 1c754c5d720d
Revises: 
Create Date: 2023-05-01 16:26:15.938255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c754c5d720d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('user', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('email', sa.String, nullable=False, unique=True), sa.Column('password', sa.String, nullable=False), sa.Column('name', sa.String, nullable=False), sa.Column('phoneNumber', sa.Integer, nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('user')
    pass
