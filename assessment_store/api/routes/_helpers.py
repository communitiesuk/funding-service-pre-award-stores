from config.mappings.assessment_mapping_fund_round import fund_round_to_assessment_mapping


def transform_to_assessor_task_list_metadata(
        fund_id: str, round_id: str
) -> tuple[dict, dict]:
    mapping = fund_round_to_assessment_mapping[f"{fund_id}:{round_id}"]

    sections = [
        {
            "name": s["name"],
            "sub_criterias": [
                {
                    "name": sc["name"],
                    "id": sc["id"],
                    "first_theme_id": sc["themes"][0]["id"],
                }
                for sc in s["sub_criteria"]
            ],
        }
        for s in mapping["unscored_sections"]
    ]

    criterias = [
        {
            "name": c["name"],
            "total_criteria_score": -1,  # TODO(FS-2000): Get dynamic state.
            "total_criteria_score_possible": -1,  # TODO(FS-2000): ^^^
            "weighting": c["weighting"],
            "sub_criterias": [
                {
                    "name": sc["name"],
                    "id": sc["id"],
                    "score": -1,  # TODO(FS-2000): Get dynamic state.
                    "theme_count": len(sc["themes"]),
                    "status": "Not started",  # TODO(FS-2000): Get dynamic state.
                    "first_theme_id": sc["themes"][0]["id"],
                }
                for sc in c["sub_criteria"]
            ],
        }
        for c in mapping["scored_criteria"]
    ]

    return sections, criterias
