import csv
import itertools
import random

def create_education_dictionary(n):
    education_dict = {}
    # Το path που περιέχει το csv αρχείο με τους επιστήμονες
    CSV_PATH = './computer_scientists_data.csv'
    with open(CSV_PATH, 'r', encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            education_values = eval(row['Education'])
            awards = int(row['#Awards'])
            surname = row['Surname']

            for education_value in education_values:
                education_str = education_value.strip("'\"")  # Αφαίρεση περιττών εισαγωγικών χαρακτήρων
                # Κατασκευή ενός dictionary που περιέχει ως key το education και ως value surname και awards
                if education_str not in education_dict:
                    education_dict[education_str] = [(surname, awards)]
                else:
                    education_dict[education_str].append((surname, awards))

    # Αφαίρεση επιστημόνων με κενό " " education 
    education_dict.pop('', None)

    # Ανακατεύει τα περιεχόμενα του dictionary
    education_dict = list(education_dict.items())
    random.shuffle(education_dict)
    education_dict = dict(education_dict)

    # Κρατάει μόνο τα n πρώτα στοιχεία του dictionary 
    education_dict = dict(itertools.islice(education_dict.items(), n))
    '''
    for key, value in education_dictionary.items():
        print(f"Education: {key}")
        print(f"Scientists/Awards: {value}")
        print()
    '''
    return education_dict

