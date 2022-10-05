"""empty message

Revision ID: 5bf853808dfb
Revises: 
Create Date: 2022-09-27 12:34:43.514139

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = '5bf853808dfb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    status_enum = postgresql.ENUM('NOT_STARTED', 'IN_PROGRESS', 'SUBMITTED', 'COMPLETED', name='status')

    op.create_table('applications',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('account_id', sa.String(), nullable=False),
    sa.Column('fund_id', sa.String(), nullable=False),
    sa.Column('round_id', sa.String(), nullable=False),
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('reference', sa.String(), nullable=False),
    sa.Column('project_name', sa.String(), nullable=True),
    sa.Column('started_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('status', status_enum, nullable=False),
    sa.Column('date_submitted', sa.DateTime(), nullable=True),
    sa.Column('last_edited', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_applications')),
    sa.UniqueConstraint('fund_id', 'round_id', 'key', name='_reference'),
    sa.UniqueConstraint('reference', name=op.f('uq_applications_reference'))
    )
    op.create_table('forms',
    sa.Column('id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('application_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('json', sa.JSON(), nullable=True),
    sa.Column('status', status_enum, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('has_completed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['application_id'], ['applications.id'], name=op.f('fk_forms_application_id_applications')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_forms')),
    sa.UniqueConstraint('id', 'name', name=op.f('uq_forms_id'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('forms')
    op.drop_table('applications')
    # ### end Alembic commands ###
