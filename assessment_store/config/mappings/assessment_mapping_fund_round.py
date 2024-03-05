# flake8: noqa
from uuid import uuid4

from config.mappings.cof_mapping_parts.eoi_unscored_sections import (
    unscored_sections as cof_unscored_sections_eoi,
)
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
from config.mappings.cof_mapping_parts.r3w3_scored_criteria import (
    scored_criteria as cof_scored_criteria_r3w3,
)
from config.mappings.cof_mapping_parts.r3w3_unscored_sections import (
    unscored_sections as cof_unscored_sections_r3w3,
)
from config.mappings.cof_mapping_parts.r4w1_scored_criteria import (
    scored_criteria as cof_scored_criteria_r4w1,
)
from config.mappings.cof_mapping_parts.r4w1_unscored_sections import (
    unscored_sections as cof_unscored_sections_r4w1,
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
COF_ROUND_3_W3_ID = "4efc3263-aefe-4071-b5f4-0910abec12d2"
COF_ROUND_4_W1_ID = "33726b63-efce-4749-b149-20351346c76e"
COF_EOI_FUND_ID = "54c11ec2-0b16-46bb-80d2-f210e47a8791"
COF_EOI_ROUND_ID = "6a47c649-7bac-4583-baed-9c4e7a35c8b3"

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
    f"{COF_FUND_ID}:{COF_ROUND_3_W3_ID}": {
        "schema_id": "cof_r3w3_assessment",
        "unscored_sections": cof_unscored_sections_r3w3,
        "scored_criteria": cof_scored_criteria_r3w3,
    },
    f"{COF_FUND_ID}:{COF_ROUND_4_W1_ID}": {
        "schema_id": "cof_r4w1_assessment",
        "unscored_sections": cof_unscored_sections_r4w1,
        "scored_criteria": cof_scored_criteria_r4w1,
    },
    f"{COF_EOI_FUND_ID}:{COF_EOI_ROUND_ID}": {
        "schema_id": "cof_eoi_assessment",
        "unscored_sections": cof_unscored_sections_eoi,
        "scored_criteria": [],
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
    "COFR3W3": {
        "location": "EfdliG",
        "asset_type": "oXGwlA",
        "funding_one": "ABROnB",
        "funding_two": ["tSKhQQ", "UyaAHw"],
        "funding_field_type": "multiInputField",
    },
    "COFR4W1": {
        "location": "EfdliG",
        "asset_type": "oXGwlA",
        "funding_one": "ABROnB",
        "funding_two": ["tSKhQQ", "UyaAHw"],
        "funding_field_type": "multiInputField",
    },
    "COFEOI": {
        "location": None,
        "asset_type": None,
        "funding_one": None,
        "funding_two": None,
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
                "pVBwci": {"en": {"title": "Revenue for 1 April 2023 to 31 March 2024"}},
                "WDouQc": {"en": {"title": "Revenue for 1 April 2024 to 31 March 2025"}},
                "SGjmSM": {"en": {"title": "Capital for 1 April 2023 to 31 March 2024"}},
                "wTdyhk": {"en": {"title": "Capital for 1 April 2024 to 31 March 2025"}},
                "GRWtfV": {"en": {"title": "Revenue for 1 April 2023 to 31 March 2024"}},
                "zvPzXN": {"en": {"title": "Revenue for 1 April 2024 to 31 March 2025"}},
                "QUCvFy": {"en": {"title": "Capital for 1 April 2023 to 31 March 2024"}},
                "pppiYl": {"en": {"title": "Capital for 1 April 2024 to 31 March 2025"}},
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
                "mhYQzL": {
                    "en": {
                        "title": "Organisation address",
                        "field_type": "ukAddressField",
                    }
                },
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
                    "en": {
                        "title": "Organisation address",
                        "field_type": "ukAddressField",
                    },
                    "cy": {
                        "title": "Cyfeiriad y sefydliad",
                        "field_type": "ukAddressField",
                    },
                },
                "VhkCbM": {
                    "en": {
                        "title": "Correspondence address",
                        "field_type": "ukAddressField",
                    },
                    "cy": {
                        "title": "Cyfeiriad gohebu",
                        "field_type": "ukAddressField",
                    },
                },
            }
        },
        "OUTPUT_TRACKER": {},
    },
    COF_EOI_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "eEaDGz": {
                    "en": {
                        "title": "Does your organisation plan both to receive the funding and run the project?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A yw eich sefydliad yn bwriadu cael y cyllid a rhedeg y prosiect?",
                        "field_type": "yesNoField",
                    },
                },
                "Ihjjyi": {
                    "en": {"title": "Type of asset", "field_type": "radiosField"},
                    "cy": {
                        "title": "Y math o ased",
                        "field_type": "radiosField",
                    },
                },
                "zurxox": {
                    "en": {"title": "Is the asset based in the UK?", "field_type": "yesNoField"},
                    "cy": {
                        "title": "A yw'r ased yn y DU?",
                        "field_type": "yesNoField",
                    },
                },
                "dnqIdW": {
                    "en": {"title": "Address of the asset", "field_type": "ukAddressField"},
                    "cy": {
                        "title": "Cyfeiriad yr ased",
                        "field_type": "ukAddressField",
                    },
                },
                "lLQmNb": {
                    "en": {"title": "Is the asset at risk?", "field_type": "yesNoField"},
                    "cy": {
                        "title": "A yw'r ased mewn perygl?",
                        "field_type": "yesNoField",
                    },
                },
                "ilMbMH": {
                    "en": {"title": "What is the risk to the asset?", "field_type": "checkboxesField"},
                    "cy": {
                        "title": "Beth yw'r perygl i'r ased?",
                        "field_type": "checkboxesField",
                    },
                },
                "fBhSNc": {
                    "en": {
                        "title": "Has the asset ever been used by or had significance to the community?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A yw'r ased erioed wedi cael ei ddefnyddio gan y gymuned neu wedi bod yn arwyddocaol iddi?",
                        "field_type": "yesNoField",
                    },
                },
                "cPcZos": {
                    "en": {"title": "Do you already own the asset?", "field_type": "yesNoField"},
                    "cy": {
                        "title": "",
                        "field_type": "",
                    },
                },
                "jOpXfi": {
                    "en": {"title": "Help with public authority", "field_type": "details"},
                    "cy": {
                        "title": "Help gydag awdurdod cyhoeddus",
                        "field_type": "details",
                    },
                },
                "XuAyrs": {
                    "en": {"title": "Does the asset belong to a public authority?", "field_type": "radiosField"},
                    "cy": {
                        "title": "A yw'r ased yn perthyn i awdurdod cyhoeddus?",
                        "field_type": "radiosField",
                    },
                },
                "oDhZlw": {
                    "en": {"title": "Stage purchasing asset", "field_type": "radiosField"},
                    "cy": {
                        "title": "Cam prynu'r ased",
                        "field_type": "radiosField",
                    },
                },
                "oXFEkV": {
                    "en": {
                        "title": "I confirm the information I've provided is correct",
                        "field_type": "checkboxesField",
                    },
                    "cy": {
                        "title": "Cadarnhaf fod y wybodaeth rwyf wedi'i darparu yn gywir",
                        "field_type": "checkboxesField",
                    },
                },
                "SMRWjl": {
                    "en": {"title": "Organisation name", "field_type": "textField"},
                    "cy": {
                        "title": "Enwau'r sefydliad",
                        "field_type": "textField",
                    },
                },
                "SxkwhF": {
                    "en": {"title": "Does your organisation have any alternative names?", "field_type": "yesNoField"},
                    "cy": {
                        "title": "A oes gan eich sefydliad unrhyw enwau amgen?",
                        "field_type": "yesNoField",
                    },
                },
                "OpeSdM": {
                    "en": {"title": "Organisation address", "field_type": "ukAddressField"},
                    "cy": {
                        "title": "Cyfeiriad y sefydliad",
                        "field_type": "ukAddressField",
                    },
                },
                "Fepkam": {
                    "en": {"title": "Help with organisation type", "field_type": "details"},
                    "cy": {
                        "title": "Help gyda'r math o sefydliad",
                        "field_type": "details",
                    },
                },
                "uYiLsv": {
                    "en": {"title": "Organisation classification", "field_type": "radiosField"},
                    "cy": {
                        "title": "Dosbarthiad y sefydliad",
                        "field_type": "radiosField",
                    },
                },
                "jGoBGp": {
                    "en": {"title": "Help with insolvency", "field_type": "details"},
                    "cy": {
                        "title": "Help with insolvency",
                        "field_type": "details",
                    },
                },
                "NcQSbU": {
                    "en": {
                        "title": "Is your organisation subject to any insolvency actions?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A yw eich sefydliad yn destun unrhyw gamau ansolfedd?",
                        "field_type": "yesNoField",
                    },
                },
                "qkNYMP": {
                    "en": {"title": "Alternative name 1", "field_type": "textField"},
                    "cy": {
                        "title": "Enw amgen 1",
                        "field_type": "textField",
                    },
                },
                "mVxvon": {
                    "en": {"title": "Alternative name 2", "field_type": "textField"},
                    "cy": {
                        "title": "Enw amgen 2",
                        "field_type": "textField",
                    },
                },
                "DaIVVm": {
                    "en": {"title": "Alternative name 3", "field_type": "textField"},
                    "cy": {
                        "title": "Enw amgen 3",
                        "field_type": "textField",
                    },
                },
                "aocRmv": {
                    "en": {"title": "What do you plan to use COF's funding for?", "field_type": "checkboxesField"},
                    "cy": {
                        "title": "At ba ddiben ydych chi'n bwriadu defnyddio cyllid o'r Gronfa Perchnogaeth Gymunedol?",
                        "field_type": "checkboxesField",
                    },
                },
                "foQgiy": {
                    "en": {
                        "title": "Will the leasehold have at least 15 years when your organisation submits a full application?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A fydd gan y lesddaliad o leiaf 15 mlynedd pan fydd eich sefydliad yn cyflwyno cais llawn?",
                        "field_type": "yesNoField",
                    },
                },
                "fZAMFv": {
                    "en": {
                        "title": "How much capital funding are you requesting from COF?",
                        "field_type": "numberField",
                    },
                    "cy": {
                        "title": "Faint o gyllid cyfalaf ydych chi'n gwneud cais amdano o'r Gronfa Perchnogaeth Gymunedol?",
                        "field_type": "numberField",
                    },
                },
                "oblxxv": {
                    "en": {"title": "Do you plan to request any revenue funding?", "field_type": "yesNoField"},
                    "cy": {
                        "title": "A ydych yn bwriadu gwneud cais am unrhyw gyllid refeniw?",
                        "field_type": "yesNoField",
                    },
                },
                "eOWKoO": {
                    "en": {"title": "Do you plan to secure match funding?", "field_type": "yesNoField"},
                    "cy": {
                        "title": "A ydych yn bwriadu sicrhau arian cyfatebol?",
                        "field_type": "yesNoField",
                    },
                },
                "BykoQQ": {
                    "en": {"title": "Where do you plan to source match funding?", "field_type": "checkboxesField"},
                    "cy": {
                        "title": "O ble rydych yn bwriadu cael arian cyfatebol?",
                        "field_type": "checkboxesField",
                    },
                },
                "yZxdeJ": {
                    "en": {"title": "Does your project include an element of housing?", "field_type": "yesNoField"},
                    "cy": {
                        "title": "A yw eich prosiect yn cynnwys elfen dai?",
                        "field_type": "yesNoField",
                    },
                },
                "UORyaF": {
                    "en": {"title": "Will you need planning permission for your project?", "field_type": "radiosField"},
                    "cy": {
                        "title": "A fydd angen caniatâd cynllunio ar gyfer eich prosiect?",
                        "field_type": "radiosField",
                    },
                },
                "jICagT": {
                    "en": {
                        "title": "What stage are you at in securing planning permission?",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "Pa gam ydych chi wedi'i gyrraedd yn y broses o sicrhau caniatâd cynllunio?",
                        "field_type": "radiosField",
                    },
                },
                "kWRuac": {
                    "en": {"title": "What progress have you made to secure this funding?", "field_type": "radiosField"},
                    "cy": {
                        "title": "Pa gynnydd ydych chi wedi'i wneud i sicrhau'r arian hwn?",
                        "field_type": "radiosField",
                    },
                },
                "iXmKyq": {
                    "en": {
                        "title": "Do you wish to be contacted by the development support provider, if eligible for in-depth support?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A hoffech i'r darparwr cymorth datblygu gysylltu â chi, os ydych yn gymwys i gael cymorth manwl?",
                        "field_type": "yesNoField",
                    },
                },
                "ObIBSx": {
                    "en": {
                        "title": "What are the main things you feel you need support with to submit a good COF application?",
                        "field_type": "checkboxesField",
                    },
                    "cy": {
                        "title": "Beth yw'r prif bethau y mae angen cymorth arnoch gyda nhw er mwyn cyflwyno cais da i'r Gronfa Perchnogaeth Gymunedol yn eich barn chi?",
                        "field_type": "checkboxesField",
                    },
                },
                "MxzEYq": {
                    "en": {"title": "Describe your project and its aims", "field_type": "freeTextField"},
                    "cy": {
                        "title": "Disgrifiwch eich prosiect a'i nodau",
                        "field_type": "freeTextField",
                    },
                },
                "xWnVof": {
                    "en": {"title": "Name of lead contact", "field_type": "textField"},
                    "cy": {
                        "title": "Enw'r prif unigolyn cyswllt",
                        "field_type": "textField",
                    },
                },
                "NQoGIm": {
                    "en": {"title": "Lead contact email address", "field_type": "emailAddressField"},
                    "cy": {
                        "title": "Cyfeiriad e-bost y prif unigolyn cyswllt",
                        "field_type": "emailAddressField",
                    },
                },
                "srxZmv": {
                    "en": {"title": "Lead contact telephone number", "field_type": "telephoneNumberField"},
                    "cy": {
                        "title": "Rhif ffôn y prif unigolyn cyswllt",
                        "field_type": "telephoneNumberField",
                    },
                },
            }
        },
        "OUTPUT_TRACKER": {},
    },
    CYP_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "JbmcJE": {"en": {"title": "Organisation name"}},
                "rmBPvK": {
                    "en": {
                        "title": "Registered organisation address",
                        "field_type": "ukAddressField",
                    }
                },
                "smBPvK": {
                    "en": {
                        "title": "Alternative organisation address (optional)",
                        "field_type": "ukAddressField",
                    }
                },
                "jeocJE": {"en": {"title": "registered charity number"}},
                "JXKUcj": {"en": {"title": "27 September 2023 to 31 March 2024"}},
                "OnPeeS": {"en": {"title": "1 April 2024 to 31 March 2025"}},
                "vYYoAC": {"en": {"title": "Cohort"}},
                "fHodTO": {"en": {"title": "What is the main focus of your project?"}},
                "MADkNZ": {"en": {"title": "Give a brief summary of your project, including what you hope to achieve"}},
                "tZoOKx": {"en": {"title": "Partner organisation details"}},
            }
        },
        "OUTPUT_TRACKER": {"form_fields": {"fHodTO": {"en": {"title": "What is the main focus of your project?"}}}},
    },
    DPIF_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "nYJiWy": {"en": {"title": "Organisation name"}},
                "uYsivE": {"en": {"title": "Project sponsor name"}},
                "xgrxxv": {"en": {"title": "Project sponsor email"}},
                "cPpwET": {"en": {"title": "Section 151 officer name"}},
                "EMukio": {"en": {"title": "Section 151 officer email"}},
                "AYmilW": {"en": {"title": "Lead contact name"}},
                "IRugBv": {"en": {"title": "Lead contact email"}},
                "JUgCya": {
                    "en": {
                        "title": "You have signed the Local Digital Declaration and agree to follow the 5 core principles"
                    }
                },
                "vbmqwB": {
                    "en": {
                        "title": "Your section 151 officer consents to the funds being carried over and spent in the next financial year (March 2024-25) and beyond if deemed necessary in project budget planning"
                    }
                },
                "EQffUz": {
                    "en": {
                        "title": "You agree to let all outputs from this work be published under open licence with a view to any organisation accessing, using or adopting them freely"
                    }
                },
                "kPYiQE": {"en": {"title": "The information you have provided is accurate"}},
            }
        },
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
    "COFR3W3": {
        "fund_id": COF_FUND_ID,
        "round_id": COF_ROUND_3_W3_ID,
        "type_of_application": "COF",
    },
    "COFR4W1": {
        "fund_id": COF_FUND_ID,
        "round_id": COF_ROUND_4_W1_ID,
        "type_of_application": "COF",
    },
    "COFEOI": {
        "fund_id": COF_EOI_FUND_ID,
        "round_id": COF_EOI_ROUND_ID,
        "type_of_application": "COF-EOI",
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

fund_round_mapping_config_with_round_id = {
    v["round_id"]: {"fund_id": v["fund_id"], "type_of_application": v["type_of_application"]}
    for k, v in fund_round_mapping_config.items()
}
