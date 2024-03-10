import os
from tqdm import tqdm
from os import path, walk, getenv
from firebase_admin import initialize_app, firestore, credentials
from dotenv import load_dotenv
import json
from json import load, loads
import re
from translate import translate_json

# Load environment variables
load_dotenv()

NPL_LENGHT = 14
LEAFLET_DIR = "../../scrapers/data/products"
TOP_20_DIR = 'top_20'
SPECIAL_CHARS = ['-', '_']
TOP_19_NAMES = [
    "Alvedon", "Panodil", "Ipren", "Claritine",
    "Zyrtec", "Sudafed", "Bisolvon", "Imodium",
    "Laxoberal", "Losec", "Nexium", "Nicorette", 
    "Nicotinell", "Voltaren", "Canesten", "Daktarin",
    "Bisolvon", "Strepsils", "Läkerol"
]

# Connecti to Firebase
cert = loads(getenv("GOOGLE_APPLICATION_CREDENTIALS"))
cred = credentials.Certificate(cert)
app = initialize_app(cred)  # intiializes app from $GOOGLE_APPLICATION_CREDENTIALS

# Create client for leaflet collection
leaflets = firestore.client().collection('leaflets')

# Convert string to camelCase
def str_to_camel_case(s):
    # Ignore non-strings
    if not isinstance(s, (str, str)):
        raise ValueError('Input must be a string')
    
    # Split at any special characters
    words = re.split('[^a-zA-Z0-9åäöÅÄÖ]+', s)  
    
    # Merge into camelCase
    cc_str = words[0] + ''.join(word.capitalize() for word in words[1:])
    return cc_str

# Convert dictionary keys to camelCase
def keys_to_camel_case(obj):
    if isinstance(obj, dict):
        # Recursive call for dicts
        return {str_to_camel_case(k): keys_to_camel_case(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        # All elements in lists
        return [keys_to_camel_case(e) for e in obj]
    else: 
        # Standard string values
        return obj

def process_and_upload_data(npl, data, lang='sv'):
    # Remove any empty records and convert to camelCase
    processed = keys_to_camel_case({key: {k: v for k, v in val.items() if v} for key, val in data.items() if val})
    
    # Swedish and English collections
    collection = firestore.client().collection(lang)
    
    # Upload data
    collection.document(npl).set(processed)

# Matches files with a drug name containting the top 20
def matches_top_20(name):
    return any(top_string in name for top_string in TOP_19_NAMES)

def copy_to_top_20_folder(file_path, data):
    # Define the top_20 folder path
    
    # Create the folder if it doesn't exist
    os.makedirs(TOP_20_DIR, exist_ok=True)
    
    # Define the new file path
    new_file_path = os.path.join(TOP_20_DIR, os.path.basename(file_path))
    
    # Write the data to the new file in the top_20 folder
    with open(new_file_path, 'w', encoding='utf-8') as new_file:
        json.dump(data, new_file, ensure_ascii=False, indent=4)

# Check
def find_top_20(filename):
    file_path = os.path.join(LEAFLET_DIR, filename)
    # Open and load the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            # Check if 'product_name' key exists and matches the criteria
            if 'product_name' in data and 'product_name' in data['product_name']:
                product_name = data['product_name']['product_name']
                print(product_name)
                
                # Check if drug should be included
                if matches_top_20(product_name):
                    copy_to_top_20_folder(file_path, data)
                    
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file '{filename}'")



"""

    npl = filename.split('.')[0]  # Get nplID from filename
# Translate text
                    translated_data = translate_json(data)
                    
                    # Upload data
                    process_and_upload_data(npl, data, 'sv')
                    process_and_upload_data(npl, translated_data, 'en')
                    print(f'Uploaded {filename}')
"""

def main():   
    # Have not yet found all top 20 leaflets
    if not os.path.exists(TOP_20_DIR) and not len(os.listdir(TOP_20_DIR)) > 0:
        # Go through all files
        for filename in os.listdir(LEAFLET_DIR):
            # Only process JSON-files
            if filename.endswith('.json'):  
                find_top_20(filename)
               
    print("All top 20 files exists")
    
    (_, _, filenames) = next(walk(TOP_20_DIR))  # Get all Files in product directory
    
    pbar = tqdm(filenames)  # Progress bar
    for file in pbar:
        npl = file[:NPL_LENGHT]  # Get nplID from filename
        pbar.set_description("Migrating file with nplID=%s" % npl)

        # Get DATA
        with open(path.join(LEAFLET_DIR, file)) as json_file:
            sv_data = load(json_file)

        # Translate
        print('Translating...')
        en_data = translate_json(sv_data)
        
        # Upload data
        print('Uploading...')
        process_and_upload_data(npl, sv_data, 'sv')
        process_and_upload_data(npl, en_data, 'en')
        print(f'Uploaded {npl}')
                    
if __name__ == '__main__':
    main()