"""empty message

Revision ID: 87bab63eacab
Revises: 
Create Date: 2023-01-07 23:46:25.787291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87bab63eacab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cards',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('h_value', sa.Integer(), nullable=False),
    sa.Column('l_value', sa.Integer(), nullable=False),
    sa.Column('face', sa.String(length=3), nullable=True),
    sa.Column('suite', sa.String(length=8), nullable=True),
    sa.Column('url', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('face')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cards')
    # ### end Alembic commands ###