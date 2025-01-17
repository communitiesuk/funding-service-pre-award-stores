# ruff: noqa: E501

scored_criteria = [
    {
        "id": "about-your-organisation",
        "name": "About your organisation",
        "weighting": 0.5,
        "sub_criteria": [
            {
                "id": "organisation-information-hsra-rp",
                "name": "Organisation information",
                "themes": [
                    {
                        "id": "who-is-your-section-151-officer?",
                        "name": "Who is your section 151 officer?",
                        "answers": [
                            {
                                "field_id": "okHmBB",
                                "form_name": "organisation-information-hsra-rp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Full name",
                            },
                            {
                                "field_id": "bQOXTi",
                                "form_name": "organisation-information-hsra-rp",
                                "field_type": "emailAddressField",
                                "presentation_type": "text",
                                "question": "Email address",
                            },
                            {
                                "field_id": "phaosT",
                                "form_name": "organisation-information-hsra-rp",
                                "field_type": "telephoneNumberField",
                                "presentation_type": "text",
                                "question": "Telephone number",
                            },
                        ],
                    },
                    {
                        "id": "which-local-authority-are-you-applying-from?",
                        "name": "Which local authority are you applying from?",
                        "answers": [
                            {
                                "field_id": "WLddBt",
                                "form_name": "organisation-information-hsra-rp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Which local authority are you applying from?",
                            }
                        ],
                    },
                ],
            },
            {
                "id": "applicant-information-hsra-rp",
                "name": "Applicant information",
                "themes": [
                    {
                        "id": "who-should-we-contact-about-this-application?",
                        "name": "Who should we contact about this application?",
                        "answers": [
                            {
                                "field_id": "OkKkMd",
                                "form_name": "applicant-information-hsra-rp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Full name",
                            },
                            {
                                "field_id": "Lwkcam",
                                "form_name": "applicant-information-hsra-rp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Job title",
                            },
                            {
                                "field_id": "XfiUqN",
                                "form_name": "applicant-information-hsra-rp",
                                "field_type": "emailAddressField",
                                "presentation_type": "text",
                                "question": "Email address",
                            },
                            {
                                "field_id": "DlZjvr",
                                "form_name": "applicant-information-hsra-rp",
                                "field_type": "telephoneNumberField",
                                "presentation_type": "text",
                                "question": "Telephone number",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "about-your-project",
        "name": "About your project",
        "weighting": 0.5,
        "sub_criteria": [
            {
                "id": "vacant-property-details-hsra-rp",
                "name": "Vacant property details",
                "themes": [
                    {
                        "id": "upload-the-initial-notice-you-served-the-landlord",
                        "name": "Upload the initial notice you served the landlord",
                        "answers": [
                            {
                                "field_id": "ndpQJk",
                                "form_name": "vacant-property-details-hsra-rp",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload the initial notice you served the landlord",
                                "path": "upload-the-initial-notice-you-served-the-landlord",
                            }
                        ],
                    },
                    {
                        "id": "what-is-the-total-commercial-floorspace-of-the-property,-in-meters-squared?",
                        "name": "What is the total commercial floorspace of the property, in meters squared?",
                        "answers": [
                            {
                                "field_id": "rFpLZQ",
                                "form_name": "vacant-property-details-hsra-rp",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "What is the total commercial floorspace of the property, in meters squared?",
                            }
                        ],
                    },
                    {
                        "id": "what-is-the-vacant-property's-address?",
                        "name": "What is the vacant property's address?",
                        "answers": [
                            {
                                "field_id": "dwLpZU",
                                "form_name": "vacant-property-details-hsra-rp",
                                "field_type": "ukAddressField",
                                "presentation_type": "text",
                                "question": "What is the vacant property's address?",
                            }
                        ],
                    },
                ],
            },
            {
                "id": "designated-area-details-hsra-rp",
                "name": "Designated area details",
                "themes": [
                    {
                        "id": "share-the-link-with-details-of-the-designated-area",
                        "name": "Share the link with details of the designated area",
                        "answers": [
                            {
                                "field_id": "TzGISC",
                                "form_name": "designated-area-details-hsra-rp",
                                "field_type": "websiteField",
                                "presentation_type": "text",
                                "question": "Share the link with details of the designated area.",
                            }
                        ],
                    },
                    {
                        "id": "which-designated-high-street-or-town-centre-is-the-vacant-property-in?",
                        "name": "Which designated high street or town centre is the vacant property in?",
                        "answers": [
                            {
                                "field_id": "frDgtU",
                                "form_name": "designated-area-details-hsra-rp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Which designated high street or town centre is the vacant property in?",
                            }
                        ],
                    },
                ],
            },
            {
                "id": "milestones-hsra-rp",
                "name": "Milestones",
                "themes": [
                    {
                        "id": "when-do-you-expect-the-auction-to-take-place?",
                        "name": "When do you expect the auction to take place?",
                        "answers": [
                            {
                                "field_id": "kkBYPW",
                                "form_name": "milestones-hsra-rp",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "When do you expect the auction to take place?",
                            }
                        ],
                    },
                    {
                        "id": "when-do-you-expect-the-tenant-to-move-in?",
                        "name": "When do you expect the tenant to move in?",
                        "answers": [
                            {
                                "field_id": "HeqfVH",
                                "form_name": "milestones-hsra-rp",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "When do you expect the tenant to move in?",
                            }
                        ],
                    },
                    {
                        "id": "when-do-you-expect-to-finish-the-refurbishment-works?",
                        "name": "When do you expect to finish the refurbishment works?",
                        "answers": [
                            {
                                "field_id": "gLzqSP",
                                "form_name": "milestones-hsra-rp",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "When do you expect to finish the refurbishment works?",
                            }
                        ],
                    },
                    {
                        "id": "when-do-you-expect-to-submit-your-claim?",
                        "name": "When do you expect to submit your claim?",
                        "answers": [
                            {
                                "field_id": "pTZLiJ",
                                "form_name": "milestones-hsra-rp",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "When do you expect to submit your claim?",
                            }
                        ],
                    },
                    {
                        "id": "when-do-you-expect-the-tenant-to-sign--the-tenancy-agreement?",
                        "name": "When do you expect the tenant to sign  the tenancy agreement?",
                        "answers": [
                            {
                                "field_id": "ihfalZ",
                                "form_name": "milestones-hsra-rp",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "When do you expect the tenant to sign  the tenancy agreement?",
                            }
                        ],
                    },
                ],
            },
            {
                "id": "project-costs-hsra-rp",
                "name": "Project costs",
                "themes": [
                    {
                        "id": "upload-the-independent-survey-of-works",
                        "name": "Upload the independent survey of works",
                        "answers": [
                            {
                                "field_id": "zORoJy",
                                "form_name": "project-costs-hsra-rp",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload the quote for the vacancy register",
                                "path": "upload-the-independent-survey-of-works",
                            }
                        ],
                    },
                    {
                        "id": "how-much-funding-are-you-applying-for?-",
                        "name": "How much funding are you applying for? ",
                        "answers": [
                            {
                                "field_id": "uJIluf",
                                "form_name": "project-costs-hsra-rp",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "How much funding are you applying for? ",
                            }
                        ],
                    },
                    {
                        "id": "why-are-your-costs-higher-than-the-guided-price?",
                        "name": "Why are your costs higher than the guided price?",
                        "answers": [
                            {
                                "field_id": "LFwJND",
                                "form_name": "project-costs-hsra-rp",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Why are your costs higher than the guided price?",
                            }
                        ],
                    },
                    {
                        "id": "upload-quotes-for-refurbishment",
                        "name": "Upload quotes for refurbishment",
                        "answers": [
                            {
                                "field_id": "xPzwQq",
                                "form_name": "project-costs-hsra-rp",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload quotes for refurbishment",
                                "path": "upload-quotes-for-refurbishment",
                            }
                        ],
                    },
                ],
            },
        ],
    },
]
