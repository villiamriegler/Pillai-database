from bs4 import BeautifulSoup, SoupStrainer
import grequests
from scraper import extract_delbarhet, extract_medical_text, extract_product_leaflet
from multiprocessing import Pool
import json

# Every medecine has these pages to be scraped, these are the lables
PAGES = ["bipacksedel", "produktresume", "fass_text",
         "bilder_och_delbarhet", "miljöinformation", "skyddsinfo"]

# The docTypes of each page for a medical product, needs to be Aligned with PAGES
# Bipacksedel: 7, Produktresume: 6, Förpackningar: 30, Fass_text: 3, Bilder_och_delbarhet: 2000, Miljöinformation: 78, Skyddsinfo: 80
DOC_TYPES = [7, 6, 3, 2000, 78, 80]

# Every failed request gets appended to this list so that program can retry the request later
RETRY = []

# Notifies when a request fails


def _request_execption_handler(resquest, exception):
    print(f"Request: {resquest} failed with error\n\t{exception}")


# Conveverts and parses the content of a request into BeautifulSoup
def convert_to_soup(response, strainer):
    # Avoids checking the status of NoneType when reciving a failed request
    if response is None:
        print("***FAILED Request***")
        return None

    # If status code is 200 then the request was fully Successful and we can return the BeautifulSoup
    if response.status_code == 200:
        # Parsing engine lxml is the fastest https://www.crummy.com/software/BeautifulSoup/bs4/doc/#:~:text=lenient%20than%20html5lib.-,lxml%E2%80%99s%20HTML%20parser,-BeautifulSoup(markup%2C
        # The stainer allowes us to only parse parts of the recived html allowing speedup for parsing
        return BeautifulSoup(response.text, 'lxml', parse_only=strainer)

    # Any request with other staus than 200 is considerd falty and retried
    return None


def assert_content(result):
    original = {}
    with open(f"../data/products/{result[0]}.json", "r") as doc:
        original = json.load(doc)
    if original != result[1]:
        print(f"{result[0]} Failed")
        with open(f"{result[0]}.json", "w") as doc:
            json.dump(result[1], doc, indent=4, ensure_ascii=False)

    else:
        print(f"{result[0]} Successful")


# Interface to keep track of an gather information about a specific medical product
class MedicalPage:
    nplid = None  # The Id of medical product scraped from fass
    name = None   # Name of the medical product
    links = []    # A list of the links to each page in the medical product

    # A list of content responses from requesting all the pages,
    # This needs to be aligned with PAGES
    responses = []
    # The result after scraping all the pages
    json = {}

    # Relative link to where the json file should be stored
    PRODUCTS_DIR = "../data/products/"

    def __init__(self, nplid, name, baseLink):
        self.nplid = nplid
        self.name = name

        # Constructing all links to the relative pages of a medical product
        self.links = [baseLink + f"&docType={page}" for page in DOC_TYPES]

    # Creates AsyncRequest objects for every page of the medical product
    def request_pages(self):
        rnew = [grequests.get(u) for u in self.links]
        return rnew

    # Takes a list of responses and assigns first [len(pages)] to this product, sequentiallity is important to not mix up
    # requests with their responses
    def assign_responses(self, resp):
        self.responses = resp[:len(PAGES)]
        return resp[len(PAGES):]

    # Scrapes all pages of a medical product and puts the content in a Dict
    def scrape(self):
        result = {}

        # Strainer to only parse the relevant parts of the document
        only_content = SoupStrainer(
            "div", {"id": "readspeaker-article-content"})

        # Loops over all content retrived from fass and scrapes that page
        for response, page in zip(self.responses, PAGES):
            # Converting a request into BeutitifulSoup
            soup = convert_to_soup(response, only_content)

            # If conversion fails we need to retry this product
            if soup is None:
                RETRY.append(self)
                return {}

            # Diffrent pages have diffrent scraping methods
            match page:
                case "bipacksedel":
                    result[page] = extract_product_leaflet(soup)
                case "bilder_och_delbarhet":
                    result[page] = extract_delbarhet(soup)
                case _:
                    result[page] = extract_medical_text(soup)

        result['product_name'] = {'product_name': self.name}

        self.json = result

        return result

    # Writes the result to file
    def write_result(self):
        with open(self.PRODUCTS_DIR + f"{self.nplid}.json", "w") as outfile:
            json.dump(self.json, outfile, ensure_ascii=False, indent=4)


# For every A-Ö page we retrive every medecine listed, after all links are exausted it retuns the ones that need to be retied untill everything is scraped
def retrive_medecine_links():
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
    PAGE_BASE_LINK = "https://www.fass.se/LIF/pharmaceuticallist?userType=2&page="
    NPL_ID_OFFSETT = -14

    only_list = SoupStrainer("li", attrs={"class": "tradeNameList"})

    # Batches all pages into parallel requests
    rs = (grequests.get(PAGE_BASE_LINK + u) for u in ALPHABET)
    # Makes all requets in parallel
    responses = grequests.map(rs, exception_handler=_request_execption_handler)

    for response in responses:
        soup = convert_to_soup(response, only_list)

        links = soup.select(".linkList > a")  # Extracts all medecine links
        # Collects the names of medecines
        names = soup.select(".linkList .innerlabel")

        # Creates MedicalPage objects from every link on page
        for (link, name) in zip(links, names):
            # The base links is formed by fass domain and the relative link retrived removing first char '.'
            base = "https://www.fass.se/LIF" + link.get('href')[1:]
            yield MedicalPage(base[NPL_ID_OFFSETT:], name.get_text().strip(), base)

    # After exausting all normal medecines yield the ones that need retrying
    while len(RETRY) > 0:
        yield RETRY.pop(0)


# Batching togheter medcecines in groups instead of one by one
def medecine_batch(batchsize):
    pages = []

    # Looping over medecines
    for idx, value in enumerate(retrive_medecine_links()):
        pages.append(value)

        # yield batch when big enough
        if (idx % batchsize == batchsize - 1):
            yield pages
            pages = []

    # If we end with less than a full batch give a partial batch
    yield pages


# Requesting a batch of pages in parallel and assigning the responses accordingly
def get_medical_pages(batch):
    rs = []
    pages_in_batch = []

    batchsize = len(batch)

    # Loop over batch
    for page in batch:
        # Get AsyncRequest objects
        rs += page.request_pages()
        # Add pages as requested, needs to be aligned with rs
        pages_in_batch.append(page)

    # Make all requests in the batch in paralell
    responses = grequests.map(rs, exception_handler=_request_execption_handler)

    # Assign responses to the correct pages
    for page_in_batch in pages_in_batch:
        responses = page_in_batch.assign_responses(responses)

    print(f"***Batch of size: {batchsize} retrived***")

    # Return batch with Pages that have content
    return pages_in_batch


# Scrapes all pages of a MedicalPage and writes the result to file
def scrape_page(page):
    page.scrape()
    page.write_result()
    print(f"\tMedecine {page.nplid} has been scraped")


# Goes through all medicalPages and requests them in parallel while scraping them in paralell
def crawl():
    total = 0
    with Pool() as io_pool:
        with Pool() as scrape_pool:
            for requested_pages in io_pool.imap_unordered(get_medical_pages, medecine_batch(25)):  # Requesting the pages of N many MedicalPage:s in parallel at most N*cpu_count at once
                total += len(requested_pages)
                scrape_pool.map(scrape_page, requested_pages)  # Scraping the requested pages in parallel
    print(f"Total {total} medecines scraped")


if __name__ == '__main__':
    crawl()
