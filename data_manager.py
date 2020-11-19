import csv


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


def write_csv_file(filename, dictionary):
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dictionary:
            writer.writerow(data)

# powyższe do sprawdzenia czy zadziała
