"""Expand wishlist entries into beta applications.

Revision ID: b82d71e9fa10
Revises: 7a31b6e4c2d9
"""

from alembic import op
import sqlalchemy as sa


revision = "b82d71e9fa10"
down_revision = "7a31b6e4c2d9"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("wishlist_entry") as batch_op:
        batch_op.add_column(sa.Column("timezone", sa.String(length=80), nullable=True))
        batch_op.add_column(sa.Column("experience", sa.String(length=80), nullable=True))
        batch_op.add_column(sa.Column("active_projects", sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column("frustration", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("alpha_comfort", sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column("heard_from", sa.String(length=80), nullable=True))
        batch_op.add_column(sa.Column("beta_goal", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("feedback_frequency", sa.String(length=80), nullable=True))
        batch_op.add_column(sa.Column("status", sa.String(length=30), nullable=False, server_default="legacy"))
        batch_op.add_column(sa.Column("wave", sa.String(length=40), nullable=True))
        batch_op.add_column(sa.Column("admin_notes", sa.Text(), nullable=True))


def downgrade():
    with op.batch_alter_table("wishlist_entry") as batch_op:
        for column in (
            "admin_notes", "wave", "status", "feedback_frequency", "beta_goal",
            "heard_from", "alpha_comfort", "frustration", "active_projects",
            "experience", "timezone",
        ):
            batch_op.drop_column(column)
