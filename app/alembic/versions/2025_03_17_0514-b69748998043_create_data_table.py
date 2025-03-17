"""create_data_table

Revision ID: b69748998043
Revises:
Create Date: 2025-03-17 05:14:27.849432

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b69748998043"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "data",
        sa.Column("object", sa.String(length=50), nullable=False),
        sa.Column("status", sa.Integer(), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("parent", sa.String(), nullable=True),
        sa.Column("owner", sa.String(length=14), nullable=False),
        sa.PrimaryKeyConstraint("object", name=op.f("pk_data")),
    )


def downgrade() -> None:
    op.drop_table("data")
