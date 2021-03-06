"""empty message

Revision ID: 1fe7cafd8736
Revises: 758e5a466ba2
Create Date: 2021-10-26 00:27:56.143170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fe7cafd8736'
down_revision = '758e5a466ba2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('population', sa.String(length=120), nullable=False),
    sa.Column('terrain', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('name')
    )
    op.drop_index('eye_color', table_name='people')
    op.drop_index('eye_color_2', table_name='people')
    op.drop_index('gender', table_name='people')
    op.drop_index('gender_2', table_name='people')
    op.drop_index('hair_color', table_name='people')
    op.drop_index('hair_color_2', table_name='people')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('hair_color_2', 'people', ['hair_color'], unique=False)
    op.create_index('hair_color', 'people', ['hair_color'], unique=False)
    op.create_index('gender_2', 'people', ['gender'], unique=False)
    op.create_index('gender', 'people', ['gender'], unique=False)
    op.create_index('eye_color_2', 'people', ['eye_color'], unique=False)
    op.create_index('eye_color', 'people', ['eye_color'], unique=False)
    op.drop_table('planets')
    # ### end Alembic commands ###
