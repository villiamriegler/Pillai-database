from os import path, walk, getenv
from firebase_admin import initialize_app, firestore, credentials
from dotenv import load_dotenv
from json import load, loads


load_dotenv()

NPL_LENGHT = 14
LEAFLET_DIR = "../../scrapers/data/products"

# Connecting to Firebase
cert = loads(getenv("GOOGLE_APPLICATION_CREDENTIALS"))
cred = credentials.Certificate(cert)
app = initialize_app(cred)  # intiializes app form $GOOGLE_APPLICATION_CREDENTIALS

# Create client for leaflet collection
leaflets = firestore.client().collection('leaflets')

(_, _, filenames) = next(walk(LEAFLET_DIR))  # Get all Files in product directory
for num, file in enumerate(filenames):
    npl = file[:NPL_LENGHT]  # Get nplID from filename

    # Get DATA
    with open(path.join(LEAFLET_DIR, file)) as json_file:
        data = load(json_file)

    post_process = {key: {k: v for k, v in val.items() if v} for key, val in data.items() if val}  # Remove any empty records

    leaflets.document(npl).set(post_process)
