"""Create feedback_message column

Revision ID: 008_add_feedback_message
Revises: 007_create_account_store
Create Date: 2024-11-30 19:33:00.710210

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "008_add_feedback_message"
down_revision = "007_create_account_store"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE status ADD VALUE 'CHANGES_REQUESTED'")


def downgrade():
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
