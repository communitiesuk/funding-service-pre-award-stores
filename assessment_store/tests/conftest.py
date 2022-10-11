import pytest
from app import create_app
from colored import attr
from colored import fg
from colored import stylize
from db import db
from db.models.assessment import Assessment
from db.models.compliance import Compliance
from db.models.criteria import Criteria
from db.models.scores_justifications import ScoresJustifications
from db.models.sub_criteria import SubCriteria
from flask_migrate import upgrade

TEST_STYLE = fg("dark_orange_3a") + attr("bold")
seeded_assessment_ids = []
seeded_criteria = []
seeded_subcriteria = []
seeded_compliance_records = []
seeded_scores_justifications = []


@pytest.fixture(scope="session")
def app():
    """
    Creates the test client we will be using to test the responses
    from our app, this is a test fixture.
    :return: A flask test client.
    """
    app = create_app()
    with app.app_context():
        upgrade()
    yield app


@pytest.fixture(autouse=True)
def seed_data(db_session):
    print(stylize("in before_tests", TEST_STYLE))
    assessment_1 = Assessment(
        compliance_status="UNASSESSED",
        application_id="app_id_existing",
        round_id="round_1",
        fund_id="fund_1",
    )
    assessment_2 = Assessment(
        compliance_status="UNASSESSED",
        application_id="app_id_123",
        round_id="round_1",
        fund_id="fund_1",
    )
    db.session.add(assessment_1)
    db.session.add(assessment_2)
    db.session.commit()
    seeded_assessment_ids.append(assessment_1.id)
    seeded_assessment_ids.append(assessment_2.id)

    seeded_criteria.append(
        Criteria(
            criteria_name="strategy",
            round_id="round_1",
            fund_id="fund_1",
        )
    )
    seeded_criteria.append(
        Criteria(
            criteria_name="deliverability",
            round_id="round_1",
            fund_id="fund_1",
        )
    )
    seeded_criteria.append(
        Criteria(
            criteria_name="value_for_money",
            round_id="round_1",
            fund_id="fund_1",
        )
    )

    for c in seeded_criteria:
        db.session.add(c)
    db.session.commit()

    seeded_subcriteria.append(
        SubCriteria(
            criteria_id=seeded_criteria[0].id,
            sub_criteria_title="something",
        )
    )
    seeded_subcriteria.append(
        SubCriteria(
            criteria_id=seeded_criteria[1].id,
            sub_criteria_title="nothing",
        )
    )

    seeded_subcriteria.append(
        SubCriteria(
            criteria_id=seeded_criteria[2].id,
            sub_criteria_title="nothing",
        )
    )

    seeded_subcriteria.append(
        SubCriteria(
            criteria_id=seeded_criteria[2].id,
            sub_criteria_title="nothing",
        )
    )

    for s in seeded_subcriteria:
        db.session.add(s)
    db.session.commit()

    seeded_compliance_records.append(
        Compliance(
            assessment_id=seeded_assessment_ids[1],
            sub_criteria_id=seeded_subcriteria[1].id,
            is_compliant=True,
        )
    )

    for cr in seeded_compliance_records:
        db.session.add(cr)
    db.session.commit()

    seeded_scores_justifications.append(
        ScoresJustifications(
            assessment_id=seeded_assessment_ids[1],
            sub_criteria_id=seeded_subcriteria[0].id,
            score=0,
            justification="wow0",
            assessor_user_id="person_1",
        )
    )
    seeded_scores_justifications.append(
        ScoresJustifications(
            assessment_id=seeded_assessment_ids[1],
            sub_criteria_id=seeded_subcriteria[1].id,
            score=1,
            justification="wow1",
            assessor_user_id="person_1",
        )
    )
    seeded_scores_justifications.append(
        ScoresJustifications(
            assessment_id=seeded_assessment_ids[1],
            sub_criteria_id=seeded_subcriteria[2].id,
            score=2,
            justification="wow2",
            assessor_user_id="person_1",
        )
    )
    seeded_scores_justifications.append(
        ScoresJustifications(
            assessment_id=seeded_assessment_ids[1],
            sub_criteria_id=seeded_subcriteria[2].id,
            score=2,
            justification="not great",
            assessor_user_id="person_2",
        )
    )

    for sj in seeded_scores_justifications:
        db.session.add(sj)
    db.session.commit()

    yield

    #  Do some cleanup
    seeded_assessment_ids.clear()
    seeded_criteria.clear()
    seeded_subcriteria.clear()
    seeded_compliance_records.clear()
    seeded_scores_justifications.clear()


@pytest.fixture(scope="session")
def _db(app):
    """
    Provide the transactional fixtures with access
    to the database via a Flask-SQLAlchemy
    database connection.
    """
    return db


@pytest.fixture(autouse=True)
def enable_transactional_tests(db_session):
    pass
