import csv


def read_csv_file(filename):
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            return line


# do poniższej listy trzeba będzie dodać kolumnę "image" na końcu gdy dodawanie zdjęć będzie gotowe
csv_columns = ["id", "submission_time", "view_number", "vote_number", "title", "message"]

def write_csv_file(filename, dictionary):
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dictionary:
            writer.writerow(data)

# powyższe do sprawdzenia czy zadziała