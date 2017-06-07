"""empty message

Revision ID: 51c653d0876c
Revises: 437126f00e1f
Create Date: 2017-06-07 22:15:15.719326

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '51c653d0876c'
down_revision = '437126f00e1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_login', sa.DateTime(), nullable=True))
    op.alter_column('user', 'email',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'email',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.drop_column('user', 'last_login')
    # ### end Alembic commands ###