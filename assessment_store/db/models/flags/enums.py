from enum import Enum


class FlagType(Enum):
    FLAGGED = 0
    STOPPED = 1
    QA_COMPLETED = 2


class ResolutionType(Enum):
    QUERY_RESOLVED = 0
    STOP_ASSESSMENT = 1
