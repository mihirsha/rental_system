"""created user table

Revision ID: 5165b6582bf2
Revises: 1c754c5d720d
Create Date: 2023-05-02 11:18:59.696777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5165b6582bf2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table('user',
                    sa.Column('id', sa.UUID(),
                              nullable=False, primary_key=True),
                    sa.Column('email', sa.String, nullable=False, unique=True),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('name', sa.String, nullable=False),
                    sa.Column('phoneNumber', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('user')
    pass
