from tqdm import tqdm
from os import path, walk, getenv
from firebase_admin import initialize_app, firestore, credentials
from dotenv import load_dotenv
from json import load, loads
import re

load_dotenv()

NPL_LENGHT = 14
LEAFLET_DIR = "../../scrapers/data/products"
SPECIAL_CHARS = ['-', '_']

# Connecting to Firebase
cert = loads(getenv("GOOGLE_APPLICATION_CREDENTIALS"))
cred = credentials.Certificate(cert)
app = initialize_app(cred)  # intiializes app form $GOOGLE_APPLICATION_CREDENTIALS

# Create client for leaflet collection
leaflets = firestore.client().collection('leaflets')

(_, _, filenames) = next(walk(LEAFLET_DIR))  # Get all Files in product directory

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

pbar = tqdm(filenames)  # Progress bar
for file in pbar:
    npl = file[:NPL_LENGHT]  # Get nplID from filename
    pbar.set_description("Migrating file with nplID=%s" % npl)

    # Get DATA
    with open(path.join(LEAFLET_DIR, file)) as json_file:
        data = load(json_file)

    # Remove any empty records
    post_process = {key: {k: v for k, v in val.items() if v} for key, val in data.items() if val}  

    # Convert to camelCase
    cc_dict = keys_to_camel_case(post_process)
    

    leaflets.document(npl).set(cc_dict)
