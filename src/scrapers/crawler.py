import requests
from bs4 import BeautifulSoup
from scraper import *
from pprint import pprint

# viktig-patientinfo: https://www.fass.se/LIF/product?userType=2&nplId=20071201000025&docType=15&scrollPosition=0


# Fetches html content for web ardress and returns as bs4 soup
def fetch_url(url):
    # Send request for html content to webserver
    response = requests.get(url)
    if response.status_code == 200:     # If the request was successful
        # Return html form page as bs4 soup
        return BeautifulSoup(response.content, 'html.parser')
    else:                               # Request was unsucessful, server responded with error or nothing
        raise ConnectionError('Could not connect to website')


# Print debuging info for all parsed data
#   params: key(index of the page that was scraped, used to differenttiate between the information we want to display)
#           result(the scraped content from the page)
def debug(key, result):
    # 0 = No print
    # 1 = Print keys
    # 2 = Print all
    DEBUGING_PAGES = {
        "bipacksedel": 0,
        "produktresume": 0,
        "förpackningar": 0,
        "fass-text": 0,
        "bilder-och-delbarhet": 0,
        "miljöinformation": 0,
        "skyddsinfo": 0
    }

    match DEBUGING_PAGES[key]:
        case 2:     # Pretty print full dictionary
            pprint(result)
        case 1:     # Onl print the keys in the dictionary
            print(result.keys())
        case _:
            pass


# Scrapes the information from each page on a given url
#       params: page(the page to scrape, used to differentiate diffrent scraping methods for diffrent pages) 
#               soup(the html content of the page to scrape)
def extract_page_information(page, soup):
    result = {}

    # NOTE: some subcategories may be scraped using the same scraping method
    # example of this is both the fass-text and miljöinformation.
    # This is because the inforamtion followes the same format
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
            result = extract_medical_text(soup,'a',False,False)
        case "produktresume":
            # Keys retrived from first entry

            # 'tradename', 'composition', 'product-form', 'clinical',
            # 'pharmacological', 'pharmaceutical',
            # 'prod-license', 'approval-number', 'approval-first-date', 'revision-date'
            
            result = extract_medical_text(soup, 'h2', True, True)
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
            result = extract_medical_text(soup,'h2',True,True)
        case "bilder-och-delbarhet":
            result = extract_delbarhet(soup)
        case "miljöinformation":
            result = extract_fass_text(soup)
        case "skyddsinfo":
            result = extract_product_resume(soup)

    debug(page, result)
    return result


# Walks all the pages for a given medecine and extracts the information
#       params: full_url(the url of the base page to scrape)
def crawl_pages(full_url):
    # The url for each subcategory of medecine information can be indexed as
    # the base_url with an appended docType selector. The docType selection
    # uses the following magic numbers for each subcategory
    PAGES = {
        "bipacksedel": 7,
        "produktresume": 6,
        "förpackningar": 30,
        "fass-text": 3,
        "bilder-och-delbarhet": 2000,
        "miljöinformation": 78,
        "skyddsinfo": 80
    }

    url_result = {}
    # Iterate over the information subcategories
    for (page, number) in PAGES.items():
        # Creates the full url of subcategory to be scraped
        page_url = full_url + f"&docType={number}"

        # Fetches html content of the page
        soup = fetch_url(page_url)

        # Check if page exists
        if soup is None:
            continue

        # Extracting all information from medecine subcategory and stores the
        # result by subcategory in a dictionary of dictionaries
        url_result[page] = extract_page_information(page, soup)

    return url_result


# Crawls through all the medecines in the alpabetical list of medecines found on
# https://www.fass.se/LIF/pharmaceuticalliststart?userType=2
def crawl_alphabetical_list():
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
        product_ids = [link.get('href').strip()[-14:] for link in links]    # The product link is relative 
                                                                            # To get the absolute link we extract only the nplID of the link

        count = 0
        # Iterate over every product beginning with current letter
        for product_id in product_ids:
            count += 1
            # Full link to product
            full_url = PRODUCT_BASE_LINK + product_id
            print(
                f"*****************************\n{full_url} {count}\n********************************")

            # Retrive all information from pages
            page_information = crawl_pages(full_url)


if __name__ == '__main__':
    crawl_alphabetical_list()
