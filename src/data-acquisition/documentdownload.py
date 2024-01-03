import os
import time
import xml.etree.ElementTree as ET
import requests

import urllib3
import ssl



def download_file(nlpid, doctype, url, lang):
    response = requests.get(url)
    if response.status_code != 200:    
        raise ConnectionError('Could not connect to website')
    
    path = f"data/productdocs/{lang}/{nlpid}_{doctype}.pdf"

    if not os.path.exists(f"data/productdocs/{lang}"):
        os.makedirs(path)

    with open(path, "wb") as file:
        file.write(response.content)



def download_files():
    with open("data/produktdokument.xml","r") as products:
        root = ET.parse(products).getroot()

        for product in root.findall("DocumentList"):
            doctype = product.find("Typ").text
            if doctype != "PL" and doctype != "SmPC":
                continue

            lang = product.find("Språk").text
            nlpid = product.find("NplId").text
            url = product.find("DokumentLänk").text
            download_file(nlpid, doctype, url, lang)

            

download_files()