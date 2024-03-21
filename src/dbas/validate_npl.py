import json
import os

EAN_FILE = 'ean.json'
DIRECTORY = '../scrapers/data/products/'

list_of_eans = []
npl_without_ean = []

def get_common_eans():
    # Open file with ean codes
    f = open(EAN_FILE)

    # Load data from ean file
    data = json.load(f)

    # Loop through nplIDs as filenames
    for filename in os.listdir(DIRECTORY):
        t = False
        # Get nplID from file name
        file_npl = filename.split(".")[0]

        # Loop through ean codes in JSON file
        for ean in data:
            # Check if this is the current filename
            if file_npl == data[ean]:
                list_of_eans.append(ean)
                t = True

        if not t:
            npl_without_ean.append(filename)
    
    return list_of_eans
    # print("Total number of eans: " + str(len(data)))


def main():
    get_common_eans()
    print("Number of common eans: " + str(len(list_of_eans)))
    print("Number of filename npls withoud eans: " + str(len(npl_without_ean)))


if __name__ == '__main__': main()