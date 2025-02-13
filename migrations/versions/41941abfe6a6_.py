"""empty message

Revision ID: 41941abfe6a6
Revises: b708a7ba0deb
Create Date: 2025-02-09 23:41:16.454861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41941abfe6a6'
down_revision = 'b708a7ba0deb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fav_people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('people_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fav_people')
    # ### end Alembic commands ###
