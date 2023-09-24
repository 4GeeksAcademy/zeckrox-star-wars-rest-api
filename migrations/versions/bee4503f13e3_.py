"""empty message

Revision ID: bee4503f13e3
Revises: 7ad7001d5a54
Create Date: 2023-09-24 18:03:24.248477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bee4503f13e3'
down_revision = '7ad7001d5a54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite_people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('people_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_planets_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('favorite_people_id', sa.Integer(), nullable=True))
        batch_op.create_unique_constraint(None, ['user_id'])
        batch_op.drop_constraint('favorite_planet_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('favorite_people_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'favorite_planets', ['favorite_planets_id'], ['id'])
        batch_op.create_foreign_key(None, 'favorite_people', ['favorite_people_id'], ['id'])
        batch_op.drop_column('planet_id')
        batch_op.drop_column('people_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('people_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('favorite_people_id_fkey', 'people', ['people_id'], ['id'])
        batch_op.create_foreign_key('favorite_planet_id_fkey', 'planet', ['planet_id'], ['id'])
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('favorite_people_id')
        batch_op.drop_column('favorite_planets_id')

    op.drop_table('favorite_planets')
    op.drop_table('favorite_people')
    # ### end Alembic commands ###
