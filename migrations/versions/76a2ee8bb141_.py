"""empty message

Revision ID: 76a2ee8bb141
Revises: c21823fd649b
Create Date: 2017-09-07 21:53:26.916365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76a2ee8bb141'
down_revision = 'c21823fd649b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('leads', sa.Column('is_verified', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('leads', 'is_verified')
    # ### end Alembic commands ###