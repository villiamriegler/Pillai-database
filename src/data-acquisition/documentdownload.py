import os
import time
import xml.etree.ElementTree as ET
import requests



def download_file(nlpid, doctype, url, lang):
    response = requests.get(url)
    if response.status_code != 200:    
        raise ConnectionError('Could not connect to website')
    
    path = f"data/productdocs/{lang}/{nlpid}_{doctype}.pdf"

    if not os.path.exists(f"data/productdocs/{lang}"):
        os.makedirs()

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
            doctype = product.find("Typ").text
            if doctype != "PL" and doctype != "SmPC":
                continue

            lang = product.find("Språk").text
            nlpid = product.find("NplId").text
            url = product.find("DokumentLänk").text
            download_file(nlpid, doctype, url, lang)

            

download_files()