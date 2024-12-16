"""Initial commit

Revision ID: 72adc734b61f
Revises:
Create Date: 2024-12-13 19:21:50.615727

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "72adc734b61f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "admins",
        sa.Column("is_superadmin", sa.Boolean(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("password", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "candidates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("photo", sa.String(length=255), nullable=True),
        sa.Column("full_name", sa.String(length=100), nullable=True),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("location", sa.String(length=100), nullable=True),
        sa.Column("resume", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=100), nullable=True),
        sa.Column("is_hired", sa.Boolean(), nullable=True),
        sa.Column("clients", sa.Integer(), nullable=True),
        sa.Column("objects", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("phone"),
    )
    op.create_index(
        op.f("ix_candidates_is_hired"), "candidates", ["is_hired"], unique=False
    )
    op.create_table(
        "courses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "offices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.Column("location", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "candidate_courses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=True),
        sa.Column("candidate_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["candidate_id"],
            ["candidates.id"],
        ),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["courses.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_candidate_courses_candidate_id"),
        "candidate_courses",
        ["candidate_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_candidate_courses_course_id"),
        "candidate_courses",
        ["course_id"],
        unique=False,
    )
    op.create_table(
        "candidate_skills",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=True),
        sa.Column("candidate_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["candidate_id"],
            ["candidates.id"],
        ),
        sa.ForeignKeyConstraint(
            ["skill_id"],
            ["skills.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_candidate_skills_candidate_id"),
        "candidate_skills",
        ["candidate_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_candidate_skills_skill_id"),
        "candidate_skills",
        ["skill_id"],
        unique=False,
    )
    op.create_table(
        "managers",
        sa.Column("full_name", sa.String(length=100), nullable=True),
        sa.Column("quotas", sa.Integer(), nullable=True),
        sa.Column("office_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("password", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["office_id"],
            ["offices.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_managers_quotas"), "managers", ["quotas"], unique=False)
    op.create_table(
        "manager_candidates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("done_by", sa.Integer(), nullable=True),
        sa.Column("candidate_id", sa.Integer(), nullable=True),
        sa.Column("is_viewed", sa.Boolean(), nullable=True),
        sa.Column("is_favorite", sa.Boolean(), nullable=True),
        sa.Column("note", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["candidate_id"],
            ["candidates.id"],
        ),
        sa.ForeignKeyConstraint(
            ["done_by"],
            ["managers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_manager_candidates_candidate_id"),
        "manager_candidates",
        ["candidate_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_manager_candidates_done_by"),
        "manager_candidates",
        ["done_by"],
        unique=False,
    )
    op.create_index(
        op.f("ix_manager_candidates_is_favorite"),
        "manager_candidates",
        ["is_favorite"],
        unique=False,
    )
    op.create_index(
        op.f("ix_manager_candidates_is_viewed"),
        "manager_candidates",
        ["is_viewed"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_manager_candidates_is_viewed"), table_name="manager_candidates"
    )
    op.drop_index(
        op.f("ix_manager_candidates_is_favorite"), table_name="manager_candidates"
    )
    op.drop_index(
        op.f("ix_manager_candidates_done_by"), table_name="manager_candidates"
    )
    op.drop_index(
        op.f("ix_manager_candidates_candidate_id"), table_name="manager_candidates"
    )
    op.drop_table("manager_candidates")
    op.drop_index(op.f("ix_managers_quotas"), table_name="managers")
    op.drop_table("managers")
    op.drop_index(op.f("ix_candidate_skills_skill_id"), table_name="candidate_skills")
    op.drop_index(
        op.f("ix_candidate_skills_candidate_id"), table_name="candidate_skills"
    )
    op.drop_table("candidate_skills")
    op.drop_index(
        op.f("ix_candidate_courses_course_id"), table_name="candidate_courses"
    )
    op.drop_index(
        op.f("ix_candidate_courses_candidate_id"), table_name="candidate_courses"
    )
    op.drop_table("candidate_courses")
    op.drop_table("skills")
    op.drop_table("offices")
    op.drop_table("courses")
    op.drop_index(op.f("ix_candidates_is_hired"), table_name="candidates")
    op.drop_table("candidates")
    op.drop_table("admins")
    # ### end Alembic commands ###
