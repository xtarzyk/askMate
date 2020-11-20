
# otwieram csv


def open_file(file_name):
    with open(file_name, 'r') as file:
        question_file = file.readlines()
        result = []
        for question in question_file:
            result.append(question.strip().split(','))

    return result


# pobieram pytanie by id
def get_question_by_id(question_id):
    data_file = open_file('sample_data/question.csv')
    for question in data_file:
        if question[0] == question_id:
            return question


def get_answers_by_question_id(question_id):
    data_file = open_file('sample_data/answer.csv')
    result = []
    for answer in data_file:
        if answer[3] == question_id:
            result.append(answer)
    return result


def id_maker(dict_id):
    if len(dict_id) == 0:
        ide = 1
    else:
        max_key = max(dict_id, key=int)
        ide = max_key + 1
    return int(ide)

# def get_all_questions():
#     data_file = open_file('sample_data/movie_questions.csv')
#     return data_file
