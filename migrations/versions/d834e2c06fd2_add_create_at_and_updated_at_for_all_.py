"""Add create_at and updated_at for all models

Revision ID: d834e2c06fd2
Revises: a657c709ec06
Create Date: 2024-12-02 21:56:46.597666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd834e2c06fd2'
down_revision: Union[str, None] = 'a657c709ec06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('candidate_courses', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('candidate_courses', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('candidates', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('candidates', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('courses', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('courses', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('manager_candidates', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('manager_candidates', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('offices', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('offices', sa.Column('updated_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('offices', 'updated_at')
    op.drop_column('offices', 'created_at')
    op.drop_column('manager_candidates', 'updated_at')
    op.drop_column('manager_candidates', 'created_at')
    op.drop_column('courses', 'updated_at')
    op.drop_column('courses', 'created_at')
    op.drop_column('candidates', 'updated_at')
    op.drop_column('candidates', 'created_at')
    op.drop_column('candidate_courses', 'updated_at')
    op.drop_column('candidate_courses', 'created_at')
    # ### end Alembic commands ###
