"""updated billing model ensuing that plan name is unique

Revision ID: 2c831357263d
Revises: c8e8bd65628a
Create Date: 2024-08-11 13:37:01.628797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c831357263d'
down_revision: Union[str, None] = 'c8e8bd65628a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_subscriptions', sa.Column('organisation_id', sa.String(), nullable=False))
    op.create_foreign_key(None, 'user_subscriptions', 'organisations', ['organisation_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_subscriptions', type_='foreignkey')
    op.drop_column('user_subscriptions', 'organisation_id')
    # ### end Alembic commands ###
