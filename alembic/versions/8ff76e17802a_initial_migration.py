"""initial migration

Revision ID: 8ff76e17802a
Revises: 17515fbab786
Create Date: 2025-10-25 12:44:22.579837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ff76e17802a'
down_revision: Union[str, Sequence[str], None] = '17515fbab786'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
