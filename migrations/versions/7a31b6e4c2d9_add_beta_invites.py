"""add beta invites

Revision ID: 7a31b6e4c2d9
Revises: 4af6f4d6d5a2
"""
from alembic import op
import sqlalchemy as sa

revision = "7a31b6e4c2d9"
down_revision = "4af6f4d6d5a2"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "beta_invite",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("note", sa.String(length=200), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("used_at", sa.DateTime(), nullable=True),
        sa.Column("used_by_id", sa.Integer(), nullable=True),
        sa.Column("revoked", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["used_by_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("used_by_id"),
    )
    op.create_index(op.f("ix_beta_invite_code"), "beta_invite", ["code"], unique=True)


def downgrade():
    op.drop_index(op.f("ix_beta_invite_code"), table_name="beta_invite")
    op.drop_table("beta_invite")
