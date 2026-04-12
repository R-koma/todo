"""update_status_check_constraint

Revision ID: 1446fe4b88e5
Revises: 999bb0d567ed
Create Date: 2026-04-12 19:24:53.685413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1446fe4b88e5'
down_revision: Union[str, Sequence[str], None] = '999bb0d567ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE tasks DROP CONSTRAINT tasks_status_check")
    op.execute("ALTER TABLE tasks ADD CONSTRAINT tasks_status_check CHECK (status IN('in_progress', 'completed'))")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE tasks DROP CONSTRAINT tasks_status_check")
    op.execute("ALTER TABLE tasks ADD CONSTRAINT tasks_status_check CHECK (status IN('in_progress', 'is_completed'))")
