from dataclasses import dataclass
import inspect
from typing import List, Dict
from stringcase import camelcase
from api.models.answer import Answer
from dataclass_dict_convert import dataclass_dict_convert


@dataclass_dict_convert()
@dataclass()
class Theme:
    id: str
    name: str
    answers: List[Answer]

    def __post_init__(self):
        self.answers = [
            Answer.from_filtered_dict(answer) for answer in self.answers
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
