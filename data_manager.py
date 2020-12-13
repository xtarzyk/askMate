import time


def convert_to_data(list_of_question):
    if type(list_of_question) == list:
        for i in range(len(list_of_question)):
            time_in_seconds = list_of_question[i][2]
            local_time = time.ctime(time_in_seconds)
            list_of_question[i][2] = local_time
    else:
        local_time = time.ctime(list_of_question)
        list_of_question = local_time

    return list_of_question
