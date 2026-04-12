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
    """
    Revert the tasks status constraint and rename 'completed' statuses to 'is_completed'.
    
    Drops the `tasks_status_check` constraint on the `tasks` table, updates rows with
    `status = 'completed'` to `status = 'is_completed'`, and re-adds the
    `tasks_status_check` constraint allowing `status` values `'in_progress'` and
    `'is_completed'`.
    """
    op.execute("ALTER TABLE tasks DROP CONSTRAINT tasks_status_check")
    op.execute("UPDATE tasks SET status = 'is_completed' WHERE status = 'completed'")
    op.execute("ALTER TABLE tasks ADD CONSTRAINT tasks_status_check CHECK (status IN('in_progress', 'is_completed'))")
