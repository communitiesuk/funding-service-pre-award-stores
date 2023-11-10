# flake8: noqa
from uuid import uuid4

from config.mappings.cof_mapping_parts.r2_scored_criteria import (
    scored_criteria as cof_scored_criteria_r2,
)
from config.mappings.cof_mapping_parts.r2_unscored_sections import (
    unscored_sections as cof_unscored_sections_r2,
)
from config.mappings.cof_mapping_parts.r3_scored_criteria import (
    scored_criteria as cof_scored_criteria_r3,
)
from config.mappings.cof_mapping_parts.r3_unscored_sections import (
    unscored_sections as cof_unscored_sections_r3,
)
from config.mappings.cof_mapping_parts.r3w2_scored_criteria import (
    scored_criteria as cof_scored_criteria_r3w2,
)
from config.mappings.cof_mapping_parts.r3w2_unscored_sections import (
    unscored_sections as cof_unscored_sections_r3w2,
)
from config.mappings.cyp_mapping_parts.r1_scored_criteria import (
    scored_criteria as cyp_scored_criteria_r1,
)
from config.mappings.cyp_mapping_parts.r1_unscored_criteria import (
    unscored_sections as cyp_unscored_sections_r1,
)
from config.mappings.dpif_mappping_parts.r2_scored_criteria import (
    scored_criteria as dpif_scored_criteria,
)
from config.mappings.dpif_mappping_parts.r2_unscored_criteria import (
    unscored_sections as dpif_unscored_sections,
)
from config.mappings.nstf_mapping_parts.r2_scored_criteria import (
    scored_criteria as nstf_scored_criteria,
)
from config.mappings.nstf_mapping_parts.r2_unscored_sections import (
    unscored_sections as nstf_unscored_sections,
)

# FUND AND ROUND CONFIGURATION (Extracted from the fund store)
COF_FUND_ID = "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4"
COF_ROUND_2_ID = "c603d114-5364-4474-a0c4-c41cbf4d3bbd"
COF_ROUND_2_W3_ID = "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f"
COF_ROUND_3_W1_ID = "e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762"
COF_ROUND_3_W2_ID = "6af19a5e-9cae-4f00-9194-cf10d2d7c8a7"

NSTF_FUND_ID = "13b95669-ed98-4840-8652-d6b7a19964db"
NSTF_ROUND_2_ID = "fc7aa604-989e-4364-98a7-d1234271435a"

CYP_FUND_ID = "1baa0f68-4e0a-4b02-9dfe-b5646f089e65"
CYP_ROUND_1_ID = "888aae3d-7e2c-4523-b9c1-95952b3d1644"

DPIF_FUND_ID = "f493d512-5eb4-11ee-8c99-0242ac120002"
DPIF_ROUND_2_ID = "0059aad4-5eb5-11ee-8c99-0242ac120002"

# ASSESSMENT DISPLAY CONFIGURATION

fund_round_to_assessment_mapping = {
    f"{COF_FUND_ID}:{COF_ROUND_2_ID}": {
        "schema_id": "cof_r2w2_assessment",
        "unscored_sections": cof_unscored_sections_r2,
        "scored_criteria": cof_scored_criteria_r2,
    },
    f"{COF_FUND_ID}:{COF_ROUND_2_W3_ID}": {
        "schema_id": "cof_r2w3_assessment",
        "unscored_sections": cof_unscored_sections_r2,
        "scored_criteria": cof_scored_criteria_r2,
    },
    f"{NSTF_FUND_ID}:{NSTF_ROUND_2_ID}": {
        "schema_id": "nstf_r2_assessment",
        "unscored_sections": nstf_unscored_sections,
        "scored_criteria": nstf_scored_criteria,
    },
    f"{COF_FUND_ID}:{COF_ROUND_3_W1_ID}": {
        "schema_id": "cof_r3w1_assessment",
        "unscored_sections": cof_unscored_sections_r3,
        "scored_criteria": cof_scored_criteria_r3,
    },
    f"{COF_FUND_ID}:{COF_ROUND_3_W2_ID}": {
        "schema_id": "cof_r3w2_assessment",
        "unscored_sections": cof_unscored_sections_r3w2,
        "scored_criteria": cof_scored_criteria_r3w2,
    },
    f"{CYP_FUND_ID}:{CYP_ROUND_1_ID}": {
        "schema_id": "cyp_r1_assessment",
        "unscored_sections": cyp_unscored_sections_r1,
        "scored_criteria": cyp_scored_criteria_r1,
    },
    f"{DPIF_FUND_ID}:{DPIF_ROUND_2_ID}": {
        "schema_id": "dpif_r2_assessment",
        "unscored_sections": dpif_unscored_sections,
        "scored_criteria": dpif_scored_criteria,
    },
}

# Key information for header fields (within JSON)
# We extract a number of field to display at a higher level
# in the assessment view (assessor dashboard view), these
# bits of information are extracted from the application_json


fund_round_data_key_mappings = {
    "COFR2W2": {
        "location": "yEmHpp",
        "asset_type": "yaQoxU",
        "funding_one": "JzWvhj",
        "funding_two": "jLIgoi",
    },
    "COFR2W3": {
        "location": "yEmHpp",
        "asset_type": "yaQoxU",
        "funding_one": "JzWvhj",
        "funding_two": "jLIgoi",
    },
    "COFR3W1": {
        "location": "EfdliG",
        "asset_type": "oXGwlA",
        "funding_one": "ABROnB",
        "funding_two": "cLDRvN",
    },
    "COFR3W2": {
        "location": "EfdliG",
        "asset_type": "oXGwlA",
        "funding_one": "ABROnB",
        "funding_two": ["tSKhQQ", "UyaAHw"],
        "funding_field_type": "multiInputField",
    },
    "NSTFR2": {
        "location": "mhYQzL",
        "asset_type": None,
        "funding_one": ["mCbbyN", "iZdZrr"],
        "funding_two": ["XsAoTv", "JtBjFp"],
        "funding_field_type": "multiInputField",
    },
    "CYPR1": {
        "location": "rmBPvK",
        "asset_type": None,
        "funding_one": None,
        "funding_two": ["JXKUcj", "OnPeeS"],  # only revenue funding for cyp
    },
    "DPIFR2": {
        "location": None,
        "asset_type": None,
        "funding_one": None,
        "funding_two": None,
    },
}

applicant_info_mapping = {
    NSTF_FUND_ID: {
        "OUTPUT_TRACKER": {
            "form_fields": {
                "opFJRm": {"en": {"title": "Organisation name"}},
                "fUMWcd": {"en": {"title": "Name of lead contact"}},
                "CDEwxp": {"en": {"title": "Lead contact email address"}},
                "nURkuc": {"en": {"title": "Local Authority"}},
                "pVBwci": {
                    "en": {
                        "title": "Revenue for 1 April 2023 to 31 March 2024"
                    }
                },
                "WDouQc": {
                    "en": {
                        "title": "Revenue for 1 April 2024 to 31 March 2025"
                    }
                },
                "SGjmSM": {
                    "en": {
                        "title": "Capital for 1 April 2023 to 31 March 2024"
                    }
                },
                "wTdyhk": {
                    "en": {
                        "title": "Capital for 1 April 2024 to 31 March 2025"
                    }
                },
                "GRWtfV": {
                    "en": {
                        "title": "Revenue for 1 April 2023 to 31 March 2024"
                    }
                },
                "zvPzXN": {
                    "en": {
                        "title": "Revenue for 1 April 2024 to 31 March 2025"
                    }
                },
                "QUCvFy": {
                    "en": {
                        "title": "Capital for 1 April 2023 to 31 March 2024"
                    }
                },
                "pppiYl": {
                    "en": {
                        "title": "Capital for 1 April 2024 to 31 March 2025"
                    }
                },
                "AVShTf": {"en": {"title": "Region"}},
            },
            "score_fields": {
                "Application ID",
                "Short ID",
                "Score Subcriteria",
                "Score",
                "Score Date",
                "Score Time",
            },
        },
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "fUMWcd": {"en": {"title": "Name of lead contact"}},
                "CDEwxp": {"en": {"title": "Lead contact email address"}},
                "DvBqCJ": {"en": {"title": "Lead contact telephone number"}},
                "mhYQzL": {"en": {"title": "Organisation address"}},
            }
        },
    },
    COF_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "SnLGJE": {
                    "en": {"title": "Name of lead contact"},
                    "cy": {"title": "Enw'r cyswllt arweiniol"},
                },
                "NlHSBg": {
                    "en": {"title": "Lead contact email address"},
                    "cy": {"title": "Cyfeiriad e-bost y cyswllt arweiniol"},
                },
                "FhBkJQ": {
                    "en": {"title": "Lead contact telephone number"},
                    "cy": {"title": "Rhif ffôn y cyswllt arweiniol"},
                },
                "ZQolYb": {
                    "en": {"title": "Organisation address"},
                    "cy": {"title": "Cyfeiriad y sefydliad"},
                },
                "VhkCbM": {
                    "en": {"title": "Correspondence address"},
                    "cy": {"title": "Cyfeiriad gohebu"},
                },
            }
        },
        "OUTPUT_TRACKER": {},
    },
    CYP_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "rKHBnt": {"en": {"title": "Name of lead contact"}},
                "BKOHaM": {
                    "en": {"title": "Lead contact email address"},
                },
                "CyANDT": {
                    "en": {"title": "Lead contact telephone number"},
                },
                "rmBPvK": {
                    "en": {"title": "Registered organisation address"},
                },
                "smBPvK": {
                    "en": {"title": "Alternative organisation address"},
                },
            }
        },
        "OUTPUT_TRACKER": {},
    },
    CYP_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "JbmcJE": {"en": {"title": "Organisation name"}},
                "rmBPvK": {"en": {"title": "Registered organisation address"}},
                "smBPvK": {
                    "en": {
                        "title": "Alternative organisation address (optional)"
                    }
                },
                "jeocJE": {"en": {"title": "registered charity number"}},
                "JXKUcj": {
                    "en": {"title": "27 September 2023 to 31 March 2024"}
                },
                "OnPeeS": {"en": {"title": "1 April 2024 to 31 March 2025"}},
                "vYYoAC": {"en": {"title": "Cohort"}},
                "fHodTO": {
                    "en": {"title": "What is the main focus of your project?"}
                },
                "MADkNZ": {
                    "en": {
                        "title": "Give a brief summary of your project, including what you hope to achieve"
                    }
                },
                "tZoOKx": {"en": {"title": "Partner organisation details"}},
            }
        },
        "OUTPUT_TRACKER": {},
    },
    DPIF_FUND_ID: {
        "ASSESSOR_EXPORT": {},
        "OUTPUT_TRACKER": {},
    },
}

# APPLICATION SEEDING CONFIGURATION

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
    "COFR3W2": {
        "fund_id": COF_FUND_ID,
        "round_id": COF_ROUND_3_W2_ID,
        "type_of_application": "COF",
    },
    "NSTFR2": {
        "fund_id": NSTF_FUND_ID,
        "round_id": NSTF_ROUND_2_ID,
        "type_of_application": "NSTF",
    },
    "CYPR1": {
        "fund_id": CYP_FUND_ID,
        "round_id": CYP_ROUND_1_ID,
        "type_of_application": "CYP",
    },
    "DPIFR2": {
        "fund_id": DPIF_FUND_ID,
        "round_id": DPIF_ROUND_2_ID,
        "type_of_application": "DPIF",
    },
    "RANDOM_FUND_ROUND": {
        "fund_id": uuid4(),
        "round_id": uuid4(),
        "type_of_application": "RFR",
    },
}
