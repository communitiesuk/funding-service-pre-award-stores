"""Empty message.

Revision ID: eecdd097df78
Revises: 2737a83d7605
Create Date: 2024-07-17 10:58:42.292111

"""
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "eecdd097df78"
down_revision = "2737a83d7605"
branch_labels = None
depends_on = None


# Assuming you have a function to generate UUIDs or you can use the uuid module
def generate_uuid():
    return str(uuid.uuid4())


# Insert scoring systems
one_to_five_id = generate_uuid()  # Generate a UUID for OneToFive
zero_to_three_id = generate_uuid()  # Generate a UUID for OneToThree


def upgrade():
    conn = op.get_bind()
    # Define scoring_system variable outside the if block
    scoring_system = postgresql.ENUM("OneToFive", "ZeroToThree", name="scoringsystem", create_type=False)

    # Rename the primary key constraint
    conn.execute(sa.text("ALTER TABLE assessment_round RENAME CONSTRAINT pk_scoring_system TO pk_assessment_round"))

    op.create_table(
        "scoring_system",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("scoring_system_name", scoring_system, nullable=False),
        sa.Column("minimum_score", sa.Integer(), nullable=False),
        sa.Column("maximum_score", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_scoring_system")),
    )
    op.execute(
        sa.text(
            "INSERT INTO scoring_system (id, scoring_system_name, minimum_score, maximum_score) "
            "VALUES (:id, 'OneToFive', 1, 5)"
        ).bindparams(id=one_to_five_id)
    )
    op.execute(
        sa.text(
            "INSERT INTO scoring_system (id, scoring_system_name, minimum_score, maximum_score) "
            "VALUES (:id, 'ZeroToThree', 0, 3)"
        ).bindparams(id=zero_to_three_id)
    )

    with op.batch_alter_table("assessment_round", schema=None) as batch_op:
        batch_op.add_column(sa.Column("scoring_system_id", sa.UUID(), nullable=True))
        batch_op.create_foreign_key(
            batch_op.f("fk_assessment_round_scoring_system_id_scoring_system"),
            "scoring_system",
            ["scoring_system_id"],
            ["id"],
        )
        batch_op.drop_column("scoring_system")

    # Assuming one_to_five_id is defined earlier and contains the ID for the OneToFive scoring system
    OneToFive_round_ids = [
        "e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762",
        "6af19a5e-9cae-4f00-9194-cf10d2d7c8a7",
        "888aae3d-7e2c-4523-b9c1-95952b3d1644",
        "0059aad4-5eb5-11ee-8c99-0242ac120002",
        "fc7aa604-989e-4364-98a7-d1234271435a",
        "c603d114-5364-4474-a0c4-c41cbf4d3bbd",
        "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f",
        "33726b63-efce-4749-b149-20351346c76e",
    ]

    # Convert list of round_ids to a format suitable for SQL IN clause
    round_ids_str = ",".join(f"'{id}'" for id in OneToFive_round_ids)

    # Update the scoring_system_id for specific round_ids
    op.execute(
        sa.text(
            f"UPDATE assessment_round SET scoring_system_id = :scoring_system_id WHERE round_id IN ({round_ids_str})"
        ).bindparams(scoring_system_id=one_to_five_id)
    )

    # ### end Alembic commands ###


def downgrade():
    conn = op.get_bind()
    op.add_column("assessment_round", sa.Column("scoring_system", sa.String(), nullable=True))
    conn.execute(
        sa.text(
            """
        UPDATE assessment_round
        SET scoring_system = (
            SELECT scoring_system_name FROM scoring_system
            WHERE scoring_system.id = assessment_round.scoring_system_id
        )
    """
        )
    )

    # Delete the foreign key constraint before dropping the column
    with op.batch_alter_table("assessment_round", schema=None) as batch_op:
        batch_op.drop_constraint("fk_assessment_round_scoring_system_id_scoring_system", type_="foreignkey")
        batch_op.drop_column("scoring_system_id")

    # Drop the scoring_system table
    op.drop_table("scoring_system")

    conn.execute(sa.text("ALTER TABLE assessment_round RENAME CONSTRAINT pk_assessment_round TO pk_scoring_system"))
