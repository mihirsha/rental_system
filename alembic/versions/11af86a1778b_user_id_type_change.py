"""book id type change

Revision ID: 11af86a1778b
Revises: 0b542e7c9fb5
Create Date: 2023-05-29 11:26:00.452225

"""
from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision = '11af86a1778b'
down_revision = '0b542e7c9fb5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('book', sa.Column(
        'id', sa.UUID, primary_key=True, default=uuid.uuid4))
    pass


def downgrade() -> None:
    op.alter_column('book', sa.Column('id', sa.Integer, primary_key=True))
    pass
