"""initial

Revision ID: e4cc726ba51a
Revises: a58729e93e85
Create Date: 2024-12-13 11:16:11.970624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4cc726ba51a'
down_revision: Union[str, None] = 'a58729e93e85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
