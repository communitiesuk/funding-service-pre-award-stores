from __future__ import annotations

import inspect
from dataclasses import dataclass


@dataclass
class Round:
    id: str = ""
    assessment_deadline: str = ""
    deadline: str = ""
    fund_id: str = ""
    opens: str = ""
    title: str = ""
    short_name: str = ""
    prospectus: str = ""
    instructions: str = ""
    contact_email: str = ""
    contact_phone: str = ""
    contact_textphone: str = ""
    support_days: str = ""
    support_times: str = ""
    application_guidance: str = ""
    is_expression_of_interest: bool = False
    reference_contact_page_over_email: bool = False
    has_eligibility: bool = False

    @classmethod
    def from_dict(cls, d: dict):
        # Filter unknown fields from JSON dictionary
        return cls(
            **{k: v for k, v in d.items() if k in inspect.signature(cls).parameters},
            has_eligibility=d["eligibility_config"]["has_eligibility"],
        )
