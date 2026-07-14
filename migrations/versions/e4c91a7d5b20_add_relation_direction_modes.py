"""Add relation direction modes and inverse labels.

Revision ID: e4c91a7d5b20
Revises: c93e82fa1b21
"""

from alembic import op
import sqlalchemy as sa


revision = "e4c91a7d5b20"
down_revision = "c93e82fa1b21"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("relation") as batch_op:
        batch_op.alter_column(
            "relation_type",
            existing_type=sa.String(length=40),
            type_=sa.String(length=80),
            existing_nullable=False,
        )
        batch_op.add_column(
            sa.Column(
                "direction_mode",
                sa.String(length=20),
                nullable=False,
                server_default="one_way",
            )
        )
        batch_op.add_column(sa.Column("inverse_relation_type", sa.String(length=80), nullable=True))


def downgrade():
    with op.batch_alter_table("relation") as batch_op:
        batch_op.drop_column("inverse_relation_type")
        batch_op.drop_column("direction_mode")
        batch_op.alter_column(
            "relation_type",
            existing_type=sa.String(length=80),
            type_=sa.String(length=40),
            existing_nullable=False,
        )
