"""created cart table and established mapping

Revision ID: 2cd861c55311
Revises: 48afbc0151d0
Create Date: 2023-05-04 13:05:18.565594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cd861c55311'
down_revision = '48afbc0151d0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('cart',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('rental_period', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer()),
                    sa.Column('book_id', sa.Integer())
                    )

    op.create_foreign_key(
        "fk_cart_user",
        "cart",
        "user",
        ["user_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_cart_book",
        "cart",
        "book",
        ["book_id"],
        ["id"],
    )
    pass


def downgrade() -> None:
    op.drop_constraint('fk_cart_user', 'cart', type_='foreignkey')
    op.drop_constraint('fk_cart_book', 'cart', type_='foreignkey')
    op.drop_table('cart')
    pass
