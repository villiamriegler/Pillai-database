from os import path, walk, getenv
from firebase_admin import initialize_app, firestore, credentials
from dotenv import load_dotenv
from json import load, loads
import json
import re
from validate_npl import get_common_eans

load_dotenv()

JSON_FILE = 'ean.json'

# Connecting to Firebase
cert = loads(getenv("GOOGLE_APPLICATION_CREDENTIALS"))
cred = credentials.Certificate(cert)
app = initialize_app(cred)  # intiializes app form $GOOGLE_APPLICATION_CREDENTIALS

# Create client for ean collection
eans = firestore.client().collection('eans')

# List of eans wanted in the database
wanted_eans = get_common_eans()

# Open and load from JSON file
with open(JSON_FILE) as f:
    data = json.load(f)

count = 0
for ean, npl in data.items():
    if ean not in wanted_eans:
        continue

    # Skip if the ean code contains other than numbers
    if not re.search("^\d+$", ean):
        continue

    eans.document(ean).set({
        'npl': npl
    })

    count = count + 1
    print("Done with " + str(count))