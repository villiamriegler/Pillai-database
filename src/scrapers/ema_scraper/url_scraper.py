

import os

import requests
from bs4 import BeautifulSoup

# URL of the website you want to scrape
url = 'https://example.com'

def get_links_from_url_en(url):
    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize a list to store the hrefs
    hrefs = []

    # Find all <small> tags and filter by text content
    for tag in soup.find_all('small'):
        if "svenska (sv)" in tag.text.strip().lower():
            print(tag.text.strip())
            # Navigate to the parent of the <small> tag
            parent = tag.parent
            
            # Find <a> tag within the parent and extract the href, if it exists
            a_tag = parent.find('a')
            if a_tag and a_tag.has_attr('href'):
                hrefs.append(a_tag['href'])

    return hrefs

def get_links_from_url_sv(url):
    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize a list to store the hrefs
    hrefs = []

    # Loop through each small tag
    for small_tag in soup.find_all('small'):
        # Check if the text 'svenska (SV)' is in the small tag
        if 'svenska (SV)'.lower() in small_tag.text.lower():
            parent_div = small_tag.find_parent('div')
            next_sibling_div = parent_div.find_next_sibling('div')
            a_tag = next_sibling_div.find('a')
            if a_tag and a_tag.has_attr('href'):
                hrefs.append(a_tag['href'])
    return hrefs

def download_pdfs(pdf_urls, folder='data'):
    """
    Download PDF files from a list of URLs and save them to a specified folder.

    Args:
    - pdf_urls: A list of URLs pointing to PDF files.
    - folder: Name of the folder where PDFs will be saved. Defaults to 'data'.
    """

    # Check if the folder exists, and create it if it doesn't
    if not os.path.exists(folder):
        os.makedirs(folder)

    for url in pdf_urls:
        try:
            # Send a GET request to the URL
            response = requests.get("https://www.ema.europa.eu/" + url)
            
            # Raise an HTTPError if the response status code is 4XX or 5XX
            response.raise_for_status()

            # Extract the PDF file name from the URL
            filename = url.split('/')[-1]
            
            # Ensure the file name ends with .pdf
            if not filename.lower().endswith('.pdf'):
                filename += '.pdf'

            # Define the full path for the file
            file_path = os.path.join(folder, filename)

            # Write the content of the response to a file in binary mode
            with open(file_path, 'wb') as file:
                file.write(response.content)

            print(f"Downloaded '{filename}' to '{folder}/'.")

        except requests.exceptions.RequestException as e:
            # Handle any errors that occur during the request
            print(f"Failed to download {url}: {e}")