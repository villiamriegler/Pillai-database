import requests
from bs4 import BeautifulSoup
from scraper import extract_medical_text,extract_fass_text,extract_package_info

PAGES = {
    "bipacksedel": 7,
    "produktresume": 6,
    "förpackningar": 30,
    "fass-text": 3,
    "bilder-och-delbarhet": 2000,
    "miljöinformation": 78,
    "skyddsinfo": 80,
    "viktig-patientinfo": 15 
}

#viktig-patientinfo: https://www.fass.se/LIF/product?userType=2&nplId=20071201000025&docType=15&scrollPosition=0

# Try to retrieva an URL
def fetch_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        raise ConnectionError('Could not connect to website')


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
PRODUCT_BASE_LINK = "https://www.fass.se/LIF/product?nplId="

# Loop over every page in the a-ö list of pharmaceuticals
for letter in ALPHABET:
    # Get reference to current letter page
    html_ref = f"https://www.fass.se/LIF/pharmaceuticallist?page={letter}"
    soup = fetch_url(html_ref)

    # Get all tags containing names of drugs
    names = soup.select('.productResultPanel .expandcontent .innerlabel')
    # Get all tags containing links to drug info
    links = soup.select('.productResultPanel .expandcontent .linkList a')

    # Extract drug names
    product_names = [name.get_text().strip() for name in names]
    # Extract drug ids
    product_ids = [link.get('href').strip()[-14:] for link in links]

    
    for product_id in product_ids:
        # Full link to product
        full_url = PRODUCT_BASE_LINK + product_id

        # Check different pages for that product
        for (page,number) in PAGES.items():
            page_url = full_url + f"&docType={number}" 
            soup = fetch_url(page_url)
        
            match page:
                case "bipacksedel":
                    extract_medical_text(soup)
                case "produktresume":
                    pass
                case "förpackningar": 
                    extract_package_info(soup)
                case "fass-text":
                    extract_fass_text(soup)
                case "bilder-och-delbarhet":
                    pass
                case "miljöinformation":
                    pass
                case "skyddsinfo":
                    pass
                case "viktig-patientinfo": 
                    pass
        