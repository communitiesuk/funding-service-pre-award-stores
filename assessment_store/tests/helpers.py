from sqlalchemy import func
from sqlalchemy.inspection import inspect
from tests.sql_infos import no_gather_sql
from db import db


def get_random_row(table):
    """get_random_row Uses a database-side select to get a random
    row. Does this by using a random offset with range (1, number of rows)

    :param table: Sqlalchemy mapper object
    :return: A random row from the given mapper.
    """
    with no_gather_sql("--test-helper"):
        primary_key_name = inspect(table).primary_key[0].name
        primary_key_column = getattr(table, primary_key_name)
        return (
            db.session.query(table)
            .offset(
                func.floor(
                    func.random()
                    * db.session.query(func.count(primary_key_column))
                )
            )
            .limit(1)
            .one()
        )
