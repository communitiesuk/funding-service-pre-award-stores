from fsd_utils import CommonConfig

from api.routes._helpers import transform_to_assessor_task_list_metadata


def test_transform_to_assessor_task_list_metadata():
    sections, critera = transform_to_assessor_task_list_metadata(
        CommonConfig.COF_FUND_ID, CommonConfig.COF_ROUND_2_ID
    )

    assert sections == [
        {
            "name": "Organisation information",
            "sub_criterias": [
                {
                    "name": "Organisation information",
                    "id": "org_info",
                    "first_theme_id": "general_info"
                },
                {
                    "name": "Applicant information",
                    "id": "applicant_info",
                    "first_theme_id": "contact_information"
                }
            ]
        },
        {
            "name": "Project information",
            "sub_criterias": [
                {
                    "name": "Project information",
                    "id": "project_info",
                    "first_theme_id": "previous_funding"
                },
                {
                    "name": "Asset information",
                    "id": "asset_info",
                    "first_theme_id": "asset_ownership"
                }
            ]
        },
        {
            "name": "Check declarations",
            "sub_criterias": [
                {
                    "name": "Declarations",
                    "id": "declarations",
                    "first_theme_id": "declarations"
                },
                {
                    "name": "Subsidy control and state aid",
                    "id": "subsidy_control_and_state_aid",
                    "first_theme_id": "asset_ownership"
                }
            ]
        }
    ]

    assert critera == [
        {
            "name": "Strategic case",
            "total_criteria_score": -1,
            "total_criteria_score_possible": -1,
            "weighting": 0.3,
            "sub_criterias": [
                {
                    "name": "Benefits",
                    "id": "benefits",
                    "score": -1,
                    "theme_count": 2,
                    "status": "Not started",
                    "first_theme_id": "community_use"
                },
                {
                    "name": "Engagement",
                    "id": "engagement",
                    "score": -1,
                    "theme_count": 2,
                    "status": "Not started",
                    "first_theme_id": "engaging-the-community"
                },
                {
                    "name": "Environmental Sustainability",
                    "id": "environmental_sustainability",
                    "score": -1,
                    "theme_count": 1,
                    "status": "Not started",
                    "first_theme_id": "environmental-considerations"
                }
            ]
        },
        {
            "name": "Management case",
            "total_criteria_score": -1,
            "total_criteria_score_possible": -1,
            "weighting": 0.3,
            "sub_criterias": [
                {
                    "name": "Funding breakdown",
                    "id": "funding_breakdown",
                    "score": -1,
                    "theme_count": 1,
                    "status": "Not started",
                    "first_theme_id": "funding_requested"
                },
                {
                    "name": "Financial and risk forecasts",
                    "id": "financial_and_risk_forecasts",
                    "score": -1,
                    "theme_count": 3,
                    "status": "Not started",
                    "first_theme_id": "feasibility"
                },
                {
                    "name": "Skills and resources",
                    "id": "skills_and_resources",
                    "score": -1,
                    "theme_count": 3,
                    "status": "Not started",
                    "first_theme_id": "previous_experience"
                },
                {
                    "name": "Representation, inclusiveness and integration",
                    "id": "representation_inclusiveness_and_integration",
                    "score": -1,
                    "theme_count": 2,
                    "status": "Not started",
                    "first_theme_id": "representing_community_views"
                },
                {
                    "name": "Business plan",
                    "id": "business_plan",
                    "score": -1,
                    "theme_count": 1,
                    "status": "Not started",
                    "first_theme_id": "business_plan"
                }
            ]
        },
        {
            "name": "Potential to deliver community benefit",
            "total_criteria_score": -1,
            "total_criteria_score_possible": -1,
            "weighting": 0.3,
            "sub_criterias": [
                {
                    "name": "How the community benefits\t",
                    "id": "community-benefits",
                    "score": -1,
                    "theme_count": 2,
                    "status": "Not started",
                    "first_theme_id": "delivering_and_sustaining_benefits"
                }
            ]
        },
        {
            "name": "Added value of the community asset",
            "total_criteria_score": -1,
            "total_criteria_score_possible": -1,
            "weighting": 0.1,
            "sub_criterias": [
                {
                    "name": "Value to the community",
                    "id": "value-to-the-community",
                    "score": -1,
                    "theme_count": 1,
                    "status": "Not started",
                    "first_theme_id": "addressing_community_challenges"
                }
            ]
        }
    ]
