import csv
import time


def read_csv_file(filename):
    new = {}
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            new[int(line['id'])] = {}
            id_number = int(line['id'])
            del line['id']
            new[id_number] = line
    return new


# do poniższej listy trzeba będzie dodać kolumnę "image" na końcu gdy dodawanie zdjęć będzie gotowe
csv_columns = ["id", "submission_time", "view_number", "vote_number", "title", "message"]


def write_csv_file(filename, dictionaries, write_method="a"):
    """
    params: nazwa pliku, lista słowników, opcjonalnie metoda zapisu: w/a
    returns: nothing
    potwierdzam, działa <3
    """
    with open(filename, write_method) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        if write_method == "w":
            writer.writeheader()
        for data in dictionaries:
            writer.writerow(data)


def convert_to_data(list_of_question):
    try:
        for i in range(len(list_of_question)):
            time_in_seconds = list_of_question[i][2]
            local_time = time.ctime(time_in_seconds)
            list_of_question[i][2] = local_time
    except:
        time_in_seconds = list_of_question
        local_time = time.ctime(time_in_seconds)
        list_of_question = local_time

    return list_of_question
