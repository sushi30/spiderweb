"""create firm table

Revision ID: e9ddfb715aac
Revises: 3a0e9563f487
Create Date: 2020-04-15 18:59:26.674315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e9ddfb715aac"
down_revision = "3a0e9563f487"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "firm",
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
    op.drop_table("firm")
