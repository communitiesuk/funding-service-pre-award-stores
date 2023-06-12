# flake8: noqa
from string import Template

application_store_json_template = Template(
    """
    {
    "account_id": "cbf981cf-5238-4d3e-84e9-b9c183789a91",
    "date_submitted": "2022-10-27T08:32:13.383999",
    "forms": [
        {
            "name": "feasibility",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Tell us about the feasibility studies you have carried out for your project",
                            "key": "ieRCkI",
                            "title": "Tell us about the feasibility studies you have carried out for your project",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "aAeszH",
                            "title": "Do you need to do any further feasibility work?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "risk",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "sample1.doc",
                            "key": "ozgwXq",
                            "title": "Risks to your project (document upload)",
                            "type": "file"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "community-use",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": [
                                "support-local-community"
                            ],
                            "key": "CDwTrG",
                            "title": "What policy aims will your project deliver against?",
                            "type": "list"
                        },
                        {
                            "answer": "Test",
                            "key": "kxgWTy",
                            "title": "Who in the community uses the asset, or has used it in the past, and who benefits from it?",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "GNhrIs",
                            "title": "Tell us how losing the asset would affect, or has already affected, people in the community",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "qsZLjZ",
                            "title": "Why will the asset be lost without community intervention?",
                            "type": "text"
                        }
                    ],
                    "question": "Strategic case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "environmental-sustainability",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "CvVZJv",
                            "title": "Tell us how you have considered the environmental sustainability of your project",
                            "type": "text"
                        }
                    ],
                    "question": "Strategic case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "local-support",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "KqoaJL",
                            "title": "Are you confident there is local support for your project?",
                            "type": "list"
                        }
                    ],
                    "question": "Strategic case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "project-qualification",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "HvxXPI",
                            "title": "Does your project meet the definition of a subsidy?",
                            "type": "list"
                        }
                    ],
                    "question": "Subsidy control and state aid",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "skills-and-resources",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "CBIWnt",
                            "title": "Do you have experience of managing a community asset?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "vKnMPG",
                            "title": "Do you have any plans to recruit people to help you manage the asset?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "upload-business-plan",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "sample1.doc",
                            "key": "rFXeZo",
                            "title": "Upload business plan",
                            "type": "file"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "project-information",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "gScdbf",
                            "title": "Have you been given funding through the Community Ownership Fund before?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "$project_name",
                            "key": "KAgrBz",
                            "title": "Project name",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "wudRxx",
                            "title": "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "TlGjXb",
                            "title": "Explain why the asset is at risk of being lost to the community, or why it has already been lost",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "GCjCse",
                            "title": "Give a brief summary of your project, including what you hope to achieve",
                            "type": "text"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Test Address, null, Test Town Or City, null, $location_postcode",
                            "key": "yEmHpp",
                            "title": "Address of the community asset",
                            "type": "text"
                        },
                        {
                            "answer": "Constituency",
                            "key": "iTeLGU",
                            "title": "In which constituency is your asset?",
                            "type": "text"
                        },
                        {
                            "answer": "Local Council",
                            "key": "MGRlEi",
                            "title": "In which local council area is your asset?",
                            "type": "text"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "organisation-information",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "ANON-###-###-###",
                            "key": "WWWWxy",
                            "title": "Your unique tracker number",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "YdtlQZ",
                            "title": "Organisation name",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "iBCGxY",
                            "title": "Does your organisation use any other names?",
                            "type": "list"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "emVGxS",
                            "title": "What is your organisation's main purpose?",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "btTtIb",
                            "title": "Tell us about your organisation's main activities",
                            "type": "text"
                        },
                        {
                            "answer": null,
                            "key": "SkocDi",
                            "title": "Tell us about your organisation's main activities - Activity 2 ",
                            "type": "text"
                        },
                        {
                            "answer": null,
                            "key": "CNeeiC",
                            "title": "Tell us about your organisation's main activities - Activity 3 ",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "BBlCko",
                            "title": "Have you delivered projects like this before?",
                            "type": "list"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "CIO",
                            "key": "lajFtB",
                            "title": "Type of organisation",
                            "type": "list"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "aHIGbK",
                            "title": "Charity number ",
                            "type": "text"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "DwfHtk",
                            "title": "Is your organisation a trading subsidiary of a parent company?",
                            "type": "list"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Test Address, null, Test Town Or City, null, $location_postcode",
                            "key": "ZQolYb",
                            "title": "Organisation address",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "zsoLdf",
                            "title": "Is your correspondence address different to the organisation address?",
                            "type": "list"
                        },
                        {
                            "answer": "https://twitter.com/luhc",
                            "key": "FhbaEy",
                            "title": "Website and social media ",
                            "type": "text"
                        },
                        {
                            "answer": null,
                            "key": "FcdKlB",
                            "title": "Website and social media - Link or username 2",
                            "type": "text"
                        },
                        {
                            "answer": null,
                            "key": "BzxgDA",
                            "title": "Website and social media - Link or username 3",
                            "type": "text"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "hnLurH",
                            "title": "Is your application a joint bid in partnership with other organisations?",
                            "type": "list"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "applicant-information",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test Name",
                            "key": "ZBjDTn",
                            "title": "Name of lead contact",
                            "type": "text"
                        },
                        {
                            "answer": "testemailfundingservice@testemailfundingservice.com",
                            "key": "LZBrEj",
                            "title": "Lead contact email address",
                            "type": "text"
                        },
                        {
                            "answer": "0000000000",
                            "key": "lRfhGB",
                            "title": "Lead contact telephone number",
                            "type": "text"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "asset-information",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "$asset_type",
                            "key": "yaQoxU",
                            "title": "Asset type",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "buy-the-asset",
                            "key": "VWkLlk",
                            "title": "What do you intend to do with the asset?",
                            "type": "list"
                        },
                        {
                            "answer": false,
                            "key": "IRfSZp",
                            "title": "Do you know who currently owns your asset?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Current Owner",
                            "key": "FtDJfK",
                            "title": "Describe the current ownership status",
                            "type": "text"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "gkulUE",
                            "title": "Have you already completed the purchase or lease?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "nvMmGE",
                            "title": "Describe the expected sale process, or the proposed terms of your lease if you are renting the asset",
                            "type": "text"
                        },
                        {
                            "answer": "2022-12-01",
                            "key": "ghzLRv",
                            "title": "Expected date of sale or lease",
                            "type": "date"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "Wyesgy",
                            "title": "Is your asset currently publicly owned?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "hvzzWB",
                            "title": "Is this a registered Asset of Community Value (ACV)?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "VwxiGn",
                            "title": "Is the asset listed for disposal, or part of a Community Asset Transfer?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project ",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": [
                                "for-sale-or-listed-for-disposal"
                            ],
                            "key": "UDTxqC",
                            "title": "Why is the asset at risk of closure?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "community-engagement",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Tell us how you have engaged with the community about your intention to take ownership of the asset",
                            "key": "HJBgvw",
                            "title": "Tell us how you have engaged with the community about your intention to take ownership of the asset, and explain how this has shaped your project plans",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "JCACTy",
                            "title": "Have you done any fundraising in the community?",
                            "type": "list"
                        }
                    ],
                    "question": "Strategic case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Tell us how your project supports any wider local plans",
                            "key": "NZKHOp",
                            "title": "Tell us how your project supports any wider local plans",
                            "type": "text"
                        }
                    ],
                    "question": "Strategic case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "funding-required",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "2300",
                            "key": "JzWvhj",
                            "title": "Capital funding",
                            "type": "text"
                        },
                        {
                            "answer": "2300",
                            "key": "jLIgoi",
                            "title": "Revenue funding (optional)",
                            "type": "text"
                        }
                    ],
                    "question": "Management case ",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": [
                                "Capital Funding : £2300"
                            ],
                            "key": "MultiInputField",
                            "title": "Capital costs",
                            "type": "text"
                        }
                    ],
                    "question": "Management case ",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "NWTKzQ",
                            "title": "Are you applying for revenue funding from the Community Ownership Fund? (optional)",
                            "type": "list"
                        }
                    ],
                    "question": "Management case ",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "DIZZOC",
                            "title": "Have you secured any match funding yet?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "RvbwSX",
                            "title": "Do you have any match funding identified but not yet secured?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "2300",
                            "key": "fnIdkJ",
                            "title": "Asset value",
                            "type": "text"
                        }
                    ],
                    "question": "Management case ",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "community-benefits",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": [
                                "community-pride"
                            ],
                            "key": "QjJtbs",
                            "title": "What community benefits do you expect to deliver with this project? ",
                            "type": "list"
                        },
                        {
                            "answer": "Test",
                            "key": "gDTsgG",
                            "title": "Tell us about these benefits in detail, and explain how you'll measure the benefits it'll bring for the community",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "kYjJFy",
                            "title": "Explain how you plan to sustain, and potentially expand, these benefits over time",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "UbjYqE",
                            "title": "Tell us how you'll make sure the whole community benefits from the asset",
                            "type": "text"
                        }
                    ],
                    "question": "Potential to deliver community benefits",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "inclusiveness-and-integration",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "SrtVAs",
                            "title": "Describe the planned activities or services that will take place at the asset",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "YbfbSC",
                            "title": "Describe anything that might prevent people from using the asset or participating in its running",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "KuhSWw",
                            "title": "Tell us how you'll make your project accessible and inclusive to everyone in the community",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "bkJsiO",
                            "title": "Describe how the project will bring people together from all over the community",
                            "type": "text"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "project-costs",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "WDDkVB",
                            "title": "Summarise your cash flow for the running of the asset",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "oaIntA",
                            "title": "If successful, will you use your funding in the next 12 months?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": [
                                "Income Test : £2300"
                            ],
                            "key": "MultiInputField",
                            "title": "Sources of income",
                            "type": "text"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": [
                                "Running Cost Test : £2300"
                            ],
                            "key": "MultiInputField-2",
                            "title": "Running costs",
                            "type": "text"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "community-representation",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "JnvsPq",
                            "title": "List the members of your board",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "yMCivI",
                            "title": "Tell us about your governance and membership structures",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "NUZOvS",
                            "title": "Explain how you'll consider the views of the community in the running of the asset",
                            "type": "text"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "value-to-the-community",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "oOPUXI",
                            "title": "Tell us about your local community as a whole",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "NKOmNL",
                            "title": "Describe any specific challenges your community faces, and how the asset will address these",
                            "type": "text"
                        }
                    ],
                    "question": "Added value to the community",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "declarations",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": true,
                            "key": "LlvhYl",
                            "title": "Confirm you have considered subsidy control and state aid implications for your project, and the information you have given us is correct",
                            "type": "list"
                        },
                        {
                            "answer": false,
                            "key": "wJrJWY",
                            "title": "Confirm you have considered people with protected characteristics throughout the planning of your project",
                            "type": "list"
                        },
                        {
                            "answer": true,
                            "key": "COiwQr",
                            "title": "Confirm you have considered sustainability and the environment throughout the planning of your project, including compliance with the government's Net Zero ambitions",
                            "type": "list"
                        },
                        {
                            "answer": false,
                            "key": "bRPzWU",
                            "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
                            "type": "list"
                        }
                    ],
                    "question": "Declarations",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        }
    ],
    "fund_id": "$fund_id",
    "id": "$app_id" ,
    "last_edited": "2022-10-27T08:32:11.843201",
    "project_name": "$project_name" ,
    "reference": "$short_ref" ,
    "round_id": "$round_id",
    "round_name": "Round 2 Window 2",
    "started_at": "2022-10-27T08:28:55.699864",
    "status": "SUBMITTED",
    "location_json_blob": {
        "error": $location_error,
        "county": "$location_county",
        "region": "$location_region",
        "country": "$location_country",
        "postcode": "$location_postcode",
        "constituency": "$location_constituency"
    }

}
"""
)

cofr3w1_application_store_json_template = Template(
    """
    {
    "id": "$app_id",
    "status": "SUBMITTED",
    "fund_id": "$fund_id",
    "language": "en",
    "round_id": "$round_id",
    "reference": "$short_ref",
    "account_id": "53433826-95b3-42b1-b56f-aee3405a1b9f",
    "round_name": "Round 3 Window 1",
    "started_at": "2023-06-05T10:52:24.629455",
    "last_edited": "2023-06-06T13:38:48.747499",
    "project_name": "$project_name",
    "date_submitted": "2023-06-06T13:38:51.467199",
    "forms": [
        {
            "name": "declarations-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "vSQKwD",
                            "type": "list",
                            "title": "Confirm you have considered subsidy control and state aid implications for your project, and the information you have given us is correct",
                            "answer": true
                        },
                        {
                            "key": "CQoLFp",
                            "type": "list",
                            "title": "Confirm you have considered people with protected characteristics throughout the planning of your project",
                            "answer": true
                        },
                        {
                            "key": "jdPkiX",
                            "type": "list",
                            "title": "Confirm you have considered sustainability and the environment throughout the planning of your project, including compliance with the government's Net Zero ambitions",
                            "answer": true
                        },
                        {
                            "key": "qWuSCy",
                            "type": "list",
                            "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
                            "answer": true
                        },
                        {
                            "key": "tjZlml",
                            "type": "list",
                            "title": "Confirm that the information you've provided in this application is accurate to the best of your knowledge on the date of submission",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "LkvizC",
                    "question": "Agree to the final confirmations"
                }
            ]
        },
        {
            "name": "funding-required-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "ABROnB",
                            "type": "text",
                            "title": "Capital funding",
                            "answer": "2300"
                        },
                        {
                            "key": "cLDRvN",
                            "type": "text",
                            "title": "Revenue funding (optional)",
                            "answer": "2300"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bgUGuD",
                    "question": "Total funding request from the Community Ownership Fund"
                },
                {
                    "fields": [
                        {
                            "key": "qQLyXL",
                            "type": "multiInput",
                            "title": "Capital costs",
                            "answer": [
                                {
                                    "GLQlOh": "Capital Funding",
                                    "JtwkMy": 2300
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bgUGuD",
                    "question": "Capital costs for your project"
                },
                {
                    "fields": [
                        {
                            "key": "DOvZvB",
                            "type": "list",
                            "title": "Have you secured any match funding yet?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bgUGuD",
                    "question": "If you've secured match funding"
                },
                {
                    "fields": [
                        {
                            "key": "DmgsiG",
                            "type": "list",
                            "title": "Do you have any match funding identified but not yet secured?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bgUGuD",
                    "question": "If you’ve identified further match funding"
                },
                {
                    "fields": [
                        {
                            "key": "matkNH",
                            "type": "list",
                            "title": "Are you applying for revenue funding from the Community Ownership Fund? (optional)",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bgUGuD",
                    "question": "Revenue funding"
                }
            ]
        },
        {
            "name": "community-representation-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "ReomFo",
                            "type": "freeText",
                            "title": "List the members of your board",
                            "answer": "<p>Test Community Representation Form</p>"
                        },
                        {
                            "key": "fjVmOt",
                            "type": "freeText",
                            "title": "Tell us about your governance and membership structures",
                            "answer": "<p>Test Community Representation Form</p>"
                        },
                        {
                            "key": "GETNxN",
                            "type": "freeText",
                            "title": "Explain how you'll consider the views of the community in the running of the asset",
                            "answer": "<p>Test Community Representation Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "KbnmOO",
                    "question": "How you’ll run the asset"
                }
            ]
        },
        {
            "name": "operational-costs-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "qXNkfr",
                            "type": "freeText",
                            "title": "Describe your cash flow for the running of the asset",
                            "answer": "<p>Summarise your cash flow for the running of the asset</p>"
                        },
                        {
                            "key": "qQSVEn",
                            "type": "list",
                            "title": "If successful, will you use your funding in the next 12 months?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "oSfXFZ",
                    "question": "Cashflow to run the asset"
                },
                {
                    "fields": [
                        {
                            "key": "MSNJQD",
                            "type": "multiInput",
                            "title": "Sources of income",
                            "answer": [
                                {
                                    "AJEWXD": "Income Test 2",
                                    "cHFrIp": 2300
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "oSfXFZ",
                    "question": "Income to run the asset"
                },
                {
                    "fields": [
                        {
                            "key": "NPgwcH",
                            "type": "multiInput",
                            "title": "Running costs",
                            "answer": [
                                {
                                    "IIdfRj": "Running Cost Test",
                                    "wlGQua": 2300
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "oSfXFZ",
                    "question": "Running costs of the asset"
                }
            ]
        },
        {
            "name": "skills-and-resources-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "XXGyzn",
                            "type": "freeText",
                            "title": "Describe any relevant experience you have delivering similar projects or running an asset",
                            "answer": "<p>Describe any relevant experience you have delivering similar projects or running an asset</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "eLpYFr",
                    "question": "Your experience running similar assets"
                },
                {
                    "fields": [
                        {
                            "key": "Uaeyae",
                            "type": "list",
                            "title": "Do you have plans to recruit people to help you run the asset?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "eLpYFr",
                    "question": "Recruitment plans"
                }
            ]
        },
        {
            "name": "inclusiveness-and-integration-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "mgIesb",
                            "type": "freeText",
                            "title": "Tell us how the asset will be accountable to local people, and involve them in its running",
                            "answer": "<p>Test Inclusiveness and Integration Form</p>"
                        },
                        {
                            "key": "lQEkep",
                            "type": "freeText",
                            "title": "Describe anything that might prevent people from using the asset or participating in its running",
                            "answer": "<p>Test Inclusiveness and Integration Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "eCZBSV",
                    "question": "How you’ll make the asset inclusive"
                }
            ]
        },
        {
            "name": "applicant-information-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "SnLGJE",
                            "type": "text",
                            "title": "Name of lead contact",
                            "answer": "Joe Bloggs"
                        },
                        {
                            "key": "qRDTUc",
                            "type": "text",
                            "title": "Lead contact job title",
                            "answer": "Mr"
                        },
                        {
                            "key": "NlHSBg",
                            "type": "text",
                            "title": "Lead contact email address",
                            "answer": "testemailfundingservice@testemailfundingservice.com"
                        },
                        {
                            "key": "FhBkJQ",
                            "type": "text",
                            "title": "Lead contact telephone number",
                            "answer": "0000000000"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "ZuHuGk",
                    "question": "Lead contact details"
                }
            ]
        },
        {
            "name": "environmental-sustainability-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "dypuJs",
                            "type": "freeText",
                            "title": "Tell us how you have considered the environmental sustainability of your project",
                            "answer": "<p>Test Environmental Sustainability Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "ljcxPd",
                    "question": "How you've considered the environment"
                }
            ]
        },
        {
            "name": "feasibility-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "iSbwDM",
                            "type": "freeText",
                            "title": "Tell us about the feasibility studies you have carried out for your project",
                            "answer": "<p>Tell us about the feasibility studies you have carried out for your project</p>"
                        },
                        {
                            "key": "jFPlEJ",
                            "type": "list",
                            "title": "Do you need to do any further feasibility work?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bBGnkL",
                    "question": "Feasiblity studies you've carried out"
                }
            ]
        },
        {
            "name": "local-support-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "tDVPnl",
                            "type": "freeText",
                            "title": "Tell us about the local support for your project",
                            "answer": "<p>Tell us about the local support for your project</p>"
                        },
                        {
                            "key": "bDWjTN",
                            "type": "text",
                            "title": "Upload supporting evidence",
                            "answer": null
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "apkBSm",
                    "question": "Your support for the project"
                }
            ]
        },
        {
            "name": "project-qualifications-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "ZEKMQd",
                            "type": "list",
                            "title": "Does your project meet the definition of a subsidy?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "WsFJts",
                    "question": "If your project meets the definition"
                }
            ]
        },
        {
            "name": "risk-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "EODncR",
                            "type": "text",
                            "title": "Risks to your project (document upload)",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "HKdODf",
                    "question": "Your project risk register"
                }
            ]
        },
        {
            "name": "upload-business-plan-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "ndpQJk",
                            "type": "text",
                            "title": "Upload business plan",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xtwqlH",
                    "question": "Your business plan"
                }
            ]
        },
        {
            "name": "project-information-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "pWwCRM",
                            "type": "list",
                            "title": "Have you applied to the Community Ownership Fund before?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qsnIGd",
                    "question": "Previous Community Ownership Fund applications"
                },
                {
                    "fields": [
                        {
                            "key": "apGjFS",
                            "type": "text",
                            "title": "Project name",
                            "answer": "$project_name"
                        },
                        {
                            "key": "bEWpAj",
                            "type": "freeText",
                            "title": "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community",
                            "answer": "<p>Test Project Information Form</p>"
                        },
                        {
                            "key": "uypCNM",
                            "type": "freeText",
                            "title": "Give a brief summary of your project, including what you hope to achieve",
                            "answer": "<p>Test Project Information Form</p>"
                        },
                        {
                            "key": "AgeRbd",
                            "type": "freeText",
                            "title": "Tell us about the planned activities and/or services that will take place in the asset",
                            "answer": "<p>Test Project Information Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qsnIGd",
                    "question": "Project name and summary"
                },
                {
                    "fields": [
                        {
                            "key": "EfdliG",
                            "type": "text",
                            "title": "Address of the community asset",
                            "answer": "Test Address, null, Test Town Or City, null, $location_postcode"
                        },
                        {
                            "key": "fIEUcb",
                            "type": "text",
                            "title": " In which constituency is your asset?",
                            "answer": "Constituency"
                        },
                        {
                            "key": "SWfcTo",
                            "type": "text",
                            "title": "In which local council area is your asset?",
                            "answer": "Local Council"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qsnIGd",
                    "question": "Address of the asset"
                }
            ]
        },
        {
            "name": "community-benefits-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "pqYxJO",
                            "type": "list",
                            "title": "What community benefits do you expect to deliver with this project?",
                            "answer": [
                                "community-pride"
                            ]
                        },
                        {
                            "key": "lgfiGB",
                            "type": "freeText",
                            "title": "Tell us about these benefits in detail, and how the asset's activities will help deliver them",
                            "answer": "<p>Test Community Benefits Form</p>"
                        },
                        {
                            "key": "zKKouR",
                            "type": "freeText",
                            "title": "Explain how you plan to deliver and sustain these benefits over time",
                            "answer": "<p>Test Community Benefits Form</p>"
                        },
                        {
                            "key": "ZyIQGI",
                            "type": "freeText",
                            "title": "Tell us how you'll make sure the whole community benefits from the asset",
                            "answer": "<p>Test Community Benefits Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "PTOBPV",
                    "question": "Benefits you'll deliver"
                }
            ]
        },
        {
            "name": "organisation-information-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "WWWWxy",
                            "type": "text",
                            "title": "Your unique tracker number",
                            "answer": "ANON-###-###-###"
                        },
                        {
                            "key": "YdtlQZ",
                            "type": "text",
                            "title": "Organisation name",
                            "answer": "Test Change Answers"
                        },
                        {
                            "key": "iBCGxY",
                            "type": "list",
                            "title": "Does your organisation use any other names?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Organisation names"
                },
                {
                    "fields": [
                        {
                            "key": "emVGxS",
                            "type": "freeText",
                            "title": "What is your organisation's main purpose?",
                            "answer": "<p>Test Org Form</p>"
                        },
                        {
                            "key": "btTtIb",
                            "type": "freeText",
                            "title": "Tell us about your organisation's main activities",
                            "answer": "<p>Test Org Form</p>"
                        },
                        {
                            "key": "SkocDi",
                            "type": "freeText",
                            "title": "Tell us about your organisation's main activities - Activity 2 ",
                            "answer": null
                        },
                        {
                            "key": "CNeeiC",
                            "type": "freeText",
                            "title": "Tell us about your organisation's main activities - Activity 3 ",
                            "answer": null
                        },
                        {
                            "key": "BBlCko",
                            "type": "list",
                            "title": "Have you delivered projects like this before?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Purpose and activities"
                },
                {
                    "fields": [
                        {
                            "key": "lajFtB",
                            "type": "list",
                            "title": "Type of organisation",
                            "answer": "CIO"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "How your organisation is classified"
                },
                {
                    "fields": [
                        {
                            "key": "aHIGbK",
                            "type": "text",
                            "title": "Charity number ",
                            "answer": "234388322"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Charity registration details"
                },
                {
                    "fields": [
                        {
                            "key": "DwfHtk",
                            "type": "list",
                            "title": "Is your organisation a trading subsidiary of a parent company?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Trading subsidiaries"
                },
                {
                    "fields": [
                        {
                            "key": "ZQolYb",
                            "type": "text",
                            "title": "Organisation address",
                            "answer": "Test Address, null, Test Town Or City, null, $location_postcode"
                        },
                        {
                            "key": "zsoLdf",
                            "type": "list",
                            "title": "Is your correspondence address different to the organisation address?",
                            "answer": false
                        },
                        {
                            "key": "FhbaEy",
                            "type": "text",
                            "title": "Website and social media",
                            "answer": "https://twitter.com/luhc"
                        },
                        {
                            "key": "FcdKlB",
                            "type": "text",
                            "title": "Website and social media - Link or username 2",
                            "answer": null
                        },
                        {
                            "key": "BzxgDA",
                            "type": "text",
                            "title": "Website and social media - Link or username 3",
                            "answer": null
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Organisation address"
                },
                {
                    "fields": [
                        {
                            "key": "hnLurH",
                            "type": "list",
                            "title": "Is your application a joint bid in partnership with other organisations?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Joint applications"
                }
            ]
        },
        {
            "name": "community-engagement-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "azCutK",
                            "type": "freeText",
                            "title": "Tell us how you have engaged with the community about your intention to take ownership of the asset",
                            "answer": "<p>Test Community Engagement Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "lmdhVN",
                    "question": "How you've engaged with the community"
                },
                {
                    "fields": [
                        {
                            "key": "jAhuWN",
                            "type": "freeText",
                            "title": "Describe your fundraising activities",
                            "answer": "<p>Test Community Engagement Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "lmdhVN",
                    "question": "Your fundraising activities"
                },
                {
                    "fields": [
                        {
                            "key": "HYsezC",
                            "type": "freeText",
                            "title": "Tell us about any partnerships you've formed, and how they'll help the project be successful",
                            "answer": "<p>Test Community Engagement Form</p>"
                        },
                        {
                            "key": "GGBgBY",
                            "type": "freeText",
                            "title": "Tell us how your project supports any wider local plans",
                            "answer": "<p>Test Community Engagement Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "lmdhVN",
                    "question": "Partnerships and local plans"
                }
            ]
        },
        {
            "name": "community-use-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "zTcrYo",
                            "type": "freeText",
                            "title": "Who in the community currently uses the asset, or has used it in the past?",
                            "answer": "<p>Test Community Use Form</p>"
                        },
                        {
                            "key": "whlRYS",
                            "type": "freeText",
                            "title": "Tell us how losing the asset would affect, or has already affected, people in the community",
                            "answer": "<p>Test Community Use Form</p>"
                        },
                        {
                            "key": "NGSXHE",
                            "type": "freeText",
                            "title": "Why will the asset be lost without community intervention?",
                            "answer": "<p>Test Community Use Form</p>"
                        },
                        {
                            "key": "Ieudgn",
                            "type": "freeText",
                            "title": "Explain how the community will be better served with the asset under community ownership",
                            "answer": "<p>Test Community Use Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "GMkooI",
                    "question": "Who uses the asset"
                }
            ]
        },
        {
            "name": "asset-information-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "oXGwlA",
                            "type": "list",
                            "title": "$asset_type",
                            "answer": "cinema"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "How the asset is used in the community"
                },
                {
                    "fields": [
                        {
                            "key": "LaxeJN",
                            "type": "list",
                            "title": "How do you intend to take community ownership of the asset?",
                            "answer": "buy-the-asset"
                        },
                        {
                            "key": "tTOrEp",
                            "type": "text",
                            "title": "Upload asset valuation or lease agreement",
                            "answer": "sample.txt"
                        },
                        {
                            "key": "hdmYjg",
                            "type": "list",
                            "title": "Do you know who currently owns your asset?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "The asset in community ownership"
                },
                {
                    "fields": [
                        {
                            "key": "CSsbsG",
                            "type": "text",
                            "title": "Describe the current ownership status",
                            "answer": "Current Owner"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Current ownership status"
                },
                {
                    "fields": [
                        {
                            "key": "uPvsqM",
                            "type": "list",
                            "title": "Have you already completed the purchase or lease?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "If you've already taken ownership"
                },
                {
                    "fields": [
                        {
                            "key": "XPcbJx",
                            "type": "freeText",
                            "title": "Describe the expected sale process, or the proposed terms of your lease if you are renting the asset",
                            "answer": "<p>Test Asset Information Form</p>"
                        },
                        {
                            "key": "jGjScT",
                            "type": "date",
                            "title": "Expected date of sale or lease",
                            "answer": "2022-12-01"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Expected terms of your ownership or lease"
                },
                {
                    "fields": [
                        {
                            "key": "VGXXyq",
                            "type": "list",
                            "title": "Is your asset currently publicly owned?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Public ownership"
                },
                {
                    "fields": [
                        {
                            "key": "wjBFTf",
                            "type": "list",
                            "title": "Is this a registered Asset of Community Value (ACV)?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Assets of community value"
                },
                {
                    "fields": [
                        {
                            "key": "HyWPwE",
                            "type": "list",
                            "title": "Is the asset listed for disposal, or part of a Community Asset Transfer?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Assets listed for disposal"
                },
                {
                    "fields": [
                        {
                            "key": "KQlOaJ",
                            "type": "list",
                            "title": "Why is the asset at risk of closure?",
                            "answer": [
                                "for-sale-or-listed-for-disposal"
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Risk of closure"
                }
            ]
        }
    ]
}
"""
)
