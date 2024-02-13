"""Empty message.

Revision ID: 3d9f0c0345ae
Revises: 5c03105a204c
Create Date: 2024-02-12 15:12:50.627103

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3d9f0c0345ae"
down_revision = "5c03105a204c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    insert_query = sa.text(
        "INSERT INTO assessment_round(round_id, scoring_system)" "VALUES (:uuid, :scoring_system) RETURNING round_id;"
    )

    params = {
        "uuid": "6a47c649-7bac-4583-baed-9c4e7a35c8b3",
        "scoring_system": "OneToFive",
    }
    connection.execute(insert_query, params)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    delete_query = sa.text("DELETE FROM assessment_round WHERE round_id = :uuid;")
    params = {
        "uuid": "6a47c649-7bac-4583-baed-9c4e7a35c8b3",
    }
    connection.execute(delete_query, params)
    # ### end Alembic commands ###
