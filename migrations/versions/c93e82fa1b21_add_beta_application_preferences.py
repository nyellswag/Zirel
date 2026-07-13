"""Add beta application tools and update preference.

Revision ID: c93e82fa1b21
Revises: b82d71e9fa10
"""
from alembic import op
import sqlalchemy as sa

revision = "c93e82fa1b21"
down_revision = "b82d71e9fa10"
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table("wishlist_entry") as batch_op:
        batch_op.add_column(sa.Column("current_tools", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("product_updates", sa.Boolean(), nullable=False, server_default=sa.false()))

def downgrade():
    with op.batch_alter_table("wishlist_entry") as batch_op:
        batch_op.drop_column("product_updates")
        batch_op.drop_column("current_tools")
