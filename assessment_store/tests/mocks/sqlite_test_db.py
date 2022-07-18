import datetime
import os
import uuid

import flask_migrate
from config import Config
from db import db
from db.models.assessment import Assessment
from db.models.criteria import Criteria
from db.models.scores_justifications import ScoresJustifications
from db.models.sub_criteria import SubCriteria


class SqliteTestDB:

    crit_1_uuid = uuid.uuid4()
    crit_2_uuid = uuid.uuid4()
    crit_3_uuid = uuid.uuid4()
    sub_crit_1_uuid = uuid.uuid4()
    sub_crit_2_uuid = uuid.uuid4()
    sub_crit_3_uuid = uuid.uuid4()
    sub_crit_4_uuid = uuid.uuid4()
    assessment_1_uuid = uuid.uuid4()
    assessment_2_uuid = uuid.uuid4()

    assessment_1 = Assessment(
        id=assessment_1_uuid,
        compliance_status="great",
        application_id="amazing",
        round_id="COF",
        fund_id="YUM",
    )

    assessment_2 = Assessment(
        id=assessment_2_uuid,
        compliance_status="great111",
        application_id="amazing111",
        round_id="winter",
        fund_id="funding-service-design",
    )

    criteria_1 = Criteria(
        id=crit_1_uuid,
        criteria_name="strategy",
        round_id="COF",
    )

    criteria_2 = Criteria(
        id=crit_2_uuid,
        criteria_name="deliverability",
        round_id="COF2",
    )

    criteria_3 = Criteria(
        id=crit_3_uuid,
        criteria_name="value_for_money",
        round_id="COF2",
    )

    sub_criteria_1 = SubCriteria(
        id=sub_crit_1_uuid,
        criteria_id=crit_1_uuid,
        sub_criteria_title="something",
    )

    sub_criteria_2 = SubCriteria(
        id=sub_crit_2_uuid,
        criteria_id=crit_2_uuid,
        sub_criteria_title="nothing",
    )

    sub_criteria_3 = SubCriteria(
        id=sub_crit_3_uuid,
        criteria_id=crit_2_uuid,
        sub_criteria_title="nothing",
    )

    sub_criteria_4 = SubCriteria(
        id=sub_crit_4_uuid,
        criteria_id=crit_3_uuid,
        sub_criteria_title="nothing",
    )

    score_justification = ScoresJustifications(
        created_at=datetime.datetime.strptime(
            "2022-07-07T09:11:38.240578Z", "%Y-%m-%dT%H:%M:%S.%fZ"
        ),
        id=sub_crit_1_uuid,
        assessment_id=assessment_1_uuid,
        score=5,
        justification="wow",
        assessor_user_id="person_1",
    )

    score_justification_2 = ScoresJustifications(
        created_at=datetime.datetime.strptime(
            "2022-07-07T09:11:38.240578Z", "%Y-%m-%dT%H:%M:%S.%fZ"
        ),
        id=sub_crit_2_uuid,
        assessment_id=assessment_2_uuid,
        score=2,
        justification="wow",
        assessor_user_id="person_1",
    )

    score_justification_3 = ScoresJustifications(
        created_at=datetime.datetime.strptime(
            "2022-07-07T09:11:38.240578Z", "%Y-%m-%dT%H:%M:%S.%fZ"
        ),
        id=sub_crit_1_uuid,
        assessment_id=assessment_2_uuid,
        score=3,
        justification="wow",
        assessor_user_id="person_1",
    )

    score_justification_4 = ScoresJustifications(
        created_at=datetime.datetime.strptime(
            "2022-07-07T09:11:38.240578Z", "%Y-%m-%dT%H:%M:%S.%fZ"
        ),
        id=sub_crit_3_uuid,
        assessment_id=assessment_2_uuid,
        score=5,
        justification="wow",
        assessor_user_id="person_1",
    )

    score_justification_5 = ScoresJustifications(
        created_at=datetime.datetime.strptime(
            "2022-07-07T09:11:38.240578Z", "%Y-%m-%dT%H:%M:%S.%fZ"
        ),
        id=sub_crit_4_uuid,
        assessment_id=assessment_2_uuid,
        score=5,
        justification="wow",
        assessor_user_id="person_1",
    )

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

        db.session.add(cls.assessment_1)
        db.session.commit()

        db.session.add(cls.criteria_1)
        db.session.commit()

        db.session.add(cls.criteria_2)
        db.session.commit()

        db.session.add(cls.criteria_3)
        db.session.commit()

        db.session.add(cls.sub_criteria_1)
        db.session.commit()

        db.session.add(cls.sub_criteria_2)
        db.session.commit()

        db.session.add(cls.sub_criteria_3)
        db.session.commit()

        db.session.add(cls.sub_criteria_4)
        db.session.commit()

        db.session.add(cls.score_justification)
        db.session.commit()

        db.session.add(cls.score_justification_2)
        db.session.commit()

        db.session.add(cls.score_justification_3)
        db.session.commit()

        db.session.add(cls.score_justification_4)
        db.session.commit()

        db.session.add(cls.score_justification_5)
        db.session.commit()

        db.session.add(cls.assessment_2)

        sub_criteria_5 = SubCriteria(
            id="123e4567-e89b-12d3-a456-426655440001",
            round_id="hello",
            criteria_id="hi",
            sub_criteria_title="something",
        )

        db.session.add(sub_criteria_5)
        db.session.commit()

        sub_criteria_6 = SubCriteria(
            id="123e4567-e89b-12d3-a456-426655440002",
            round_id="ciao",
            criteria_id="cya",
            sub_criteria_title="nothing",
        )

        db.session.add(sub_criteria_6)
        db.session.commit()

        score_justification_6 = ScoresJustifications(
            id=uuid.UUID("123e4567-e89b-12d3-a456-426655440003"),
            created_at=datetime.datetime.strptime(
                "2022-07-07T09:11:38.240578Z", "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            sub_criteria_id="123e4567-e89b-12d3-a456-426655440001",
            assessment_id="123e4567-e89b-12d3-a456-426655440000",
            score=5,
            justification="wow",
            assessor_user_id="person_1",
        )

        db.session.add(score_justification_6)
        db.session.commit()
