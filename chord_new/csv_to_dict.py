import csv
import itertools

def create_education_dictionary(csv_file):
    education_dict = {}

    with open(csv_file, 'r', encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            education_values = eval(row['Education'])
            awards = int(row['#Awards'])
            surname = row['Surname']

            for education_value in education_values:
                education_str = education_value.strip("'\"")  # Remove excess quotes
                # If the education key is not in the dictionary, add it
                if education_str not in education_dict:
                    education_dict[education_str] = [(surname, awards)]
                else:
                    # If it already exists, add it to the existing list
                    education_dict[education_str].append((surname, awards))

    # Remove scientists with an empty education
    education_dict.pop('', None)

    return education_dict


# Το path που περιέχει το csv αρχείο με τους επιστήμονες
CSV_PATH = './computer_scientists_data.csv'

# Αποθηκεύει το dictionary με τους επιστήμονες σε μια μεταβλητή
education_dictionary = create_education_dictionary(CSV_PATH)

# Κρατάει μόνο τα n πρώτα στοιχεία του dictionary 
n = 3
education_dictionary = dict(itertools.islice(education_dictionary.items(), n))
print(education_dictionary)
for key, value in education_dictionary.items():
    print(f"Education: {key}")
    print(f"Scientists/Awards: {value}")
    print()