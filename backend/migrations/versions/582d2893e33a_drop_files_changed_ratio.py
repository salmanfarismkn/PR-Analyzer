"""drop files_changed_ratio

Revision ID: 582d2893e33a
Revises: 08933e6b772e
Create Date: 2026-09-02 15:20:07.848026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '582d2893e33a'
down_revision: Union[str, Sequence[str], None] = '08933e6b772e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: drop files_changed_ratio column."""
    op.drop_column("pr_feature_snapshot", "files_changed_ratio")


def downgrade() -> None:
    """Downgrade schema: add files_changed_ratio column back."""
    op.add_column(
        "pr_feature_snapshot",
        sa.Column("files_changed_ratio", sa.Float(), nullable=True),
    )
