"""empty message

Revision ID: c2a534a4b74a
Revises: e6223cb02ea7
Create Date: 2023-09-28 09:50:15.321979

"""

import sqlalchemy
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c2a534a4b74a"
down_revision = "e6223cb02ea7"
branch_labels = None
depends_on = None


NSTF_R2_GUIDANCE_URL = "https://mhclg.sharepoint.com.mcas.ms/:w:/s/HomelessnessandRoughSleeping/EZn-Dq3eBvFDtdBqhyEZxUUBj_BP53F9TVyI0imX3NdcPw?e=PtmLwH"  # noqa
COF_R2_GUIDANCE_URL = "https://mhclg.sharepoint.com.mcas.ms/:w:/s/CommunityOwnershipFund/Ecv3iM7U0AtKtyHnzRrQ9dsB0HdMPvHWqAoGn1WrWM7EMA?e=6QpdUT"  # noqa
COF_R3_GUIDANCE_URL = "https://www.gov.uk/government/publications/community-ownership-fund-round-3-application-form-assessment-criteria-guidance"  # noqa


def upgrade():
    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.drop_column("guidance_url")

    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(sa.Column("guidance_url", sa.String(), nullable=True))

    connection = op.get_bind()
    connection.execute(
        sqlalchemy.text(
            f"""
                UPDATE round
                SET guidance_url = '{NSTF_R2_GUIDANCE_URL}'
                WHERE fund_id = '13b95669-ed98-4840-8652-d6b7a19964db' and short_name = 'R2'
                """
        )
    )
    connection.execute(
        sqlalchemy.text(
            f"""
                UPDATE round
                set guidance_url = '{COF_R3_GUIDANCE_URL}'
                WHERE fund_id = '47aef2f5-3fcb-4d45-acb5-f0152b5f03c4' and short_name in ('R3W1', 'R3W2')
                """
        )
    )
    connection.execute(
        sqlalchemy.text(
            f"""
                UPDATE round
                set guidance_url = '{COF_R2_GUIDANCE_URL}'
                WHERE fund_id = '47aef2f5-3fcb-4d45-acb5-f0152b5f03c4' and short_name in ('R2W2', 'R2W3')
                """
        )
    )


def downgrade():
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.drop_column("guidance_url")

    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.add_column(sa.Column("guidance_url", sa.VARCHAR(), autoincrement=False, nullable=True))
