import psycopg2
from psycopg2.extras import RealDictCursor, execute_values

import database_common
#
# Funkcja zostawiona dla przykładu na później
# @database_common.connection_handler
# def get_mentors_by_last_name(cursor: RealDictCursor, last_name: str) -> list:
#     query = """
#         SELECT first_name, last_name, city
#         FROM mentor
#         WHERE LOWER(last_name) = LOWER(%(last_name)s)
#         ORDER BY first_name"""
#     cursor.execute(query, {'last_name': last_name})
#     return cursor.fetchall()

# @database_common.connection_handler
# def add_question(cursor: RealDictCursor, id: int , message: str, time: int, title: str, view: int, vote: int):
#     query = """
#         INSERT INTO questions
#         VALUES (%(id)s,
#         %(message)s,
#         %(time)s,
#         %(title)s,
#         %(view)s,
#         %(vote)s
#         );
#


@database_common.connection_handler
def load_database(cursor: RealDictCursor):
    cursor.execute(open("./data/database.sql", "r").read())


@database_common.connection_handler
def add_question(cursor: RealDictCursor, id_number, message, submission_time, title, view_number, vote_number):
    query = "INSERT INTO questions (question_id, " \
            "message, " \
            "submission_time, " \
            "title, " \
            "view_number, " \
            "vote_number) " \
            "VALUES %s"

    execute_values(cursor, query, [(id_number, message, submission_time, title, view_number, vote_number)])


@database_common.connection_handler
def get_max_id(cursor: RealDictCursor):
    query = """
    SELECT question_id 
    FROM questions
    ORDER BY question_id DESC
    LIMIT 1
    """

    cursor.execute(query)
    query_result = cursor.fetchall()
    new_id = [*query_result[0].values()][0]
    return new_id

# except (Exception, psycopg2.Error) as error :
#     if(connection):
#         print("Failed to insert record into mobile table", error)
#
# finally:
#     #closing database connection.
#     if(connection):
#         cursor.close()
#         connection.close()