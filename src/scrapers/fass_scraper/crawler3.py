from bs4 import BeautifulSoup, SoupStrainer
import grequests
from typing import Generator
from multiprocessing import Pool
from scraper import extract_delbarhet, extract_medical_text, extract_product_leaflet
from itertools import chain, islice
import json

PAGES = ["bipacksedel", "produktresume", "fass_text",
         "bilder_och_delbarhet", "miljöinformation", "skyddsinfo"]


def _request_execption_handler(resquest, exception):
    print(f"Request: {resquest} failed with error\n\t{exception}")


def convert_to_soup(response, strainer):
    if response.status_code == 200:     # If the request was successful
        # Return html form page as bs4 soup
        return BeautifulSoup(response.text, 'lxml', parse_only=strainer)
    else:                               # Request was unsucessful, server responded with error or nothing
        raise ConnectionError('Could not connect to website')


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

    def __init__(self, nplid, name, baseLink):
        self.nplid = nplid
        self.name = name

        docTypes = [7, 6, 3, 2000, 78, 80]
        self.links = [baseLink + f"&docType={page}" for page in docTypes]

    def request_pages(self):
        rnew = (grequests.get(u) for u in self.links)
        self.responses = grequests.map(rnew)

    def scrape(self):
        if self.responses == []:
            raise ConnectionError("Pages were not retrived")

        result = {}
        only_content = SoupStrainer(
            "div", {"id": "readspeaker-article-content"})
        for response, page in zip(self.responses, PAGES):
            soup = convert_to_soup(response, only_content)

            match page:
                case "bipacksedel":
                    result[page] = extract_product_leaflet(soup)
                case "bilder_och_delbarhet":
                    result[page] = extract_delbarhet(soup)
                case _:
                    result[page] = extract_medical_text(soup)
        result['product_name'] = {'product_name': self.name}
        return result


def retrive_medecine_links() -> Generator:
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


# TODO: Batch requests or else whole operation is IO bound
def get_medical_pages() -> Generator:
    for page in retrive_medecine_links():
        page.request_pages()
        yield page


def scrape_page(page: MedicalPage):
    res = page.scrape()
    return (page.nplid, res)


def crawl():
    batchsize = 4
    with Pool() as pool:
        for result in pool.imap_unordered(scrape_page, islice(get_medical_pages(), 100), batchsize):
            assert_content(result)



if __name__ == '__main__':
    crawl()
