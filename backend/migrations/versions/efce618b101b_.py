"""empty message

Revision ID: efce618b101b
Revises: 87e83c96c13e
Create Date: 2025-03-23 08:15:02.519392

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'efce618b101b'
down_revision = '87e83c96c13e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('promotion', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tags', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))
        batch_op.alter_column('title',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=10),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('promotion', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.String(length=10),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=True)
        batch_op.drop_column('description')
        batch_op.drop_column('tags')

    # ### end Alembic commands ###
