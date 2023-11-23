import csv
import itertools

def create_education_dictionary(csv_file):
    education_dict = {}

    with open(csv_file, 'r', encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            education_str = row['Education'].strip('[]').replace("'", "").replace("\"", "")  # Remove brackets and quotes
            surname = row['Surname']
            awards = row['#Awards']

            # If the education key is not in the dictionary, add it
            if education_str not in education_dict:
                education_dict[education_str] = [(surname, int(awards))]
            else:
                # If it already exists, add it to the existing list
                education_dict[education_str].append((surname, awards))

    # Remove scientists with an empty education
    education_dict.pop('', None)

    return education_dict

if __name__ == '__main__':
    # Το path που περιέχει το csv αρχείο με τους επιστήμονες
    CSV_PATH = './computer_scientists_data.csv'

    # Αποθηκεύει το dictionary με τους επιστήμονες σε μια μεταβλητή
    education_dictionary = create_education_dictionary(CSV_PATH)

    # Κρατάει μόνο τα n πρώτα στοιχεία του dictionary 
    education_dictionary = dict(itertools.islice(education_dictionary.items(), 20))

    for key in education_dictionary.keys():
        print(key)