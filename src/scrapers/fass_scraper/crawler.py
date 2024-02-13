from bs4 import BeautifulSoup, SoupStrainer
import grequests
from scraper import extract_delbarhet, extract_medical_text, extract_product_leaflet
from multiprocessing import Pool
import json

PAGES = ["bipacksedel", "produktresume", "fass_text",
         "bilder_och_delbarhet", "miljöinformation", "skyddsinfo"]

RETRY = []


def _request_execption_handler(resquest, exception):
    print(f"Request: {resquest} failed with error\n\t{exception}")


def convert_to_soup(response, strainer):
    if response is None:
        print("***FAILED Request***")
        return None

    if response.status_code == 200:     # If the request was successful
        # Return html form page as bs4 soup
        return BeautifulSoup(response.text, 'lxml', parse_only=strainer)

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


class MedicalPage:
    nplid = None
    name = None
    links = []

    responses = []
    json = {}

    PRODUCTS_DIR = "../data/products/"

    def __init__(self, nplid, name, baseLink):
        self.nplid = nplid
        self.name = name

        docTypes = [7, 6, 3, 2000, 78, 80]
        self.links = [baseLink + f"&docType={page}" for page in docTypes]

    def request_pages(self):
        rnew = [grequests.get(u) for u in self.links]
        return rnew

    def assign_responses(self, resp):
        self.responses = resp[:len(PAGES)]
        return resp[len(PAGES):]

    def scrape(self):
        result = {}
        only_content = SoupStrainer(
            "div", {"id": "readspeaker-article-content"})
        for response, page in zip(self.responses, PAGES):
            soup = convert_to_soup(response, only_content)

            if soup is None:
                RETRY.append(self)
                continue

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

    def write_result(self):
        with open(self.PRODUCTS_DIR + f"{self.nplid}.json", "w") as outfile:
            json.dump(self.json, outfile, ensure_ascii=False, indent=4)




def retrive_medecine_links():
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
    PAGE_BASE_LINK = "https://www.fass.se/LIF/pharmaceuticallist?userType=2&page="

    only_list = SoupStrainer("li", attrs={"class": "tradeNameList"})

    rs = (grequests.get(PAGE_BASE_LINK + u) for u in ALPHABET)
    responses = grequests.map(rs, exception_handler=_request_execption_handler)

    for response in responses:
        soup = convert_to_soup(response, only_list)

        # """.tradeNameList .expandcontent > a"""
        links = soup.select(""".linkList > a""")
        names = soup.select(".linkList .innerlabel")

        for (link, name) in zip(links, names):
            base = "https://www.fass.se/LIF" + link.get('href')[1:]
            yield MedicalPage(base[-14:], name.get_text().strip(), base)

    print("***Retry VALUES***")
    while len(RETRY) > 0:
        yield RETRY.pop(0)

def medecine_batch(batchsize):
    pages = []
    for idx, value in enumerate(retrive_medecine_links()):
        pages.append(value)

        if (idx % batchsize == batchsize - 1):
            yield pages
            pages = []

    yield pages


def get_medical_pages(batch):
    rs = []
    pages_in_batch = []

    batchsize = len(batch)

    for page in batch:
        rs += page.request_pages()
        pages_in_batch.append(page)

    responses = grequests.map(rs, exception_handler=_request_execption_handler)

    for page_in_batch in pages_in_batch:
        responses = page_in_batch.assign_responses(responses)

    print(f"***Batch of size: {batchsize} retrived***")

    return pages_in_batch


def scrape_page(page):
    page.scrape()
    page.write_result()
    print(f"\tMedecine {page.nplid} has been scraped")


def crawl():
    total = 0
    with Pool() as io_pool:
        with Pool() as scrape_pool:
            for requested_pages in io_pool.imap_unordered(get_medical_pages, medecine_batch(25)):
                total += len(requested_pages)
                scrape_pool.map(scrape_page, requested_pages)
    print(f"Total {total} medecines scraped")


if __name__ == '__main__':
    crawl()
