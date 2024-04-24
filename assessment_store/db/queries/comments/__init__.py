from .queries import create_comment
from .queries import get_comments_from_db
from .queries import update_comment

__all__ = [
    "get_comments_from_db",
    "create_comment",
    "update_comment",
]
