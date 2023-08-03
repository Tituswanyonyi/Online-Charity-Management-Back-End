"""Add username column to Ngo model

Revision ID: 45efb522a7db
Revises: 
Create Date: 2023-08-02 17:38:21.623081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45efb522a7db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('donations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=50), nullable=True))
        batch_op.drop_column('donor_name')

    with op.batch_alter_table('ngos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('email', sa.String(length=50), nullable=True))
        batch_op.drop_column('org_email')
        batch_op.drop_column('org_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ngos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('org_name', sa.VARCHAR(length=100), nullable=True))
        batch_op.add_column(sa.Column('org_email', sa.VARCHAR(length=50), nullable=True))
        batch_op.drop_column('email')
        batch_op.drop_column('username')

    with op.batch_alter_table('donations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('donor_name', sa.VARCHAR(length=50), nullable=True))
        batch_op.drop_column('username')

    # ### end Alembic commands ###
