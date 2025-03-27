"""empty message

Revision ID: 184420057744
Revises: a0f18750d542
Create Date: 2025-03-26 20:36:17.460259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '184420057744'
down_revision = 'a0f18750d542'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.alter_column('gravity',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.alter_column('gravity',
               existing_type=sa.String(length=20),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
