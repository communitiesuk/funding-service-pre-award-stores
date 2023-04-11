# flake8: noqa
from config.mappings.mapping_parts.cof_r2_scored_criteria import (
    scored_criteria,
)
from config.mappings.mapping_parts.cof_r2_unscored_sections import (
    unscored_sections,
)
from fsd_utils import CommonConfig

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

fund_round_to_assessment_mapping = {
    f"{CommonConfig.COF_FUND_ID}:{CommonConfig.COF_ROUND_2_ID}": cof_r2w2_assessment_mapping,
    f"{CommonConfig.COF_FUND_ID}:{CommonConfig.COF_ROUND_2_W3_ID}": cof_r2w3_assessment_mapping,
}
