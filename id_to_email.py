import csv
import argparse
from ldap_query import *



def open_csv(filename):
    """
    This function opens the csv unsing the filename
    """
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            list_str = ','.join(row)
        id_list = list(list_str)

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
        new_person.set_id(id)
        new_person.find_details()
        people_list.append(new_person)
    
    return people_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(descrption="Find emails to the list of IDs.")
    parser.add_argument('filename', 
                        type=str, 
                        nargs='+',
                        help="the filename of the .csv file"
                        )
    args = parser.parse_args()
    filename = "{}.csv".format(args["filename"])
    id_list = open_csv(filename)
    id_list = remove_duplicates(id_list)
    people = find_data(id_list)
    
    #####debugging######
    for person in people:
        print("Name:{}, ID:{}, email:{}".format(person.name, person.id, person.email))

