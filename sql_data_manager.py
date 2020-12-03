from psycopg2.extras import RealDictCursor, execute_values

import database_common
import time
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
    new_id = new_id + 1
    return new_id


@database_common.connection_handler
def get_question_by_id(cursor: RealDictCursor, id_number: str) -> list:
    query = """
    SELECT *
    FROM questions
    WHERE question_id = %(question_id)s
    """
    cursor.execute(query, {'question_id': id_number})
    query_result = cursor.fetchall()
    question = [*query_result[0].values()]
    return question


@database_common.connection_handler
def delete_question_by_id(cursor: RealDictCursor, id_number: str) -> list:
    query = """
    DELETE FROM questions
    WHERE question_id = %(question_id)s
    """
    cursor.execute(query, {'question_id': id_number})


@database_common.connection_handler
def update_question(cursor: RealDictCursor, id_number: int, new_title: str, new_message: str) -> list:
    query = """
    UPDATE questions
    SET title = %(title)s, message = %(message)s
    WHERE question_id = %(question_id)s
    """
    cursor.execute(query, {'question_id': id_number, 'title': new_title, 'message': new_message})


@database_common.connection_handler
def last_questions(cursor: RealDictCursor, number: int) -> list:
    query = """
    SELECT *
    FROM questions
    ORDER BY submission_time desc
    LIMIT %(number)s
    """

    cursor.execute(query, {'number': number})
    query_result = cursor.fetchall()
    questions_list = []
    for i in range(len(query_result)):
        question = [*query_result[i].values()]
        questions_list.append(question)
    return questions_list


@database_common.connection_handler
def all_question(cursor: RealDictCursor) -> list:
    query = """
    SELECT *
    FROM questions
    """
    cursor.execute(query)
    query_result = cursor.fetchall()
    questions_list = []
    for i in range(len(query_result)):
        question = [*query_result[i].values()]
        questions_list.append(question)
    return questions_list


def select_question_by(select) -> list:
    if select == 'title':
        query = """
        SELECT *
        FROM questions
        ORDER BY title asc 
        """
        return execute(query)
    elif select == 'oldest':
        query = """
        SELECT *
        FROM questions
        ORDER BY submission_time asc 
        """
        return execute(query)
    elif select == 'latest':
        query = """
        SELECT *
        FROM questions
        ORDER BY submission_time desc
        """
        return execute(query)
    elif select == 'views: asc':
        query = """
        SELECT *
        FROM questions
        ORDER BY view_number asc
        """
        return execute(query)
    elif select == 'views: desc':
        query = """
        SELECT *
        FROM questions
        ORDER BY view_number desc
        """
        return execute(query)
    elif select == 'votes: asc':
        query = """
        SELECT *
        FROM questions
        ORDER BY vote_number asc
        """
        return execute(query)
    elif select == 'votes: desc':
        query = """
        SELECT *
        FROM questions
        ORDER BY vote_number desc
        """
        return execute(query)
    else:
        return all_question()


@database_common.connection_handler
def execute(cursor: RealDictCursor, query):
    cursor.execute(query)
    query_result = cursor.fetchall()
    questions_list = []
    for i in range(len(query_result)):
        question = [*query_result[i].values()]
        questions_list.append(question)
    return questions_list
