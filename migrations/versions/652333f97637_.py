"""empty message

Revision ID: 652333f97637
Revises: 7a73dfebd4b9
Create Date: 2024-12-09 01:26:32.085983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '652333f97637'
down_revision: Union[str, None] = '7a73dfebd4b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'refresh_tokens', ['token'])
    op.create_unique_constraint(None, 'users', ['refresh_token'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'refresh_tokens', type_='unique')
    # ### end Alembic commands ###