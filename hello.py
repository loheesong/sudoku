import csv, random

with open("puzzles.csv") as f:
    csv_reader = csv.reader(f, delimiter=',')
    line_count = len(list(csv_reader))
    print(line_count)
    f.seek(0)
    n = random.randint(0,line_count)
    print(n)
    for row in csv_reader:
        print(row)