import csv


def load_from_csv(filename):
    data = []
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append([float(val) for val in row])
    return data


def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
