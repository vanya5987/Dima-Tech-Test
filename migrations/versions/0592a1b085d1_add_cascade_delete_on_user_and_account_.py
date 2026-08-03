"""add cascade delete on user and account fk

Revision ID: 0592a1b085d1
Revises: ffe4f2ee29e6
Create Date: 2026-08-03 11:59:43.567429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0592a1b085d1'
down_revision: Union[str, Sequence[str], None] = 'ffe4f2ee29e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint('accounts_user_id_fkey', 'accounts', type_='foreignkey')
    op.create_foreign_key(
        'accounts_user_id_fkey', 'accounts', 'users', ['user_id'], ['id'], ondelete='CASCADE'
    )

    op.drop_constraint('payments_account_id_fkey', 'payments', type_='foreignkey')
    op.create_foreign_key(
        'payments_account_id_fkey', 'payments', 'accounts', ['account_id'], ['id'], ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('payments_account_id_fkey', 'payments', type_='foreignkey')
    op.create_foreign_key(
        'payments_account_id_fkey', 'payments', 'accounts', ['account_id'], ['id']
    )

    op.drop_constraint('accounts_user_id_fkey', 'accounts', type_='foreignkey')
    op.create_foreign_key(
        'accounts_user_id_fkey', 'accounts', 'users', ['user_id'], ['id']
    )
