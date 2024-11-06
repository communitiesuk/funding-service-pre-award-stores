"""Fund Store

Revision ID: 002_fund_store
Revises: 001_application_store
Create Date: 2024-11-06 14:53:53.140093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision: str = '002_fund_store'
down_revision: Union[str, None] = '001_application_store'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assessment_field',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('field_type', sa.String(), nullable=False),
    sa.Column('display_type', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_assessment_field')),
    sa.UniqueConstraint('id', name=op.f('uq_assessment_field_id'))
    )
    op.create_table('fund',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name_json', sa.JSON(none_as_null=True), nullable=False),
    sa.Column('title_json', sa.JSON(none_as_null=True), nullable=False),
    sa.Column('short_name', sa.String(), nullable=False),
    sa.Column('description_json', sa.JSON(none_as_null=True), nullable=False),
    sa.Column('welsh_available', sa.Boolean(), nullable=False),
    sa.Column('owner_organisation_name', sa.String(), nullable=False),
    sa.Column('owner_organisation_shortname', sa.String(), nullable=False),
    sa.Column('owner_organisation_logo_uri', sa.Text(), nullable=True),
    sa.Column('funding_type', sa.Enum('COMPETITIVE', 'UNCOMPETED', 'EOI', name='fundingtype'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_fund')),
    sa.UniqueConstraint('short_name', name=op.f('uq_fund_short_name'))
    )
    op.create_table('round',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('fund_id', sa.UUID(), nullable=False),
    sa.Column('title_json', sa.JSON(none_as_null=True), nullable=False),
    sa.Column('short_name', sa.String(), nullable=False),
    sa.Column('opens', sa.DateTime(), nullable=True),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.Column('assessment_start', sa.DateTime(), nullable=True),
    sa.Column('application_reminder_sent', sa.Boolean(), nullable=False),
    sa.Column('reminder_date', sa.DateTime(), nullable=True),
    sa.Column('assessment_deadline', sa.DateTime(), nullable=True),
    sa.Column('prospectus', sa.String(), nullable=False),
    sa.Column('privacy_notice', sa.String(), nullable=False),
    sa.Column('contact_us_banner_json', sa.JSON(none_as_null=True), nullable=True),
    sa.Column('reference_contact_page_over_email', sa.Boolean(), nullable=False),
    sa.Column('contact_email', sa.String(), nullable=True),
    sa.Column('contact_phone', sa.String(), nullable=True),
    sa.Column('contact_textphone', sa.String(), nullable=True),
    sa.Column('support_times', sa.String(), nullable=False),
    sa.Column('support_days', sa.String(), nullable=False),
    sa.Column('instructions_json', sa.JSON(none_as_null=True), nullable=True),
    sa.Column('feedback_link', sa.String(), nullable=True),
    sa.Column('project_name_field_id', sa.String(), nullable=False),
    sa.Column('application_guidance_json', sa.JSON(none_as_null=True), nullable=True),
    sa.Column('guidance_url', sa.String(), nullable=True),
    sa.Column('all_uploaded_documents_section_available', sa.Boolean(), nullable=False),
    sa.Column('application_fields_download_available', sa.Boolean(), nullable=False),
    sa.Column('display_logo_on_pdf_exports', sa.Boolean(), nullable=False),
    sa.Column('mark_as_complete_enabled', sa.Boolean(), nullable=False),
    sa.Column('is_expression_of_interest', sa.Boolean(), nullable=False),
    sa.Column('feedback_survey_config', sa.JSON(none_as_null=True), nullable=True),
    sa.Column('eligibility_config', sa.JSON(none_as_null=True), nullable=True),
    sa.Column('eoi_decision_schema ', sa.JSON(none_as_null=True), nullable=True),
    sa.ForeignKeyConstraint(['fund_id'], ['fund.id'], name=op.f('fk_round_fund_id_fund')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_round')),
    sa.UniqueConstraint('fund_id', 'short_name', name=op.f('uq_round_fund_id'))
    )
    op.create_table('event',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('round_id', sa.UUID(), nullable=True),
    sa.Column('type', sa.Enum('APPLICATION_DEADLINE_REMINDER', 'SEND_INCOMPLETE_APPLICATIONS', 'ACCOUNT_IMPORT', name='event_type'), nullable=False),
    sa.Column('activation_date', sa.DateTime(), nullable=False),
    sa.Column('processed', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['round_id'], ['round.id'], name=op.f('fk_event_round_id_round')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_event'))
    )
    op.create_table('section',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title_json', sa.JSON(none_as_null=True), nullable=False),
    sa.Column('requires_feedback', sa.Boolean(), nullable=False),
    sa.Column('round_id', sa.UUID(), nullable=False),
    sa.Column('weighting', sa.Integer(), nullable=True),
    sa.Column('path', sqlalchemy_utils.types.ltree.LtreeType(), nullable=False),
    sa.ForeignKeyConstraint(['round_id'], ['round.id'], name=op.f('fk_section_round_id_round')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_section'))
    )
    with op.batch_alter_table('section', schema=None) as batch_op:
        batch_op.create_index('ix_sections_path', ['path'], unique=False, postgresql_using='gist')

    op.create_table('form_name',
    sa.Column('section_id', sa.Integer(), nullable=False),
    sa.Column('form_name_json', sa.JSON(none_as_null=True), nullable=False),
    sa.ForeignKeyConstraint(['section_id'], ['section.id'], name=op.f('fk_form_name_section_id_section')),
    sa.PrimaryKeyConstraint('section_id', name=op.f('pk_form_name'))
    )
    op.create_table('section_field',
    sa.Column('section_id', sa.Integer(), nullable=False),
    sa.Column('field_id', sa.String(), nullable=False),
    sa.Column('display_order', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['field_id'], ['assessment_field.id'], name=op.f('fk_section_field_field_id_assessment_field')),
    sa.ForeignKeyConstraint(['section_id'], ['section.id'], name=op.f('fk_section_field_section_id_section')),
    sa.PrimaryKeyConstraint('section_id', 'field_id', name=op.f('pk_section_field'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('section_field')
    op.drop_table('form_name')
    with op.batch_alter_table('section', schema=None) as batch_op:
        batch_op.drop_index('ix_sections_path', postgresql_using='gist')

    op.drop_table('section')
    op.drop_table('event')
    op.drop_table('round')
    op.drop_table('fund')
    op.drop_table('assessment_field')
    # ### end Alembic commands ###
