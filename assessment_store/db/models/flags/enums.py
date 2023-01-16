from enum import Enum


class FlagType(Enum):
    FLAGGED = 0
    STOPPED = 1
    QA_COMPLETED = 2
    RESOLVED = 3
