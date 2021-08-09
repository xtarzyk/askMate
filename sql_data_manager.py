from psycopg2.extras import RealDictCursor, execute_values
import database_common


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
def get_max_comment_id(cursor: RealDictCursor):
    query = """
    SELECT answer_id 
    FROM answers
    ORDER BY answer_id DESC
    LIMIT 1
    """

    cursor.execute(query)
    query_result = cursor.fetchall()
    if len(query_result) == 0:
        new_id = 1
    else:
        new_id = [*query_result[0].values()][0]
        new_id = new_id + 1
    return new_id


@database_common.connection_handler
def get_max_comment_of_comment_id(cursor: RealDictCursor):
    query = """
    SELECT comment_id 
    FROM comments
    ORDER BY comment_id DESC
    LIMIT 1
    """

    cursor.execute(query)
    query_result = cursor.fetchall()
    if len(query_result) == 0:
        new_id = 1
    else:
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
def update_comment(cursor: RealDictCursor, id_number: int, new_message: str) -> list:
    query = """
    UPDATE answers
    SET comment_message = %(comment_message)s
    WHERE answer_id = %(answer_id)s
    """
    cursor.execute(query, {'answer_id': id_number, 'comment_message': new_message})


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


@database_common.connection_handler
def increment_view(cursor: RealDictCursor, actual_question_id):
    get_query = """
    SELECT view_number 
    FROM questions
    WHERE question_id = %(question_id)s
    """

    post_query = """
    UPDATE questions
    SET view_number = %(view_number)s
    WHERE question_id = %(question_id)s
    """

    cursor.execute(get_query, {'question_id': actual_question_id})
    query_result = cursor.fetchall()
    new_view = [*query_result[0].values()][0]
    new_view = new_view + 1
    cursor.execute(post_query, {'view_number': new_view, 'question_id': actual_question_id})
    return new_view


@database_common.connection_handler
def add_comment(cursor: RealDictCursor, question_id, comment_message, time_of_add_comment, comment_vote, answer_id):
    query = "INSERT INTO answers (question_id, " \
            "comment_message, " \
            "comment_submission_time, " \
            "comment_vote_number, " \
            "answer_id ) " \
            "VALUES %s"

    execute_values(cursor, query, [(question_id, comment_message, time_of_add_comment, comment_vote, answer_id)])


@database_common.connection_handler
def get_comment_by_question_id(cursor: RealDictCursor,  question_ide):
    query = """
    select answers.question_id, comment_message, comment_submission_time, comment_vote_number, answer_id
    from questions
    join answers on questions.question_id = answers.question_id
    where answers.question_id = %(question_id)s
    order by answers.comment_vote_number desc
    """
    cursor.execute(query, {'question_id': question_ide})
    query_result = cursor.fetchall()
    comment_list = []
    for i in range(len(query_result)):
        question = [*query_result[i].values()]
        comment_list.append(question)
    return comment_list


@database_common.connection_handler
def get_comment_by_id(cursor: RealDictCursor, id_number: str) -> list:
    query = """
    SELECT *
    FROM answers
    WHERE answer_id = %(answer_id)s
    """
    cursor.execute(query, {'answer_id': id_number})
    query_result = cursor.fetchall()
    answer = [*query_result[0].values()]
    return answer


@database_common.connection_handler
def get_question_by_comment_id(cursor: RealDictCursor, id_number: str):
    query="""
    select question_id
    from answers
    where answer_id = %(answer_id)s
    """
    cursor.execute(query, {'answer_id': id_number})
    query_result = cursor.fetchall()
    ide = [*query_result[0].values()][0]
    return ide


@database_common.connection_handler
def get_all_of_question_by_comment_id(cursor: RealDictCursor, id_number: str):
    query = """
    select questions.question_id, questions.message, questions.submission_time, 
    questions.title, questions.view_number, questions.vote_number
    from questions
    join answers on questions.question_id = %(question_id)s
    """
    cursor.execute(query, {'question_id': id_number})
    query_result = cursor.fetchall()
    ide = [*query_result[0].values()]
    return ide


@database_common.connection_handler
def delete_comment_by_comment_id(cursor: RealDictCursor, comment_id: str):
    query = """
    DELETE FROM answers
    WHERE answer_id = %(answer_id)s 
    """
    cursor.execute(query, {'answer_id': comment_id})


@database_common.connection_handler
def delete_comment_by_question_id(cursor: RealDictCursor, question_id: str):
    query = """
    DELETE FROM answers
    WHERE question_id = %(question_id)s
    """
    cursor.execute(query, {'question_id': question_id})


@database_common.connection_handler
def add_comment_to_comment(cursor: RealDictCursor, answer_id, comment_id, comment_of_comment_message, comment_of_comment_submission_time,
                           comment_of_comment_vote):
    query = "INSERT INTO comments (answers_id, " \
            "comment_id, " \
            "comment_of_comment_message, " \
            "comment_of_comment_submission_time, " \
            "comment_of_comment_vote ) " \
            "VALUES %s"

    execute_values(cursor, query, [(answer_id, comment_id, comment_of_comment_message, comment_of_comment_submission_time,
                                    comment_of_comment_vote)])


@database_common.connection_handler
def list_of_comment_to_comment_by_comment_id(cursor: RealDictCursor, id_number: str):
    query = """
    select comments.answers_id, comments.comment_id, comments.comment_of_comment_message, 
    comments.comment_of_comment_submission_time, comments.comment_of_comment_vote
    from answers
    join comments on answers.answer_id = comments.answers_id
    where comments.answers_id = %(answer_id)s
    order by comment_of_comment_submission_time
    """
    cursor.execute(query, {'answer_id': id_number})
    query_result = cursor.fetchall()
    comment_list = []
    for i in range(len(query_result)):
        question = [*query_result[i].values()]
        comment_list.append(question)
    return comment_list


@database_common.connection_handler
def add_vote(cursor: RealDictCursor, answer_id, question_id):
    get_query = """
    SELECT comment_vote_number
    FROM answers
    WHERE question_id = %(question_id)s and answer_id = %(answer_id)s
    """

    post_query = """
        UPDATE answers
        SET comment_vote_number = %(comment_vote_number)s
        WHERE question_id = %(question_id)s and answer_id = %(answer_id)s
        """

    cursor.execute(get_query, {'question_id': question_id, 'answer_id': answer_id})
    query_result = cursor.fetchall()
    new_vote = [*query_result[0].values()][0]
    new_vote = new_vote + 1
    cursor.execute(post_query, {'question_id': question_id, 'answer_id': answer_id,
                                'comment_vote_number': new_vote})
    return new_vote


@database_common.connection_handler
def delete_vote(cursor: RealDictCursor, answer_id, question_id):
    get_query = """
    SELECT comment_vote_number
    FROM answers
    WHERE question_id = %(question_id)s and answer_id = %(answer_id)s
    """

    post_query = """
        UPDATE answers
        SET comment_vote_number = %(comment_vote_number)s
        WHERE question_id = %(question_id)s and answer_id = %(answer_id)s
        """

    cursor.execute(get_query, {'question_id': question_id, 'answer_id': answer_id})
    query_result = cursor.fetchall()
    new_vote = [*query_result[0].values()][0]
    new_vote = new_vote - 1
    cursor.execute(post_query, {'question_id': question_id, 'answer_id': answer_id,
                                'comment_vote_number': new_vote})
    return new_vote


@database_common.connection_handler
def add_user(cursor: RealDictCursor, user_name, password, registration_date):
    query = "INSERT INTO page_user (user_name, " \
            "password, " \
            "registration_date) " \
            "VALUES %s"

    execute_values(cursor, query, [(user_name, password, registration_date)])


@database_common.connection_handler
def add_vote_question(cursor: RealDictCursor, question_id):
    get_query = """
        SELECT vote_number
        FROM questions
        WHERE question_id = %(question_id)s 
        """

    post_query = """
            UPDATE questions
            SET vote_number = %(vote_number)s
            WHERE question_id = %(question_id)s 
            """

    cursor.execute(get_query, {'question_id': question_id})
    query_result = cursor.fetchall()
    new_vote = [*query_result[0].values()][0]
    new_vote = new_vote + 1
    cursor.execute(post_query, {'question_id': question_id,
                                'vote_number': new_vote})
    return new_vote


@database_common.connection_handler
def delete_vote_question(cursor: RealDictCursor, question_id):
    get_query = """
        SELECT vote_number
        FROM questions
        WHERE question_id = %(question_id)s 
        """

    post_query = """
            UPDATE questions
            SET vote_number = %(vote_number)s
            WHERE question_id = %(question_id)s 
            """

    cursor.execute(get_query, {'question_id': question_id})
    query_result = cursor.fetchall()
    new_vote = [*query_result[0].values()][0]
    new_vote = new_vote - 1
    cursor.execute(post_query, {'question_id': question_id,
                                'vote_number': new_vote})
    return new_vote
