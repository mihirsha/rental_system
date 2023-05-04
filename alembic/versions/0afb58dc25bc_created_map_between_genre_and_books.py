"""created map between genre and books

Revision ID: 0afb58dc25bc
Revises: 3ab9bf6a32a8
Create Date: 2023-05-03 17:38:56.966896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0afb58dc25bc'
down_revision = '3ab9bf6a32a8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('genre',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('name', sa.String, nullable=False, unique=True))

    op.create_table('association_book_genre',
                    sa.Column('book_id', sa.Integer(),
                              nullable=False),
                    sa.Column('genre_id', sa.Integer(), nullable=False))

    op.create_foreign_key(
        "fk_association_book",
        "association_book_genre",
        "book",
        ["book_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_association_genre",
        "association_book_genre",
        "genre",
        ["genre_id"],
        ["id"],
    )
    pass


def downgrade() -> None:

    op.drop_constraint(u'fk_association_book',
                       'association_book_genre', type_='foreignkey')
    op.drop_constraint(u'fk_association_genre',
                       'association_book_genre', type_='foreignkey')
    op.drop_table('association_book_genre')
    op.drop_table('genre')
    pass
