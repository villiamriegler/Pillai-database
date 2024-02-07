from typing import Generator
from scraper import *
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from concurrent.futures import ProcessPoolExecutor
import cchardet
from pprint import pprint
import json


def fetch_url(session: requests.Session, url: str, strainer: SoupStrainer) -> BeautifulSoup:
    # Send request for html content to webserver
    response = session.get(url)
    if response.status_code == 200:     # If the request was successful
        # Return html form page as bs4 soup
        return BeautifulSoup(response.text, 'lxml', parse_only=strainer)
    else:                               # Request was unsucessful, server responded with error or nothing
        raise ConnectionError('Could not connect to website')


class Crawler:
    FASS_BASE_LINK = str("https://www.fass.se/LIF")

    def retrive_medecine_links(self) -> Generator:
        ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
        PAGE_BASE_LINK = "https://www.fass.se/LIF/pharmaceuticallist?userType=2&page="

        only_list = SoupStrainer("li", attrs={"class": "tradeNameList"})
        session = requests.Session()

        for letter in ALPHABET:
            page_link = PAGE_BASE_LINK + letter
            soup = fetch_url(session, page_link, only_list)

            # """.tradeNameList .expandcontent > a"""
            links = soup.select(""".linkList > a""")

            for link in links:
                base = self.FASS_BASE_LINK + link.get('href')[1:]
                yield {
                    "NPLID": base[-14:],
                    "PL": base + "&docType=7",
                    "SmPC": base + "&docType=6",
                    "Fass": base + "&docType=3",
                    "Divisability": base + "&docType=2000",
                    "env-info": base + "&docType=78",
                    "Protection-info": base + "&docType=80"
                }
        session.close()

    def assert_content(self, npl, result):
        PAGES = {
            "bipacksedel": "PL",
            "produktresume": "SmPC",
            "fass_text": "Fass",
            "bilder_och_delbarhet": "Divisability",
            "miljöinformation": "env-info",
            "skyddsinfo": "Protection-info"
        }

        error = False
        with open(f"../data/products/{npl}.json", "r") as file:
            content = json.load(file)
            for key in content.keys():
                if content[key] != result[PAGES[key]]:
                    error = True
                    print(f"Npl {npl} Failed on: {key}")
                    #pprint(content[key])
                    #pprint(result[PAGES[key]])
        if not error:
            print(f"Npl {npl} successful")


    def scrape_pages(self, links: dict):
        result = {}
        only_content = SoupStrainer(
            "div", {"id": "readspeaker-article-content"})

        session = requests.Session()
        for page in links.keys():
            if page == "NPLID":
                continue

            soup = fetch_url(session, links[page], only_content)
            match page:
                case "PL":
                    result[page] = extract_product_leaflet(soup)
                case "Divisability":
                    result[page] = extract_delbarhet(soup)
                case _:
                    result[page] = extract_medical_text(soup)
        session.close()
        self.assert_content(links['NPLID'], result)


    def print_link(self, link):
        print(link)


    def crawl(self):
        with ProcessPoolExecutor() as executor:
            executor.map(self.scrape_pages, self.retrive_medecine_links())


if __name__ == "__main__":
    cr = Crawler()
    cr.crawl()
