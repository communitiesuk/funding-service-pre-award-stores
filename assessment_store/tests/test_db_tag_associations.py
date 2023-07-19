import pytest
from api.routes.assessment_routes import get_tags_associated_with_assessment
from db.models.assessment_record import AssessmentRecord
from db.queries.assessment_records.queries import associate_assessment_tags
from sqlalchemy import select
from tests.conftest import test_input_data


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_associate_tags(_db, seed_application_records, seed_tags):
    app_id = seed_application_records[0]["application_id"]
    new_tags = [
        {"id": tag["id"], "user_id": "1d49a41c-a13e-41ab-a89c-240b3de3fbda"}
        for tag in seed_tags
    ]
    stmt = select(AssessmentRecord).where(
        AssessmentRecord.application_id == app_id
    )
    app = _db.session.scalars(stmt).one()
    assert len(app.tag_associations) == 0

    associate_assessment_tags(app_id, new_tags)

    app = _db.session.scalars(stmt).one()
    assert len(app.tag_associations) == len(new_tags)

    seeded_tags_ids = [tag["id"] for tag in new_tags]
    associated_tag_ids = [str(t_a.tag_id) for t_a in app.tag_associations]
    assert set(seeded_tags_ids) == set(associated_tag_ids)


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_that_calling_with_the_same_tags_doesnt_duplicate_association(
    _db, seed_application_records, seed_tags
):
    app_id = seed_application_records[0]["application_id"]
    new_tags = [
        {"id": tag["id"], "user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93"}
        for tag in seed_tags
    ]
    stmt = select(AssessmentRecord).where(
        AssessmentRecord.application_id == app_id
    )
    app = _db.session.scalars(stmt).one()
    assert len(app.tag_associations) == 0

    associate_assessment_tags(app_id, new_tags)
    associate_assessment_tags(app_id, new_tags)

    app = _db.session.scalars(stmt).one()
    assert len(app.tag_associations) == len(new_tags)

    seeded_tags_ids = [tag["id"] for tag in new_tags]
    associated_tag_ids = [str(t_a.tag_id) for t_a in app.tag_associations]
    assert set(seeded_tags_ids) == set(associated_tag_ids)


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_tag_association_disassociation_workflow_is_working_correctly(
    _db, seed_application_records, seed_tags
):
    app_id = seed_application_records[0]["application_id"]
    new_tags = [
        {"id": tag["id"], "user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93"}
        for tag in seed_tags
    ]
    stmt = select(AssessmentRecord).where(
        AssessmentRecord.application_id == app_id
    )
    app = _db.session.scalars(stmt).one()
    assert len(app.tag_associations) == 0

    # associate two tags
    associate_assessment_tags(app_id, new_tags)
    tags = get_tags_associated_with_assessment(app_id)
    assert len(tags) == len(new_tags)

    # associate a single tag and expect other tag to be disassociated
    updated_tags = [new_tags[0]]
    associate_assessment_tags(app_id, updated_tags)
    actual_tags = get_tags_associated_with_assessment(app_id)
    assert len(actual_tags) == len(updated_tags)
    updated_tag_ids = [tag["id"] for tag in updated_tags]
    actual_tag_ids = [t_a["tag_id"] for t_a in actual_tags]
    assert set(updated_tag_ids) == set(actual_tag_ids)

    # associate two tags again
    associate_assessment_tags(app_id, new_tags)
    actual_tags = get_tags_associated_with_assessment(app_id)
    assert len(actual_tags) == len(new_tags)

    # associate no tags and expect all associated tags to be removed
    associate_assessment_tags(app_id, [])
    actual_tags = get_tags_associated_with_assessment(app_id)
    assert actual_tags == None  # noqa: E711


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_tag_association_history_is_retained_for_reassociated_tags(
    _db, seed_application_records, seed_tags
):
    """
    When a tag is associated we record the time and user
    if this tag is disassociated the associated value of that tag is set to False
    when another tag is raised for an application for a tag with the same tag_ig,
    ensure we create a new record for this
    """
    app_id = seed_application_records[0]["application_id"]
    new_tags = [
        {"id": tag["id"], "user_id": "5dd2b7d8-12f0-482f-b64b-8809b19baa93"}
        for tag in seed_tags
    ]
    single_tag = [new_tags[0]]

    stmt = select(AssessmentRecord).where(
        AssessmentRecord.application_id == app_id
    )
    app = _db.session.scalars(stmt).one()
    # check there are no tags associated or disassociated for an app
    assert len(app.tag_associations) == 0

    # associate a single tag
    associate_assessment_tags(app_id, single_tag)
    app = _db.session.scalars(stmt).one()
    # check total associated or disassociated tags
    assert len(app.tag_associations) == 1
    # check total associated tags
    tags = get_tags_associated_with_assessment(app_id)
    assert len(tags) == 1
    assert tags[0]["user_id"] == "5dd2b7d8-12f0-482f-b64b-8809b19baa93"

    # disassociate the tag
    associate_assessment_tags(app_id, [])
    tags = get_tags_associated_with_assessment(app_id)
    app = _db.session.scalars(stmt).one()
    # check total associated or disassociated tags
    assert len(app.tag_associations) == 1
    # check total associated tags
    tags = get_tags_associated_with_assessment(app_id)
    assert tags == None  # noqa: E711

    # associate the single tag again as a different user
    single_tag[0]["user_id"] = "2d8e6a2e-aa22-417f-a138-90569c8b238f"
    associate_assessment_tags(app_id, single_tag)
    app = _db.session.scalars(stmt).one()
    # check total associated or disassociated tags
    assert len(app.tag_associations) == 2
    # check total associated tags
    tags = get_tags_associated_with_assessment(app_id)
    assert len(tags) == 1
    assert tags[0]["user_id"] == "2d8e6a2e-aa22-417f-a138-90569c8b238f"

    # disassociate the tag
    associate_assessment_tags(app_id, [])
    tags = get_tags_associated_with_assessment(app_id)
    app = _db.session.scalars(stmt).one()
    # check total associated or disassociated tags
    assert len(app.tag_associations) == 2
    # check total associated tags
    tags = get_tags_associated_with_assessment(app_id)
    assert tags == None  # noqa: E711
