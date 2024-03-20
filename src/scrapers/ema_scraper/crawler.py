from parse_csv import *
from url_scraper import *


def main(): 
    product_links = get_valid_drug_links()
    
    counter = 0
    for product_link in product_links:
        counter += 1
        print(f"Checking product {counter} / {len(product_links)}")
        
        pdf_links = get_links_from_url_en(product_link)

        download_pdfs(pdf_links)
        
if __name__ == "__main__":
    main()