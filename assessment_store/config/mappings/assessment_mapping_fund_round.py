from config.mappings.assessment_mapping import (
    cof_r2w2_assessment_mapping as cof_r2w2,
)
from fsd_utils import CommonConfig

fund_round_to_assessment_mapping = {
    f"{CommonConfig.COF_FUND_ID}:{CommonConfig.COF_ROUND_2_ID}": cof_r2w2,
}


def transform_to_assessor_task_list_metadata(
    fund_id: str, round_id: str
) -> tuple[dict, dict]:
    mapping = fund_round_to_assessment_mapping[f"{fund_id}:{round_id}"]

    sections = [
        {
            "name": s["name"],
            "sub_criterias": [
                {"name": sc["name"], "id": sc["id"]}
                for sc in s["sub_criteria"]
            ],
        }
        for s in mapping["unscored_sections"]
    ]

    criterias = [
        {
            "name": c["name"],
            "total_criteria_score": -1,  # TODO: Get dynamic state.
            "total_criteria_score_possible": -1,  # TODO: ^^^
            "weighting": c["weighting"],
            "sub_criterias": [
                {
                    "name": sc["name"],
                    "id": sc["id"],
                    "score": -1,  # TODO: Get dynamic state.
                    "theme_count": len(sc["themes"]),
                    "status": "Not started",  # TODO: Get dynamic state.
                }
                for sc in c["sub_criteria"]
            ],
        }
        for c in mapping["scored_criteria"]
    ]

    return sections, criterias
