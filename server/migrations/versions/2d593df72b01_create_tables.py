"""create tables

Revision ID: 2d593df72b01
Revises: 1c1f3ff06933
Create Date: 2023-06-15 20:49:46.015676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d593df72b01'
down_revision = '1c1f3ff06933'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('signups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Camper', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_signups_Camper_campers'), 'campers', ['Camper'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('signups', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_signups_Camper_campers'), type_='foreignkey')
        batch_op.drop_column('Camper')

    # ### end Alembic commands ###
