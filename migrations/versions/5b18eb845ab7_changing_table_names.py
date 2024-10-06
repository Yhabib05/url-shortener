"""changing table names

Revision ID: 5b18eb845ab7
Revises: 
Create Date: 2024-10-06 13:14:39.772018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b18eb845ab7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('data_base')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('data_base',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('long_url', sa.VARCHAR(length=500), nullable=False),
    sa.Column('short_id', sa.VARCHAR(length=8), nullable=False),
    sa.Column('user_id', sa.VARCHAR(length=20), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short_id'),
    sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###
