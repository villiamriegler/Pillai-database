import requests
from bs4 import BeautifulSoup

def fetch_and_parse(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        raise ConnectionError('Could not connect to website')

def extract_data(soup):
    if soup:
        data = {}

        # Extract drug name
        fass_content_section = soup.find('div', class_='fass-content')
        drug_name_tag = fass_content_section.find('h2') if fass_content_section else None
        data['drug_name'] = drug_name_tag.text.strip() if drug_name_tag else 'Not Found'

        # Extract dosage
        dosage_and_form_tag = fass_content_section.find('span', class_='strength-form') if fass_content_section else None
        data['dosage_and_form'] = dosage_and_form_tag.text.strip() if dosage_and_form_tag else 'Not Found'

        # Extract active ingridient
        active_ingredient_tag = fass_content_section.find('span', class_='word-explaination') if fass_content_section else None
        data['active_ingredient'] = active_ingredient_tag.text.strip() if active_ingredient_tag else 'Not Found'

        # Extract description
        header_data_parts = soup.find_all('div', class_='headerdatapart')
        description_texts = [part.get_text(separator=' ', strip=True) for part in header_data_parts]
        data['description'] = ' '.join(description_texts)

        return data
    else:
        raise ConnectionError('Could not load data')

# URLS
url_alvedon = 'https://www.fass.se/LIF/product?userType=2&nplId=19750613000031'
url_trileptal = 'https://www.fass.se/LIF/product?userType=2&nplId=20011102000359'

# Parse data
soup = fetch_and_parse(url_alvedon)

# Extract data
drug_data = extract_data(soup)

print(drug_data)
