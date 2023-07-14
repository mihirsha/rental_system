"""created map between user and books

Revision ID: 3ab9bf6a32a8
Revises: d3207dd4feb1
Create Date: 2023-05-03 13:01:53.537384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ab9bf6a32a8'
down_revision = 'd3207dd4feb1'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column('book', sa.Column('user_id', sa.UUID()))

    op.create_foreign_key(
        "fk_book_user",
        "book",
        "user",
        ["user_id"],
        ["id"],
    )
    pass


def downgrade() -> None:
    op.drop_constraint(u'fk_book_user', 'book', type_='foreignkey')
    op.drop_column('book', 'user_id')
    pass
