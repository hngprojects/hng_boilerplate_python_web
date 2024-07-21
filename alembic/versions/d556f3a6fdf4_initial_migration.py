"""initial migration

Revision ID: d556f3a6fdf4
Revises: 534047ee3520
Create Date: 2024-07-21 23:26:58.884048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd556f3a6fdf4'
down_revision: Union[str, None] = '534047ee3520'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('newsletters')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('newsletters',
    sa.Column('id', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='newsletters_pkey'),
    sa.UniqueConstraint('email', name='newsletters_email_key')
    )
    # ### end Alembic commands ###
