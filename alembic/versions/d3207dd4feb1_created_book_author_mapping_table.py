"""created book, author & mapping table

Revision ID: d3207dd4feb1
Revises: 5165b6582bf2
Create Date: 2023-05-02 15:34:17.668202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3207dd4feb1'
down_revision = '5165b6582bf2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('book',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=False),
                    sa.Column('description', sa.String, nullable=False))

    op.create_table('author',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('name', sa.String, nullable=False, unique=True))

    op.create_table('association_book_author',
                    sa.Column('book_id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('author_id', sa.Integer(), nullable=False))

    op.create_foreign_key(
        "fk_association_book",
        "association_book_author",
        "book",
        ["book_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_association_author",
        "association_book_author",
        "author",
        ["author_id"],
        ["id"],
    )

    # op.create_primary_key("pk_association_book_author",
    #                       "association_book_author", ["book_id", "author_id"])

    pass


def downgrade() -> None:
    op.drop_table('association_book_author')
    op.drop_table('author')
    op.drop_table('book')
    pass
