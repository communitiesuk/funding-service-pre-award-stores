# flake8: noqa
from config.mappings.mapping_parts.cof_r2_scored_criteria import (
    scored_criteria,
)
from config.mappings.mapping_parts.cof_r2_unscored_sections import (
    unscored_sections,
)

cof_r2w2_assessment_mapping = {
    "schema_id": "cof_r2w2_assessment",
    "unscored_sections": unscored_sections,
    "scored_criteria": scored_criteria,
}

cof_r2w3_assessment_mapping = {
    "schema_id": "cof_r2w3_assessment",
    "unscored_sections": unscored_sections,
    "scored_criteria": scored_criteria,
}

COF_FUND_ID = "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4"
COF_ROUND_2_ID = "c603d114-5364-4474-a0c4-c41cbf4d3bbd"
COF_ROUND_2_W3_ID = "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f"

fund_round_to_assessment_mapping = {
    f"{COF_FUND_ID}:{COF_ROUND_2_ID}": cof_r2w2_assessment_mapping,
    f"{COF_FUND_ID}:{COF_ROUND_2_W3_ID}": cof_r2w3_assessment_mapping,
}
