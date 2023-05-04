"""created review table and map btw review and user

Revision ID: 36516f6230a0
Revises: 2a857a831f34
Create Date: 2023-05-04 10:14:01.085234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36516f6230a0'
down_revision = '2a857a831f34'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('review',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('review', sa.String(), nullable=False)
                    )

    op.create_foreign_key(
        "fk_review_user",
        "review",
        "user",
        ["user_id"],
        ["id"],
    )
    pass


def downgrade() -> None:

    op.drop_constraint(u'fk_review_user',
                       'review', type_='foreignkey')
    op.drop_table('review')
    pass
