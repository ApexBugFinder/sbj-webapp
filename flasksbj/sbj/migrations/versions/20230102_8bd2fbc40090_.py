"""empty message

Revision ID: 8bd2fbc40090
Revises: 7dddbd8ff9ee
Create Date: 2023-01-02 06:47:07.471585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bd2fbc40090'
down_revision = '7dddbd8ff9ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gameplayers',
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], ),
    sa.PrimaryKeyConstraint('game_id', 'player_id')
    )
    op.create_table('handcards',
    sa.Column('hand_id', sa.Integer(), nullable=False),
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.Column('added_to_hand_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['card_id'], ['cards.id'], ),
    sa.ForeignKeyConstraint(['hand_id'], ['hands.id'], ),
    sa.PrimaryKeyConstraint('hand_id', 'card_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('handcards')
    op.drop_table('gameplayers')
    # ### end Alembic commands ###