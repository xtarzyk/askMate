import csv


def read_csv_file(filename):
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            return line