from db.queries import get_round_by_id
from db.schemas.round import RoundSchema
from scripts.data_updates.FS2910_ns_links import update_rounds_with_links


def test_update_links_present(seed_dynamic_data):
    r = get_round_by_id(
        seed_dynamic_data["funds"][0]["id"],
        seed_dynamic_data["funds"][0]["rounds"][0]["id"],
    )
    round_data = RoundSchema().dump(r)
    round_data["privacy_notice"] = "new privacy notice"
    round_data["prospectus"] = "new prospectus"

    update_rounds_with_links([round_data])

    r = get_round_by_id(
        seed_dynamic_data["funds"][0]["id"],
        seed_dynamic_data["funds"][0]["rounds"][0]["id"],
    )

    assert r.privacy_notice == "new privacy notice"
    assert r.prospectus == "new prospectus"


def test_update_links_not_present(seed_dynamic_data):
    r = get_round_by_id(
        seed_dynamic_data["funds"][0]["id"],
        seed_dynamic_data["funds"][0]["rounds"][1]["id"],
    )
    round_data = RoundSchema().dump(r)
    round_data["privacy_notice"] = ""
    round_data["prospectus"] = ""

    update_rounds_with_links([round_data])

    r = get_round_by_id(
        seed_dynamic_data["funds"][0]["id"],
        seed_dynamic_data["funds"][0]["rounds"][1]["id"],
    )

    assert r.privacy_notice == "http://google.com"
    assert r.prospectus == "http://google.com"
