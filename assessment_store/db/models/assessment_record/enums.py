from enum import Enum


class Status(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    SUBMITTED = 2
    COMPLETED = 3


class Language(Enum):
    en = 0
    cy = 1
