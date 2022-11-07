from collections import defaultdict
from sqlalchemy.engine import Engine
import datetime
from db import db
from config import Config
import inspect
from statistics import mean
from sqlalchemy import event

queries_types = defaultdict(int)
slow_queries = []
query_times = []

@event.listens_for(db.Session, 'do_orm_execute')
def receive_do_orm_execute(orm_execute_state):
    
    if orm_execute_state.is_select:
        queries_types["selects"] =+ 1
    if orm_execute_state.is_insert:
        queries_types["inserts"] =+ 1

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(datetime.datetime.now())


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    time_for_query = datetime.datetime.now() - conn.info["query_start_time"].pop(-1)

    if "SAVEPOINT" not in statement and 'pytest_pyfunc_call' in [frame.function for frame in inspect.stack()]:
        if time_for_query.microseconds/1000 > Config.WARN_IF_QUERIES_OVER_MS:
            slow_queries.append({"query_statement" : statement, "query_time" : time_for_query.microseconds/1000})
        query_times.append(time_for_query.microseconds/1000)
        

def pytest_addoption(parser):
    parser.addoption(
        "--testrows",
        action="store",
        default=20,
        help="The amount of rows to use when testing the db.",
        type=int,
    )

    parser.addoption(
        "--rowsperapp",
        action="store",
        default=10,
        help="The amount of rows to assign to each app use when testing the db.",
        type=int,
    )


def pytest_terminal_summary(terminalreporter):
    terminalreporter.section("Database test information")
    rows_to_create = terminalreporter.config.option.testrows
    database_url = Config.SQLALCHEMY_DATABASE_URI
    terminalreporter.write_line(f"Database URL: {database_url}")
    terminalreporter.write_line(f"Test rows created: {rows_to_create} (Adjust with --testrows=INT)")

    terminalreporter.section("SQL Query information")
    terminalreporter.write_line(f"Average query time: {round(mean(query_times), 3)}")
    if slow_queries != []:
        terminalreporter.write_line(f"Slow queries found!")
        for query in slow_queries:
            terminalreporter.write_line("-" * 10)
            terminalreporter.write_line(f"Time taken : {query['query_time']}ms")
            terminalreporter.write_line(f"Query: {query['query_statement']}")
