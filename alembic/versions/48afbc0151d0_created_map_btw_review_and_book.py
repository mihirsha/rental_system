"""created map btw review and book

Revision ID: 48afbc0151d0
Revises: 36516f6230a0
Create Date: 2023-05-04 10:24:39.241530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48afbc0151d0'
down_revision = '36516f6230a0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('review', sa.Column('book_id', sa.UUID(), nullable=False))
    op.create_foreign_key(
        "fk_book_review",
        "review",
        "book",
        ["book_id"],
        ["id"],
    )
    pass


def downgrade() -> None:
    op.drop_constraint('fk_book_review', 'review', type_='foreignkey')
    op.drop_column('review', 'book_id')
    pass
