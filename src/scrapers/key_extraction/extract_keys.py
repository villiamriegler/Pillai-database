import os
import json
from collections import defaultdict
from pprint import pprint
PRODUCT_DIR = '../products'
META_DIR = '../metadata'
OUTPUT_FILE = os.path.join(META_DIR, 'fass_keys.json')


# Gets the filenames from products directory 
#   Function may error if directory contains incorrect information
def get_files():
    ALLOWED_SUBDIRECTORIES = []
    error = False

    (dirpath, dirnames, filenames) = next(os.walk(PRODUCT_DIR), (None, None, []))

    if dirnames != ALLOWED_SUBDIRECTORIES:
        print(f"""
            Unlawfull subdirectories {dirpath} inside {PRODUCT_DIR}
                * If this is intended update this file
                * Otherwise please remove the directory\n
        """)
        error = True

    if dirpath != PRODUCT_DIR:
        print(f"""
            Walking incorrect directory {dirpath}\n
        """)
        error = True

    if filenames == []:
        print("""
            No files in directory\n
        """)
        error = True

    if error:
        exit(1)

    return filenames


# Retive json data from file
def get_json_from_file(filename):
    json_data = {}

    # Asserting that file is a json file
    #   Does not cause error, simply does not return data
    if not filename.endswith('.json'):
        print(f"""
            WARN: {filename} is not a json file\n
        """)
        return {}

    # Opens file and retrives data in a dictionary 
    file_path = os.path.join(PRODUCT_DIR, filename)
    with open(file_path) as product_file:
        json_data = json.load(product_file)

    return json_data


# Iterate over all files in products
def walk_products():
    # Dictionary with default values of default type being a set
    key_values = defaultdict(set)

    # Iterating over files in the directory
    for file in get_files():
        # Retrive data from file
        data = get_json_from_file(file)

        keys = data.keys()
        for page in keys:
            # Append keys not seen before to page
            key_values[page].update(data[page].keys())

    return key_values


# Converts sets into lists in order to be serialized into json
def post_process(dictionary):
    for key in dictionary.keys():
        dictionary[key] = list(dictionary[key])

    return dictionary

if __name__ == '__main__':
    with open(OUTPUT_FILE, "w") as outfile:
        output = post_process(walk_products())
        json.dump(output, outfile, ensure_ascii=False, indent=4)
