# flake8: noqa
from uuid import uuid4

from config.mappings.cof_mapping_parts.cof_r2_scored_criteria import (
    scored_criteria as cof_scored_criteria_r2,
)
from config.mappings.cof_mapping_parts.cof_r2_unscored_sections import (
    unscored_sections as cof_unscored_sections_r2,
)
from config.mappings.nstf_mapping_parts.nstf_r2_scored_criteria import (
    scored_criteria as nstf_scored_criteria,
)
from config.mappings.nstf_mapping_parts.nstf_r2_unscored_sections import (
    unscored_sections as nstf_unscored_sections,
)
from config.mappings.cof_mapping_parts.cof_r3_scored_criteria import (
    scored_criteria as cof_scored_criteria_r3,
)
from config.mappings.cof_mapping_parts.cof_r3_unscored_sections import (
    unscored_sections as cof_unscored_sections_r3,
)

cof_r2w2_assessment_mapping = {
    "schema_id": "cof_r2w2_assessment",
    "unscored_sections": cof_unscored_sections_r2,
    "scored_criteria": cof_scored_criteria_r2,
}

cof_r2w3_assessment_mapping = {
    "schema_id": "cof_r2w3_assessment",
    "unscored_sections": cof_unscored_sections_r2,
    "scored_criteria": cof_scored_criteria_r2,
}

nstf_r2_assessment_mapping = {
    "schema_id": "nstf_r2_assessment",
    "unscored_sections": nstf_unscored_sections,
    "scored_criteria": nstf_scored_criteria,
}

cof_r3w1_assessment_mapping = {
    "schema_id": "cof_r3w1_assessment",
    "unscored_sections": cof_unscored_sections_r3,
    "scored_criteria": cof_scored_criteria_r3,
}

COF_FUND_ID = "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4"
COF_ROUND_2_ID = "c603d114-5364-4474-a0c4-c41cbf4d3bbd"
COF_ROUND_2_W3_ID = "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f"
COF_ROUND_3_W1_ID = "e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762"

NSTF_FUND_ID = "13b95669-ed98-4840-8652-d6b7a19964db"
NSTF_ROUND_2_ID = "fc7aa604-989e-4364-98a7-d1234271435a"

fund_round_to_assessment_mapping = {
    f"{COF_FUND_ID}:{COF_ROUND_2_ID}": cof_r2w2_assessment_mapping,
    f"{COF_FUND_ID}:{COF_ROUND_2_W3_ID}": cof_r2w3_assessment_mapping,
    f"{NSTF_FUND_ID}:{NSTF_ROUND_2_ID}": nstf_r2_assessment_mapping,
    f"{COF_FUND_ID}:{COF_ROUND_3_W1_ID}": cof_r3w1_assessment_mapping,
}

fund_round_mapping_config = {
    "COFR2W2": {
        "fund_id": COF_FUND_ID,
        "round_id": COF_ROUND_2_ID,
        "type_of_application": "COF",
    },
    "COFR2W3": {
        "fund_id": COF_FUND_ID,
        "round_id": COF_ROUND_2_W3_ID,
        "type_of_application": "COF",
    },
    "COFR3W1": {
        "fund_id": COF_FUND_ID,
        "round_id": COF_ROUND_3_W1_ID,
        "type_of_application": "COF",
    },
    "NSTFR2": {
        "fund_id": NSTF_FUND_ID,
        "round_id": NSTF_ROUND_2_ID,
        "type_of_application": "NSTF",
    },
    "RANDOM_FUND_ROUND": {
        "fund_id": uuid4(),
        "round_id": uuid4(),
        "type_of_application": "RFR",
    },
}
