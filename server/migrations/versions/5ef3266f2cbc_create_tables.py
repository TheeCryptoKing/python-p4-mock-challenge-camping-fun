"""create tables

Revision ID: 5ef3266f2cbc
Revises: 
Create Date: 2023-06-16 21:50:48.169694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ef3266f2cbc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('difficulty', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_activities'))
    )
    op.create_table('campers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_campers'))
    )
    op.create_table('signups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Camper', sa.Integer(), nullable=True),
    sa.Column('Activity', sa.Integer(), nullable=True),
    sa.Column('time', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['Activity'], ['activities.id'], name=op.f('fk_signups_Activity_activities')),
    sa.ForeignKeyConstraint(['Camper'], ['campers.id'], name=op.f('fk_signups_Camper_campers')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_signups'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('signups')
    op.drop_table('campers')
    op.drop_table('activities')
    # ### end Alembic commands ###