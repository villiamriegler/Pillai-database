import os
import psycopg2
from time import sleep
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
import re
import zipfile
import json
from io import BytesIO
from pdfminer.high_level import extract_text
from requests.exceptions import HTTPError
import time


# Load environment variables
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_pass = os.getenv('POSTGRES_PASSWORD')
db_host = 'db'  # Docker Compose service name for the DB

# Constants
NPL_URL = 'https://npl.mpa.se/MpaProductExport/4.3/'
VARA_URL = 'https://vara.ehalsomyndigheten.se/vara-web/visaProdukt.xhtml?id='
PRODUCT_XML = 'products.xml'
JSON_FILE = 'products.json'

# Language codes
LANGUAGES = {
    'svensk': 'SV',
    'engelsk': 'EN'
}

# Demo mode with only a few products
demo_mode = True
demo_products = [
    '20010601000082',
    '20170809000076',
    '20080306000045',
    '20190806000015'    
]


# Download a product leaflet as PDF
def download_pdf(url, language, name, type, npl):
    try:
        # Get the URL and load content
        response = requests.get(url)
        response.raise_for_status()
        pdf_content = BytesIO(response.content)

        # Create directory if it does not exist
        os.makedirs(f'products/{language}', exist_ok=True)

        # Save the PDF to directory
        pdf_filename = f'products/{language}/{npl}.{name}.{type}.pdf'
        with open(pdf_filename, 'wb') as pdf_file:
            pdf_file.write(pdf_content.getbuffer())
        
        return pdf_content
    # Handle errors
    except HTTPError as e:
        print(f'Warning: HTTP error occurred while downloading PDF from {url} - {e}')
    except Exception as e:
        print(f'Error: An error occurred while downloading PDF from {url} - {e}')

    return None

# Get EAN code based on NPL-ID from VARA
def get_ean_code(npl):
    try:
        # Get product page from VARA
        response = requests.get(VARA_URL + npl)
        response.raise_for_status() 

        # Parse the HTML content 
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table by ID
        table = soup.find('table', id='article-table')

        # Collect all product codes in table
        product_codes = []
        for row in table.find_all('tr', class_='table__list-item--secondary'):
            # Extract columns
            cols = row.find_all('td')
            
            # Extract product codes from column 3
            if len(cols) > 2:
                product_code = cols[2].text.strip()  
                product_codes.append(product_code)

        return product_codes
    # Handle errors
    except requests.RequestException as e:
        print(f"Error: An error occurred while fetching product EAN from {VARA_URL + npl}: {e}")
        return []

# Exctract product information from XML, download PDF:s
def download_all_pdfs(file_path):
    print(f'Downloading files [Demo mode = {demo_mode}]')
    
    # Get XML root
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Find all DocumentList tags
    document_list = root.findall('.//DocumentList')
    total_documents = len(document_list)

    # Loop through all documents
    for index, document in enumerate(document_list, start=1):
        # Extract data
        npl = document.find('NplId').text if document.find('NplId') is not None else None
        link = document.find('DokumentLänk').text if document.find('DokumentLänk') is not None else None
        name = document.find('ProduktNamn').text if document.find('ProduktNamn') is not None else None
        type = document.find('Typ').text if document.find('Typ') is not None else None
        language = document.find('Språk').text if document.find('Språk') is not None else None
        
        # Convert language to shorter name [SV, EN]
        language = LANGUAGES.get(language.lower(), language)
        
        # Remove bad characters from name
        name = name.replace('/', '_')
        
        # Demo mode
        if demo_mode and npl not in demo_products:
            pass

        # Validate informarion
        if npl and npl in demo_products and link and link.endswith('.pdf'):
            print(f'Downloading document {index} of {total_documents}, NPL: {npl}, {(index/total_documents)*100:.2f}%')
            download_pdf(link, language, name, type, npl)


def process_downloaded_pdfs():
    # Collect all data in a list
    processed_data = []
    pdf_directory = 'products'

    # Seperate languages
    for language in os.listdir(pdf_directory):
        # Process each file
        for filename in os.listdir(pdf_directory + '/' + language):
            if filename.endswith('.pdf'):
                # Exctract relevant data
                npl = filename.split('.')[0]
                name = filename.split('.')[1]
                pdf_path = os.path.join(pdf_directory+ '/' + language, filename)
                ean_codes = get_ean_code(npl)

                # Convert PDF-file to text
                with open(pdf_path, 'rb') as pdf_file:
                    pdf_text = extract_text(pdf_file)
                    # Append data
                    processed_data.append({
                        'npl': npl,
                        'name': name,
                        'text': pdf_text,
                        'language': language,
                        'ean': ean_codes
                    })

    return processed_data

# Save data to JSON file
def save_to_json(data, json_file_path):
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Load data from JSON file
def load_data_from_json(json_file_path):
    with open(json_file_path, 'r') as file:
        return json.load(file)

# Insert data into database
def insert_into_database(data):
    # Connection to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=db_name, 
        user=db_user, 
        password=db_pass, 
        host=db_host
    )

    # Establish cursor
    cursor = conn.cursor()

    try:
        for product in data:
            # Insert data into leaflets
            leaflet_query = """
                INSERT INTO leaflets (npl, language, text) VALUES (%s, %s, %s)
                ON CONFLICT (npl) DO NOTHING;
            """
            cursor.execute(leaflet_query, (product['npl'], product['language'], product['text']))

            # Insert all product EAN-codes
            for ean in product['ean']:
                product_query = """
                    INSERT INTO products (ean, npl, name) VALUES (%s, %s, %s)
                    ON CONFLICT (ean) DO NOTHING;
                """
                cursor.execute(product_query, (ean, product['npl'], product['name']))

        conn.commit()
    except psycopg2.Error as e:
        # Handle errors
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        # Close connection
        cursor.close()
        conn.close()


# Download latest NPL data from Läkemedelsverket (NOT USED)
def download_newest_npl():
    response = requests.get(NPL_URL)
    response.raise_for_status()  

    # Parse content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all Total .zip links
    zip_links = soup.find_all('a', href=re.compile(r'Total.*\.zip$'))
    

    # No .zip files found
    if not zip_links:
        print('Error: No zip files found.')
        return
    
    # Get zip name
    filename = os.path.basename(zip_links[-1]['href'])
    
    # Check if the file already exists
    if os.path.exists(filename):
        print(f"'{filename}' already exists. No download needed.")
        return

    # Get link to newest (last) zip
    file_ref = 'https://npl.mpa.se/' + zip_links[-1]['href']

    # Download the last zip file
    download_response = requests.get(file_ref)
    download_response.raise_for_status()

    # Save the file
    filename = os.path.basename(filename)
    with open(filename, 'wb') as file:
        file.write(download_response.content)
    
    # Unpack the ZIP file
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall('.')

    with conn.cursor() as cur:
        print('Leaflets:')
        cur.execute('SELECT * FROM leaflets')
        for row in cur.fetchall():
            print(row)

        print('\nProducts:')
        cur.execute('SELECT * FROM products')
        for row in cur.fetchall():
            print(row)

# Print the contents of the database
def print_database():
    # Connection to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=db_name, 
        user=db_user, 
        password=db_pass, 
        host=db_host
    )
    cur = conn.cursor()

    try:
        # Query all data from leaflets table
        cur.execute("SELECT * FROM leaflets")
        print("Leaflets:")
        for row in cur.fetchall():
            print(row)

        # Query all data from products table
        cur.execute("SELECT * FROM products")
        print("\nProducts:")
        for row in cur.fetchall():
            print(row)

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        cur.close()
        conn.close()

def main():
    # Download all PDFs
    download_all_pdfs(PRODUCT_XML)

    # Process the downloaded PDFs
    data = process_downloaded_pdfs()

    # Save the processed data to a JSON file
    save_to_json(data, JSON_FILE)
    
    # Insert data into database
    insert_into_database(data)
    
    # Print database contents
    print_database()
    
    print('Done')

if __name__ == '__main__':
    main()
    
