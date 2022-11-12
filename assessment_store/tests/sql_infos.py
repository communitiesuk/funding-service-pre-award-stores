from contextlib import contextmanager
import datetime
from collections import defaultdict
from statistics import mean

from config import Config
from db import db
from rich import print as fancy_print
from rich.syntax import Syntax
from rich.text import Text
from sqlalchemy import event
from sqlalchemy.engine import Engine

query_info = {
    "queries_types": defaultdict(int),
    "slow_queries": [],
    "query_times": [],
}


@contextmanager
def no_gather_sql(comment):
    @event.listens_for(Engine, "before_cursor_execute", retval=True)
    def mark_as_ignore(
        conn, cursor, statement, parameters, context, executemany
    ):
        statement = statement + f"{comment}"
        return statement, parameters

    yield

    event.remove(Engine, "before_cursor_execute", mark_as_ignore)


def attach_listeners():
    @event.listens_for(db.Session, "do_orm_execute")
    def receive_do_orm_execute(orm_execute_state):

        if orm_execute_state.is_select:
            query_info["queries_types"]["selects"] = +1
        if orm_execute_state.is_insert:
            query_info["queries_types"]["inserts"] = +1

    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        conn.info.setdefault("query_start_time", []).append(
            datetime.datetime.now()
        )

    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        time_for_query = datetime.datetime.now() - conn.info[
            "query_start_time"
        ].pop(-1)

        filter_strings = [
            "--seeding-database",
            "SAVEPOINT",
            "--prepping-database",
            "--rollback-database",
            "--test-helper",
        ]

        if not any([substr in statement for substr in filter_strings]):
            if (
                time_for_query.microseconds / 1000
                > Config.WARN_IF_QUERIES_OVER_MS
            ):
                query_info["slow_queries"].append(
                    {
                        "statement": statement,
                        "time": time_for_query.microseconds / 1000,
                    }
                )
            query_info["query_times"].append(
                {
                    "statement": statement,
                    "time": time_for_query.microseconds / 1000,
                }
            )


def pytest_terminal_summary(terminalreporter):
    terminalreporter.section("Database test information")
    rows_to_create = terminalreporter.config.option.testrows
    statementdetails = terminalreporter.config.option.statementdetails
    database_url = Config.SQLALCHEMY_DATABASE_URI
    terminalreporter.write_line(f"Database URL: {database_url}")
    terminalreporter.write_line(
        f"Test rows created: {rows_to_create} (Adjust with --testrows=INT)"
    )

    terminalreporter.section("SQL Query information")
    query_times = [query["time"] for query in query_info["query_times"]]
    terminalreporter.write_line(
        f"Average query time: {round(mean(query_times or [0]), 3)}"
    )

    if query_info["slow_queries"] != []:
        terminalreporter.write_line("Slow queries found!")

        for query in query_info["slow_queries"]:

            statement_string = Text("Statement:", style="bold magenta")
            time_string = Text("Time:", style="bold green")

            statement = Syntax(
                query["statement"], "sql", theme="autumn", dedent=True
            )
            time = Text(f"{query['time']}", style="italic black")

            time_string.append(time)

            fancy_print(statement_string)
            fancy_print(statement)
            fancy_print(time_string)

    if statementdetails:
        for query in query_info["query_times"]:

            statement_string = Text("Statement:", style="bold magenta")
            time_string = Text("Time:", style="bold green")

            statement = Syntax(
                query["statement"],
                "sql",
                theme="xcode",
                dedent=True,
                background_color="default",
            )
            time = Text(f"{query['time']}", style="italic black")

            time_string.append(time)

            fancy_print(statement_string)
            fancy_print(statement)
            fancy_print(time_string)
