from config.mappings.assessment_mapping_fund_round import (
    fund_round_to_assessment_mapping,
)
from db.models.assessment_record.enums import Status


def _derive_status(
    score_map: dict, comment_map: dict, sub_criteria_id: str
) -> str:
    if sub_criteria_id in score_map:
        return Status.COMPLETED.name  # if we've scored, we've completed
    if sub_criteria_id in comment_map:
        return (
            Status.IN_PROGRESS.name
        )  # if we've commented, but not scored, we're in progress

    # if we haven't commented or scored, we're not started
    return Status.NOT_STARTED.name


def transform_to_assessor_task_list_metadata(
    fund_id: str, round_id: str, score_map: dict, comment_map: dict
) -> tuple[dict, dict]:
    mapping = fund_round_to_assessment_mapping[f"{fund_id}:{round_id}"]

    sections = [
        {
            "name": s["name"],
            "sub_criterias": [
                {
                    "name": sc["name"],
                    "id": sc["id"],
                }
                for sc in s["sub_criteria"]
            ],
        }
        for s in mapping["unscored_sections"]
    ]

    criterias = [
        {
            "name": c["name"],
            "total_criteria_score": sum(
                score_map.get(sc["id"], 0) for sc in c["sub_criteria"]
            ),
            "total_criteria_score_possible": sum(5 for _ in c["sub_criteria"]),
            "weighting": c["weighting"],
            "sub_criterias": [
                {
                    "name": sc["name"],
                    "id": sc["id"],
                    "score": score_map.get(sc["id"]),
                    "theme_count": len(sc["themes"]),
                    "status": _derive_status(score_map, comment_map, sc["id"]),
                }
                for sc in c["sub_criteria"]
            ],
        }
        for c in mapping["scored_criteria"]
    ]

    return sections, criterias
