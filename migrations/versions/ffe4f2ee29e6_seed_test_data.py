"""seed test data

Revision ID: ffe4f2ee29e6
Revises: aa33e5646b25
Create Date: 2026-08-03 11:49:29.195634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffe4f2ee29e6'
down_revision: Union[str, Sequence[str], None] = 'aa33e5646b25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
