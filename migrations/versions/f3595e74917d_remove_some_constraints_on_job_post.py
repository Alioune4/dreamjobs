"""Remove some constraints on job post

Revision ID: f3595e74917d
Revises: b8dd57ea8246
Create Date: 2024-07-24 01:55:46.660609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3595e74917d'
down_revision = 'b8dd57ea8246'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_posts', schema=None) as batch_op:
        batch_op.alter_column('salary',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('location',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.drop_constraint('job_posts_posted_by_fkey', type_='foreignkey')
        batch_op.drop_column('posted_by')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('posted_by', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('job_posts_posted_by_fkey', 'users', ['posted_by'], ['id'])
        batch_op.alter_column('location',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('salary',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
