
"""
    Bipacksedel extraction
"""
def extract_medical_text(soup):
    data = {}
    # Select full div containing the medical text 
    fass_content = soup.select('.fass-content')

    # Every section is labled with an a tag defining what information followes
    #   used as index for our data dictionary
    headers = fass_content[0].find_all('a')

    for section in headers:
        title = section.get('id')
        headerpart_div = soup.find(id=title).find_next('div').get_text()    # Extract all text content folowing the lable
        info = " ".join(headerpart_div.split())                             # Clean up text removing \n \t and whitespace 
        data[title] = info

    return data

def extract_fass_text(soup):
    data = {}
    # Select full div containing the medical text 
    fass_content = soup.select('.fass-content')

    # Every section is labled with an a tag defining what information followes
    #   used as index for our data dictionary
    headers = fass_content[0].find_all('h2')


    for section in headers:
        title = section.find('a').get('id')
        headerpart_div = soup.find(id=title).find_next('div').get_text()    # Extract all text content folowing the lable
        info = " ".join(headerpart_div.split())                             # Clean up text removing \n \t and whitespace 
        data[title] = info

    return data

def extract_package_info(soup):
    productIDs = []
    tables = soup.select('.fass-content table')
    
    for table in tables:
        table_rows = table.select('tbody tr')

        for row in table_rows:
            cells = row.find_all('td')
            productIDs.append(cells[5].get_text().strip())

    return productIDs        
    

def extract_data(soup):
    if soup:
        data = extract_medical_text(soup)

        fass_content_section = soup.find('div', class_='fass-content')

        ## Extract dosage
        dosage_and_form_tag = fass_content_section.find('span', class_='strength-form') if fass_content_section else None
        data['dosage_and_form'] = dosage_and_form_tag.text.strip() if dosage_and_form_tag else 'Not Found'

        ### Extract active ingridient
        active_ingredient_tag = fass_content_section.find('span', class_='word-explaination') if fass_content_section else None
        data['active_ingredient'] = active_ingredient_tag.text.strip() if active_ingredient_tag else 'Not Found'

        return data

    else:
        raise ConnectionError('Could not load data')


