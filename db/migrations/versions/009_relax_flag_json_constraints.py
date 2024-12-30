"""Allow nullable user_id in flag_update and allow editable json on assessment_records.
Add two new workflow statuses

Revision ID: "009_relax_flag_json_constraints"
Revises: "008_extend_flag_for_change_req"
Create Date: 2024-12-19 16:30:00.346479

"""

from alembic import op
from alembic_utils.pg_trigger import PGTrigger

# revision identifiers, used by Alembic.
revision = "009_relax_flag_json_constraints"
down_revision = "008_extend_flag_for_change_req"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("DROP TRIGGER IF EXISTS block_updates_on_app_blob on assessment_records")

    op.execute("alter type status add value 'CHANGE_REQUESTED' after 'COMPLETED'")
    op.execute("alter type status add value 'CHANGE_RECEIVED' after 'CHANGE_REQUESTED'")


def downgrade():
    public_assessment_records_block_updates_on_app_blob = PGTrigger(
        schema="public",
        signature="block_updates_on_app_blob",
        on_entity="public.assessment_records",
        is_constraint=False,
        definition="BEFORE UPDATE\n    ON assessment_records\n    FOR EACH ROW\n    EXECUTE PROCEDURE block_blob_mutate()",  # noqa: E501
    )
    op.create_entity(public_assessment_records_block_updates_on_app_blob)

    # Revert enum by removing the new statuses
    # Step 1: Rename the existing ENUM type
    op.execute("ALTER TYPE status RENAME TO status_old")
    # Step 2: Create a new ENUM type without the unwanted value
    op.execute("""
        CREATE TYPE status AS ENUM(
            'NOT_STARTED',
            'IN_PROGRESS',
            'SUBMITTED',
            'COMPLETED'
        )
    """)
    # Step 3: Update all columns using the old ENUM type to use the new ENUM type
    op.execute("""
        ALTER TABLE forms
        ALTER COLUMN status
        TYPE status
        USING status::TEXT::status
    """)
    op.execute("""
        ALTER TABLE applications
        ALTER COLUMN status
        TYPE status
        USING status::TEXT::status
    """)
    op.execute("""
        ALTER TABLE feedback
        ALTER COLUMN status
        TYPE status
        USING status::TEXT::status
    """)
    op.execute("""
        ALTER TABLE assessment_records
        ALTER COLUMN workflow_status
        TYPE status
        USING workflow_status::TEXT::status
    """)
    # Step 4: Drop the old ENUM type
    op.execute("DROP TYPE status_old")
