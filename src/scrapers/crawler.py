import requests
from bs4 import BeautifulSoup
from scraper import *
from pprint import pprint

PAGES = {
    "bipacksedel": 7,
    "produktresume": 6,
    "förpackningar": 30,
    "fass-text": 3,
    "bilder-och-delbarhet": 2000,
    "miljöinformation": 78,
    "skyddsinfo": 80
}

# 0 = No print
# 1 = Print keys
# 2 = Print all
DEBUGING_PAGES = {
    "bipacksedel": 1,
    "produktresume": 1,
    "förpackningar": 1,
    "fass-text": 1,
    "bilder-och-delbarhet": 1,
    "miljöinformation": 1,
    "skyddsinfo": 1
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


# Print debuging info for all parsed data
def debug(key, result):
    match DEBUGING_PAGES[key]:
        case 2:
            pprint(result)
        case 1:
            print(result.keys())
        case _: 
            pass


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

    count = 0
    for product_id in product_ids:
        count += 1
        # Full link to product
        full_url = PRODUCT_BASE_LINK + product_id
        print(f"*****************************\n{full_url} {count}\n********************************")

        # Check different pages for that product
        for (page,number) in PAGES.items():
            page_url = full_url + f"&docType={number}" 
            soup = fetch_url(page_url)
            result = {}

            if soup is None:
                continue

            match page:
                case "bipacksedel":
                    # Keys retrived inside the medical-text

                    # 'user-information', 'product-information', 'indication', 
                    # 'caution-and-warnings', 'contraindication', 'caution', 
                    # 'interaction', 'pregnancy', 'driving', 'substance-information', 
                    # 'usage-and-administration', 'overdosage', 'missed', 
                    # 'withdrawal', 'side-effects', 
                    # 'additionalMonitoringInfo', 'storage', 'information-source', 
                    # 'composition', 'appearance', 'prod-license'
                    result = extract_medical_text(soup)
                case "produktresume":
                    # Keys retrived from first entry
                    
                    # 'tradename', 'composition', 'product-form', 'clinical', 
                    # 'pharmacological', 'pharmaceutical', 
                    # 'prod-license', 'approval-number', 'approval-first-date', 'revision-date'
                    result = extract_product_resume(soup)
                case "förpackningar": 
                    # All the package information 
                    result = extract_package_info(soup)
                case "fass-text":
                    # Keys retrived inside the fass-text

                    # 'indication', 'contraindication', 'dosage', 'caution', 
                    # 'interaction', 'pregnancy', 'breastfeeding', 'fertility', 
                    # driving', 'side-effects', 'overdosage', 'pharmacodynamic', 
                    # 'pharmacokinetic', 'preclinical-info', 'composition', 'env-effect', 
                    # 'handling-life-shelf-storage'
                    result = extract_fass_text(soup)
                case "bilder-och-delbarhet":
                    result = extract_debarhet(soup)
                case "miljöinformation":
                    result = extract_fass_text(soup)
                case "skyddsinfo":
                    result = extract_product_resume(soup)

            debug(page,result)
        
