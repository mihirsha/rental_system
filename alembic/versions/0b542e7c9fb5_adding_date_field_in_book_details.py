"""adding date field in book details

Revision ID: 0b542e7c9fb5
Revises: 2cd861c55311
Create Date: 2023-05-12 11:03:10.782606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b542e7c9fb5'
down_revision = '2cd861c55311'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('book_details', column=sa.Column(
        'rented_day', sa.DateTime, nullable=True))
    op.add_column('book_details', column=sa.Column(
        'release_day', sa.DateTime, nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('book_details', 'rented_day')
    op.drop_column('book_details', 'release_day')
    pass
