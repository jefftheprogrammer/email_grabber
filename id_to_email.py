from csv import writer, reader
import argparse
from ldap_query import *
from os import path, remove



def open_csv(filename):
    """
    This function opens the csv unsing the filename
    """
    with open(filename) as csv_file:
        file_reader = reader(csv_file, delimiter=',')
        id_list = []
        for row in file_reader:
            id_list.append(row[0])

    return id_list

def remove_duplicates(id_list):
    """
    This function removes the duplicated in id_list.
    """
    id_set = set(id_list)
    id_set_dup = id_set.intersection(id_set)
    id_set_diff = id_set.symmetric_difference(id_set)
    id_set_unique = id_set_dup.union(id_set_diff)
    id_list_unique = list(id_set_unique)

    return id_list_unique

def find_data(id_list):
    """
    This function iterates through id_list
    and returns a list of emails and names.
    """
    people_list = []
    for id in id_list:
        new_person = Query()
        new_person.id = id
        new_person.find_details()
        people_list.append(new_person)
    
    return people_list

def export_csv(people):
    if path.isfile("mailing_list_export.csv") == True:
        remove("mailing_list_export.csv")
    
    with open("mailing_list_export.csv", "w") as csv_file:
        file_writer = writer(csv_file)
        for person in people:
            file_writer.writerow([person.id,person.name,person.email])

def tester(people):
    for person in people:
        print("Name:{}, ID:{}, email:{}".format(person.name, person.id, person.email))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find emails to the list of IDs.")
    parser.add_argument('filename', 
                        type=str, 
                        nargs='+',
                        help="the filename of the .csv file"
                        )

    args = parser.parse_args()
    filename = "{}.csv".format(args.filename[0])
    id_list = open_csv(filename)
    print("id list:{}".format(id_list))
    id_list = remove_duplicates(id_list)
    print("id list without dup:{}".format(id_list))
    people = find_data(id_list)
    export_csv(people)


