"""update email template fields

Revision ID: 854472eb449d
Revises: 27ffc98eab7b
Create Date: 2024-08-01 14:47:41.077078

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '854472eb449d'
down_revision: Union[str, None] = '27ffc98eab7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('email_templates', sa.Column('title', sa.Text(), nullable=False))
    op.add_column('email_templates', sa.Column('template', sa.Text(), nullable=False))
    op.add_column('email_templates', sa.Column('status', sa.Boolean(), server_default='true', nullable=True))
    op.drop_column('email_templates', 'name')
    op.drop_column('email_templates', 'html_content')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('email_templates', sa.Column('html_content', sa.TEXT(), autoincrement=False, nullable=False))
    op.add_column('email_templates', sa.Column('name', sa.TEXT(), autoincrement=False, nullable=False))
    op.drop_column('email_templates', 'status')
    op.drop_column('email_templates', 'template')
    op.drop_column('email_templates', 'title')
    # ### end Alembic commands ###
