import os
import time
import xml.etree.ElementTree as ET
import ssl
import urllib3
import requests
from pdfquery import PDFQuery

class CustomHttpAdapter (requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session


def download_file(nlpid, doctype, url, lang):
    response = get_legacy_session().get(url)
    if response.status_code != 200:    
        raise ConnectionError('Could not connect to website')
    
    path = f"data/productdocs/{lang}/{nlpid}_{doctype}.pdf"

    if not os.path.exists(f"data/productdocs/{lang}"):
        os.makedirs(f"data/productdocs/{lang}")

    with open(path, "wb") as file:
        file.write(response.content)

def verify_file(nlpid, doctype, url, lang):
    response = requests.get(url)
    if response.status_code != 200: 
        return  
    
    path = f"data/productdocs/{lang}/{nlpid}_{doctype}.pdf"

    if os.path.getsize(path) != response.content.__sizeof__:
        print(f"Filesize does not match {path}")


def download_files():
    with open("data/produktdokument.xml","r") as products:
        root = ET.parse(products).getroot()

        for product in root.findall("DocumentList"):
            break
            doctype = product.find("Typ").text
            if doctype != "PL" and doctype != "SmPC":
                continue

            lang = product.find("Språk").text
            nlpid = product.find("NplId").text
            url = product.find("DokumentLänk").text
            print(url)
            download_file(nlpid, doctype, url, lang)

    pdf = PDFQuery('data/productdocs/Svensk/20150626000039_PL.pdf')
    pdf.load()
    pdf.tree.write('test.xml',pretty_print=True)
            

download_files()
