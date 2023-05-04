"""created book details table

Revision ID: 2a857a831f34
Revises: 0afb58dc25bc
Create Date: 2023-05-04 07:32:10.017771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a857a831f34'
down_revision = '0afb58dc25bc'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table('book_details',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('rental_price', sa.Integer(), nullable=False),
                    sa.Column('rental_period', sa.Integer(), nullable=False),
                    sa.Column('availability', sa.Boolean(),
                              nullable=False, default=False),
                    sa.Column('book_id', sa.Integer(),
                              nullable=False, unique=True),
                    )

    op.create_foreign_key(
        "fk_book_details_book",
        "book_details",
        "book",
        ["book_id"],
        ["id"],
    )
    pass


def downgrade() -> None:
    op.drop_constraint(u'fk_book_details_book',
                       'book_details', type_='foreignkey')
    op.drop_table('book_details')
    pass
