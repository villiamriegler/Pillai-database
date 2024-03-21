from parse_csv import *
from url_scraper import *


def main(): 
    # Find all valid drug links
    product_links = get_valid_drug_links()
    
    counter = 0

    # Go through all links and find valid references to leaflet documents in Swedish or English
    for product_link in product_links:
        counter += 1
        print(f"Checking product {counter} / {len(product_links)}")
        
        # Change to "get_links_from_url_sv" for Swedish leaflets
        pdf_links = get_links_from_url_en(product_link)

        # Download all leaflets
        download_pdfs(pdf_links)
        
if __name__ == "__main__":
    main()