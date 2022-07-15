import datetime
import os
import uuid

import flask_migrate
from config import Config
from db import db
from db.models.assessment import Assessment
from db.models.scores_justifications import ScoresJustifications
from db.models.sub_criteria import SubCriteria


class SqliteTestDB:
    @classmethod
    def remove(cls):
        flask_root = Config.FLASK_ROOT
        db_file_name = Config.SQLITE_DB_NAME
        db_file_path = os.path.join(flask_root, db_file_name)
        if os.path.exists(db_file_path):
            os.remove(db_file_path)

    @classmethod
    def create(cls):
        cls.remove()
        flask_migrate.upgrade()

        assessment_1 = Assessment(
            id="123e4567-e89b-12d3-a456-426655440000",
            compliance_status="great",
            application_id="amazing",
        )
        db.session.add(assessment_1)
        db.session.commit()

        sub_criteria_1 = SubCriteria(
            id="123e4567-e89b-12d3-a456-426655440001",
            round_id="hello",
            criteria_id="hi",
            sub_criteria_title="something",
        )
        db.session.add(sub_criteria_1)
        db.session.commit()

        sub_criteria_2 = SubCriteria(
            id="123e4567-e89b-12d3-a456-426655440002",
            round_id="ciao",
            criteria_id="cya",
            sub_criteria_title="nothing",
        )
        db.session.add(sub_criteria_2)
        db.session.commit()

        score_justification = ScoresJustifications(
            scores_justifications_id=uuid.UUID(
                "123e4567-e89b-12d3-a456-426655440003"
            ),
            created_at=datetime.datetime.strptime(
                "2022-07-07T09:11:38.240578Z", "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            sub_criteria_id="123e4567-e89b-12d3-a456-426655440001",
            assessment_id="123e4567-e89b-12d3-a456-426655440000",
            score=5,
            justification="wow",
            assessor_user_id="person_1",
        )
        db.session.add(score_justification)
        db.session.commit()
