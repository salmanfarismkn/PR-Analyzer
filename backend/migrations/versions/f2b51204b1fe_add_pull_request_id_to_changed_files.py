"""Add pull_request_id to changed_files

Revision ID: f2b51204b1fe
Revises: fe394418dd7d
Create Date: 2026-08-09 10:40:24.456530
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f2b51204b1fe"
down_revision: Union[str, Sequence[str], None] = "fe394418dd7d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Step 1: Add column as nullable
    op.add_column(
        "changed_files",
        sa.Column("pull_request_id", sa.Integer(), nullable=True),
    )

    # Step 2: Backfill existing rows (set correct PR IDs if possible, or temporary default)
    # Example: set all to 1 temporarily
    op.execute("UPDATE changed_files SET pull_request_id = 1 WHERE pull_request_id IS NULL")

    # Step 3: Alter column to NOT NULL
    op.alter_column("changed_files", "pull_request_id", nullable=False)

    # Step 4: Add index + foreign key
    op.create_index(
        "ix_changed_file_pull_request_id",
        "changed_files",
        ["pull_request_id"],
        unique=False,
    )
    op.create_foreign_key(
        "fk_changed_files_pull_request_id",
        "changed_files",
        "pull_requests",
        ["pull_request_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_changed_files_pull_request_id", "changed_files", type_="foreignkey")
    op.drop_index("ix_changed_file_pull_request_id", table_name="changed_files")
    op.drop_column("changed_files", "pull_request_id")
