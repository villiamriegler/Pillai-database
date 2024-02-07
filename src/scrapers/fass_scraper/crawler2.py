from typing import Generator
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import cchardet                 # improves bs4 parsing performance just by importing


class Request:
    session = requests.Session()

    def fetch_url(self, url: str, strainer: SoupStrainer) -> BeautifulSoup:
        # Send request for html content to webserver
        response = self.session.get(url)
        if response.status_code == 200:     # If the request was successful
            # Return html form page as bs4 soup
            return BeautifulSoup(response.text, 'lxml', parse_only=strainer)
        else:                               # Request was unsucessful, server responded with error or nothing
            raise ConnectionError('Could not connect to website')

class Crawler(Request):
    def retrive_medecine_links(self) -> Generator:
        ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
        PAGE_BASE_LINK = "https://www.fass.se/LIF/pharmaceuticallist?userType=2&page="

        only_list = SoupStrainer("li", attrs={"class": "tradeNameList"})

        for letter in ALPHABET:
            page_link = PAGE_BASE_LINK + letter
            soup = self.fetch_url(page_link, only_list)

            # """.tradeNameList .expandcontent > a"""
            links = soup.select(""".linkList > a""")

            for link in links:
                yield link.get('href')[1:]


if __name__ == "__main__":
    for nplid in Crawler().retrive_medecine_links():
        pass
