"""refresh_tokens table init

Revision ID: 7a73dfebd4b9
Revises: 3de886c1a49f
Create Date: 2024-12-09 00:57:48.743389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a73dfebd4b9'
down_revision: Union[str, None] = '3de886c1a49f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('refresh_tokens',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('token', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users', sa.Column('refresh_token', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'users', 'refresh_tokens', ['refresh_token'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'refresh_token')
    op.drop_table('refresh_tokens')
    # ### end Alembic commands ###