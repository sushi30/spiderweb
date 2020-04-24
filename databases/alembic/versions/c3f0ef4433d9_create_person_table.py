"""create person table

Revision ID: c3f0ef4433d9
Revises: e9ddfb715aac
Create Date: 2020-04-15 19:00:33.729261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c3f0ef4433d9"
down_revision = "e9ddfb715aac"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "person",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("UUID", sa.String(length=36), nullable=True),
        sa.Column("HEBREW_NAME", sa.String(), nullable=True),
        sa.Column("ENGLISH_NAME", sa.String(), nullable=True),
        sa.Column("ID", sa.String(), nullable=False),
        sa.Column("ID_TYPE", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("ID", "ID_TYPE"),
    )


def downgrade():
    op.drop_table("person")
