"""Add feedback topic

Revision ID: 4af6f4d6d5a2
Revises: 3390b393a0e8
Create Date: 2026-07-07 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "4af6f4d6d5a2"
down_revision = "3390b393a0e8"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("feedback", sa.Column("topic", sa.String(length=60), nullable=True))


def downgrade():
    op.drop_column("feedback", "topic")
