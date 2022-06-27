import os

import flask_migrate
from config import Config


class SqliteTestDB:
    @classmethod
    def remove(cls):
        flask_root = Config.FLASK_ROOT
        db_file_name = Config.SQLITE_DB_NAME
        db_file_path = os.path.join(flask_root, db_file_name)
        if os.path.exists(db_file_path):
            os.remove(db_file_path)

    @classmethod
    def create(cls):
        cls.remove()
        flask_migrate.upgrade()
