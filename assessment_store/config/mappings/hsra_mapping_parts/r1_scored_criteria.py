# flake8: noqa
# Ignore line length

scored_criteria = [
    {
        "id": "project_costs",
        "name": "Project costs",
        "weighting": 0.53,
        "sub_criteria": [
            {
                "id": "total_expected_cost",
                "name": "Total expected cost",
                "themes": [
                    {
                        "id": "total_expected_cost",
                        "name": "Total expected cost",
                        "answers": [
                            {
                                "field_id": "QveKZm",
                                "form_name": "total-expected-cost-hsra",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "How much match funding have you secured, in pounds?",
                            },
                            {
                                "field_id": "KSQYyb",
                                "form_name": "total-expected-cost-hsra",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Have you secured any match funding?",
                            },
                            {
                                "field_id": "lfXuaP",
                                "form_name": "total-expected-cost-hsra",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "What is the total expected cost of delivering the HSRA, in pounds?",
                            },
                            {
                                "field_id": "pyCINJ",
                                "form_name": "total-expected-cost-hsra",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Who is providing this?",
                            },
                            {
                                "field_id": "OBXEXZ",
                                "form_name": "total-expected-cost-hsra",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Why are your costs higher than \u00c2\u00a372,000?",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "refurbishment_costs",
                "name": "Refurbishment costs",
                "themes": [
                    {
                        "id": "refurbishment_costs",
                        "name": "Refurbishment costs",
                        "answers": [
                            {
                                "field_id": "pfEHzn",
                                "form_name": "refurbishment-costs-hsra",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "What is the total expected cost of refurbishment, in pounds?",
                            },
                            {
                                "field_id": "xUgKLI",
                                "form_name": "refurbishment-costs-hsra",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload quotes showing refurbishment costs",
                            },
                            {
                                "field_id": "SMwXcK",
                                "form_name": "refurbishment-costs-hsra",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload the independent survey of works",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "auction_costs",
                "name": "Auction costs",
                "themes": [
                    {
                        "id": "auction_costs",
                        "name": "Auction costs",
                        "answers": [
                            {
                                "field_id": "QXHlgU",
                                "form_name": "auction-costs-hsra",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload quotes showing auction costs",
                            },
                            {
                                "field_id": "kNlEvn",
                                "form_name": "auction-costs-hsra",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "What is the total expected cost of the auction, in pounds?",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "other_costs",
                "name": "Other costs",
                "themes": [
                    {
                        "id": "other_costs",
                        "name": "Other costs",
                        "answers": [
                            {
                                "field_id": "uJIluf",
                                "form_name": "other-costs-hsra",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "What is the total of any other expected costs, in pounds?",
                            },
                            {
                                "field_id": "kRiNuO",
                                "form_name": "other-costs-hsra",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload quotes showing other costs",
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "about_your_project",
        "name": "About your project",
        "weighting": 0.47,
        "sub_criteria": [
            {
                "id": "vacant_property_details",
                "name": "Vacant property details",
                "themes": [
                    {
                        "id": "vacant_property_details",
                        "name": "Vacant property details",
                        "answers": [
                            {
                                "field_id": "qYtKIg",
                                "form_name": "vacant-property-details-hsra",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "How have you verified this?",
                            },
                            {
                                "field_id": "ndpQJk",
                                "form_name": "vacant-property-details-hsra",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload the initial notice you served the landlord",
                            },
                            {
                                "field_id": "NnOqGc",
                                "form_name": "vacant-property-details-hsra",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "How many days has the property been vacant?",
                            },
                            {
                                "field_id": "vAvGTE",
                                "form_name": "vacant-property-details-hsra",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Before you served notice, what contact did you make with the landlord about the property\u00e2\u20ac\u2122s vacant status?",
                            },
                            {
                                "field_id": "rFpLZQ",
                                "form_name": "vacant-property-details-hsra",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "What is the total commercial floorspace of the property, in meters squared?",
                            },
                            {
                                "field_id": "dwLpZU",
                                "form_name": "vacant-property-details-hsra",
                                "field_type": "ukAddressField",
                                "presentation_type": "address",
                                "question": "What is the vacant property's address?",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "designated_area_details",
                "name": "Designated area details",
                "themes": [
                    {
                        "id": "designated_area_details",
                        "name": "Designated area details",
                        "answers": [
                            {
                                "field_id": "frDgtU",
                                "form_name": "designated-area-details-hsra",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Which designated high street or town centre is the vacant property in?",
                            },
                            {
                                "field_id": "boXxzj",
                                "form_name": "designated-area-details-hsra",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "How many commercial properties are in the designated area?",
                            },
                            {
                                "field_id": "eBpXPM",
                                "form_name": "designated-area-details-hsra",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "How many of these are vacant?",
                            },
                            {
                                "field_id": "fmWgiF",
                                "form_name": "designated-area-details-hsra",
                                "field_type": "websiteField",
                                "presentation_type": "text",
                                "question": "Where have you published the designation details?",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "milestones",
                "name": "Project milestones",
                "themes": [
                    {
                        "id": "milestones",
                        "name": "Project milestones",
                        "answers": [
                            {
                                "field_id": "VoAANy",
                                "form_name": "milestones-hsra",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "When do you expect the tenant to move in?",
                            },
                            {
                                "field_id": "KFjxBs",
                                "form_name": "milestones-hsra",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "When do you expect to submit your post-payment verification (PPV)?",
                            },
                            {
                                "field_id": "fIkkRN",
                                "form_name": "milestones-hsra",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "When do you expect to finish the refurbishment works?",
                            },
                            {
                                "field_id": "yvpmIv",
                                "form_name": "milestones-hsra",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "When do you expect the auction to take place?",
                            },
                            {
                                "field_id": "ihfalZ",
                                "form_name": "milestones-hsra",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "When do you expect the tenant to sign  the tenancy agreement?",
                            },
                            {
                                "field_id": "gzJqwe",
                                "form_name": "milestones-hsra",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "When do you expect to submit your claim?",
                            },
                        ],
                    }
                ],
            },
        ],
    },
]
