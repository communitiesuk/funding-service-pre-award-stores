import inspect
from dataclasses import dataclass
from typing import List, Dict
from api.models.theme import Theme
from stringcase import lowercase
from dataclasses import dataclass
from dataclass_dict_convert import dataclass_dict_convert


@dataclass_dict_convert()
@dataclass()
class SubCriteria:
    id: str
    name: str
    score_submitted: bool
    themes: List[Theme]

    def __post_init__(self):
        self.themes = [
            Theme.from_filtered_dict(theme) for theme in self.themes
        ]

    @classmethod
    def from_filtered_dict(cls, d: dict):
        # Filter unknown fields from JSON dictionary
        return cls(
            **{
                k: v
                for k, v in d.items()
                if k in inspect.signature(cls).parameters
            }
        )
