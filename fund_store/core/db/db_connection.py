from core.fund_round_dao import dummmy_db_connection

if True:
    db_connection = dummmy_db_connection()
else:
    db_connection = "a real connection"
