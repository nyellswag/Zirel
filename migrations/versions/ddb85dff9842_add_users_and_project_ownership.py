"""Add users and project ownership

Revision ID: ddb85dff9842
Revises: 2bb216b2e40b
Create Date: 2026-06-21 17:02:01.623541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddb85dff9842'
down_revision = '2bb216b2e40b'
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    if "user" not in inspector.get_table_names():
        op.create_table(
            "user",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("username", sa.String(length=80), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("password_hash", sa.String(length=256), nullable=False),
            sa.Column("is_admin", sa.Boolean(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("email"),
            sa.UniqueConstraint("username"),
        )

    project_columns = {column["name"] for column in inspector.get_columns("project")}
    if "user_id" not in project_columns:
        with op.batch_alter_table("project", schema=None) as batch_op:
            batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=True))
            batch_op.create_foreign_key(
                "fk_project_user_id",
                "user",
                ["user_id"],
                ["id"],
            )


def downgrade():
    with op.batch_alter_table("project", schema=None) as batch_op:
        batch_op.drop_constraint("fk_project_user_id", type_="foreignkey")
        batch_op.drop_column("user_id")

    op.drop_table("user")
