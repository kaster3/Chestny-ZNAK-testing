"""create_documents_table

Revision ID: 4309ed459816
Revises: b69748998043
Create Date: 2025-03-17 05:15:24.802165

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "4309ed459816"
down_revision: Union[str, None] = "b69748998043"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("doc_id", sa.String(), nullable=False),
        sa.Column("received_at", sa.DateTime(), nullable=True),
        sa.Column("document_type", sa.String(), nullable=False),
        sa.Column(
            "document_data",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("processed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("doc_id", name=op.f("pk_documents")),
    )


def downgrade() -> None:
    op.drop_table("documents")
