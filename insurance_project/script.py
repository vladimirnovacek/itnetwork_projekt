import csv
from insurance_app.models import Person

with open("insurance_app_person.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            keys = row
        else:
            parameters = {key: value for key, value in zip(keys, row)}
            p = Person(**parameters)
            p.set_password("heslo123")
            p.save()
        line_count += 1
