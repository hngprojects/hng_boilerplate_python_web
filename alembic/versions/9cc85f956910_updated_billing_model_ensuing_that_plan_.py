"""updated billing model ensuing that plan name is unique

Revision ID: 9cc85f956910
Revises: c82575f5f4ed
Create Date: 2024-08-11 17:04:57.083221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cc85f956910'
down_revision: Union[str, None] = 'c82575f5f4ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
