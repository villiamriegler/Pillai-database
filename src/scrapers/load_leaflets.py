import os
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
import re
import zipfile
from requests.exceptions import HTTPError
from tqdm import tqdm
import json

# Constants
NPL_URL = 'https://npl.mpa.se/MpaProductExport/4.3/'
VARA_URL = 'https://vara.ehalsomyndigheten.se/vara-web/visaProdukt.xhtml?id='
PRODUCT_XML = 'products.xml'

# Download latest NPL data from Läkemedelsverket (NOT USED)
def download_newest_npl():
    print("Starting download of NPL-data")
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
    if not os.path.exists(filename):
        # Get link to newest (last) zip
        file_ref = 'https://npl.mpa.se/' + zip_links[-1]['href']

        # Download the last zip file with a progress bar
        with requests.get(file_ref, stream=True) as download_response:
            download_response.raise_for_status()

            total_size_in_bytes = int(download_response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

            with open(filename, 'wb') as file:
                for data in download_response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()
    else:
        print(f"'{filename}' already exists. No download needed.")


    # Process the ZIP file without extracting everything
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        # Get all filenames in the ZIP archive
        all_files = zip_ref.namelist()

        # Filter filenames that start with 'Productdata/'
        productdata_files = [f for f in all_files if f.startswith('Productdata/')]

        # Initialize progress bar
        with tqdm(total=len(productdata_files), desc='Processing Productdata files', unit='file') as progress_bar:
            npl_names = []
            for f in productdata_files:
                # Extract the basename and remove the file extension
                filename_without_extension = os.path.splitext(os.path.basename(f))[0]
                npl_names.append(filename_without_extension)
                
                # Update progress bar
                progress_bar.update(1)

        # Saving the list of filenames to a JSON file
        with open('npl.json', 'w') as json_file:
            json.dump(npl_names, json_file, indent=4)



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
    
def main():
    download_newest_npl()
    # Load NPL-IDs from JSON
    with open('npl.json', 'r') as file:
        npl_ids = json.load(file)

    ean_to_npl_mapping = {}

    # Progress bar for fetching EAN codes
    with tqdm(total=len(npl_ids), desc="Fetching EAN Codes", unit="NPL-ID") as progress_bar:
        for npl_id in npl_ids:
            ean_codes = get_ean_code(npl_id)
            for ean in ean_codes:
                ean_to_npl_mapping[ean] = npl_id
            progress_bar.update(1)

    # Save EAN to NPL-ID mapping to JSON
    with open('ean.json', 'w') as file:
        json.dump(ean_to_npl_mapping, file, indent=4)

if __name__ == "__main__":
    main()
