import requests
from bs4 import BeautifulSoup
from scraper import extract_data

# Try to retrieva an URL
def fetch_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        raise ConnectionError('Could not connect to website')


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"

for letter in ALPHABET:
    # Get reference to current letter page
    html_ref = f"https://www.fass.se/LIF/pharmaceuticallist?userType=2&page={letter}"
    soup = fetch_url(html_ref)

    # Get all tags containing names of drugs
    names = soup.select('.productResultPanel .expandcontent .innerlabel')
    # Get all tags containing links to drug info
    links = soup.select('.productResultPanel .expandcontent .linkList a')

    # Extract the actual text and link from each tag
    extracted_names = [name.get_text().strip() for name in names]
    extracted_links = ["https://www.fass.se/LIF" + link.get('href').strip()[1:9] + link.get('href').strip()[link.get('href').strip().find('?') : ] for link in links]

    for link in extracted_links:
        soup2 = fetch_url(link)
        print(extract_data(soup2))
        
