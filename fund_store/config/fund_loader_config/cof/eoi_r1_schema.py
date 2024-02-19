from fsd_utils import Eoi_Decision

COF_SECURE_MATCH_FUNDING_CAVEAT = (
    "Make progress in securing match funding: COF will contribute up to 80% of the"
    " capital costs you require, and you must raise at least 20% from other sources."
    " You do not need to have secured all your match funding by the time you apply, but"
    " we will ask you to set out your total costs, funding already secured, and plans"
    " to raise any additional funding. You must use COF funding within 12 months, so"
    " you must be able to show that you've made good progress to secure the remaining"
    " match funding. This is so that we're confident you can draw down this funding"
    " within this timeframe."
)
COF_PLANNING_PERMISSION_CAVEAT = (
    "Get planning permission, if needed: When you apply, you must be able to show that"
    " you have secured or have made good progress in securing planning permission, if"
    " needed (and building warrants, if required). This is so that we're confident that"
    " COF funding will be used within the 12 month timeframe."
)

COF_R3_EOI_SCHEMA = {
    "uYiLsv": [
        {
            "answerValue": "not-yet-incorporated",
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Incorporate your organisation: You must have incorporated your"
                " organisation by the time you submit a full application. If you remain"
                " unincorporated, your application will be ineligible."
            ),
        },
    ],
    "NcQSbU": [
        {
            "answerValue": True,
            "result": Eoi_Decision.FAIL,
            "caveat": None,
        },
    ],
    "eEaDGz": [
        {
            "answerValue": False,
            "result": Eoi_Decision.FAIL,
            "caveat": None,
        },
    ],
    "zurxox": [
        {
            "answerValue": False,
            "result": Eoi_Decision.FAIL,
            "caveat": None,
        },
    ],
    "lLQmNb": [
        {
            "answerValue": False,
            "result": Eoi_Decision.FAIL,
            "caveat": None,
        },
    ],
    "fBhSNc": [
        {
            "answerValue": False,
            "result": Eoi_Decision.FAIL,
            "caveat": None,
        },
    ],
    "XuAyrs": [
        {
            "answerValue": "Yes, a parish or community council",
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Understand the rules on acquiring assets from town, parish or"
                " community councils: We cannot fund you to acquire a publicly owned"
                " asset if this involves transferring responsibility for delivering"
                " statutory services (services paid for by tax payers) from the public"
                " authority to your organisation. You should only apply to acquire an"
                " asset from a town, parish or community council if you do not plan to"
                " deliver statutory services."
            ),
        },
        {
            "answerValue": "Yes, another type of public authority",
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Understand the rules on acquiring public sector assets: COF funding"
                " can only be used for renovation and refurbishment costs once a"
                " publicly owned asset has been transferred to you. We cannot fund"
                " capital receipts, unless the costs incurred in transferring the asset"
                " to you are nominal (very small and far below the real value).In your"
                " application, you should show that you are not asking COF to fund a"
                " capital receipt to a public authority (for example, by sharing a"
                " letter confirming the authority is willing/has already agreed a"
                " long-term lease and no capital receipt is involved).We also cannot"
                " fund you to acquire a publicly owned asset if this involves"
                " transferring responsibility for delivering statutory services"
                " (services paid for by tax payers) from the public authority to your"
                " organisation"
            ),
        },
    ],
    "foQgiy": [
        {
            "answerValue": False,
            "result": Eoi_Decision.FAIL,
            "caveat": None,
        },
    ],
    "daJkaD": [
        {
            "answerValue": ["Not sure"],
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Make progress in securing match funding: COF will contribute up to 80%"
                " of the capital costs you require, and you must raise at least 20%"
                " from other sources.You do not need to have secured all your match"
                " funding by the time you apply, but we will ask you to set out your"
                " total costs, funding already secured, and plans to raise any"
                " additional funding.You must use COF funding within 12 months, so you"
                " must be able to show that you've made good progress to secure the"
                " remaining match funding. This is so that we're confident you can draw"
                " down this funding within this timeframe."
            ),
        },
    ],
    "eOWKoO": [
        {
            "answerValue": False,
            "result": Eoi_Decision.FAIL,
            "caveat": None,
        },
    ],
    "oblxxv": [
        {
            "answerValue": False,
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Consider requesting revenue funding: We encourage all organisations"
                " to apply for revenue funding to help cover the initial running costs"
                " of your project. When you apply, you'll need to show us how you"
                " plan to use any revenue funding."
                " See [Section 9 of the COF prospectus for more"
                " guidance](https://www.gov.uk/government/publications/community-"
                "ownership-fund-prospectus/community-ownership-fund-prospectus--3#funding-available)."
            ),
        },
    ],
    "kWRuac": [
        {
            "answerValue": "Not yet approached any funders",
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": COF_SECURE_MATCH_FUNDING_CAVEAT,
        },
        {
            "answerValue": "Approached some funders but not yet secured",
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": COF_SECURE_MATCH_FUNDING_CAVEAT,
        },
        {
            "answerValue": "Approached all funders but not yet secured",
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": COF_SECURE_MATCH_FUNDING_CAVEAT,
        },
        {
            "answerValue": "Secured some match funding",
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": COF_SECURE_MATCH_FUNDING_CAVEAT,
        },
    ],
    "yZxdeJ": [
        {
            "answerValue": True,
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": (
                "Understand the rules on housing: We will not provide funding if your"
                " project's main purpose is to purchase or develop housing assets,"
                " including social housing. However, you can include housing elements"
                " in your project where these are only a small part of supporting the"
                " overall financial sustainability of the asset in community ownership."
            ),
        }
    ],
    "UORyaF": [
        {
            "answerValue": "Not sure",
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": COF_PLANNING_PERMISSION_CAVEAT,
        }
    ],
    "jICagT": [
        {
            "answerValue": "Not yet started",
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": COF_PLANNING_PERMISSION_CAVEAT,
        },
        {
            "answerValue": "Early stage",
            "result": Eoi_Decision.PASS_WITH_CAVEATS,
            "caveat": COF_PLANNING_PERMISSION_CAVEAT,
        },
    ],
    "fZAMFv": [
        {
            "operator": ">",
            "compareValue": 2000000,  # 2 million
            "result": Eoi_Decision.FAIL,
            "caveat": None,
        }
    ],
}
