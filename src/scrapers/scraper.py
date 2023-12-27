
PRODUCT_ID_INDEX = 5

"""
    Bipacksedel extraction
"""
def extract_medical_text(soup):
    data = {}
    # Select full div containing the medical text 
    fass_content = soup.select('.fass-content')

    # Every section is labled with an a tag defining what information followes
    #   used as index for our data dictionary
    headers = fass_content[0].find_all('a', id=True, recursive=False)

    for section in headers:
        try:
            title = section.get('id')
        except:
            continue
        headerpart_div = fass_content[0].find(id=title).find_next('div').get_text()    # Extract all text content folowing the lable
        info = " ".join(headerpart_div.split())                             # Clean up text removing \n \t and whitespace 
        data[title] = data.get(title, "") + info

    return data

def extract_fass_text(soup):
    data = {}
    # Select full div containing the medical text 
    fass_content = soup.select('.fass-content')

    # Every section is labled with an a tag defining what information followes
    #   used as index for our data dictionary
    headers = fass_content[0].find_all('h2')


    for section in headers:
        try:
            title = section.find('a', id=True).get('id')
        except:
            continue
        
        headerpart_div = fass_content[0].find(id=title).find_next('div').get_text()    # Extract all text content folowing the lable
        info = " ".join(headerpart_div.split())                             # Clean up text removing \n \t and whitespace 
        data[title] = data.get(title, "") + info

    return data

def extract_product_resume(soup):
    data = {}
    # Select full div containing the medical text 
    fass_content = soup.select('.fass-content')

    # Every section is labled with an a tag defining what information followes
    #   used as index for our data dictionary
    headers = fass_content[0].find_all('h2')


    for section in headers:
        try:
            title = section.find('a', id=True).get('id')
        except:
            title = 'övrig-information'

        html = ""
        for tag in section.next_siblings:
            if tag.name == "h2":
                break
            else:
                html += str(tag.get_text())

        info = " ".join(html.split()) # Clean up text removing \n \t and whitespace 
        data[title] = data.get(title, "") + info
    
    return data

def extract_debarhet(soup):
    div = soup.select(".tablet-delbarhet-information ")
    if len(div) == 0:
        return {}

    result = " ".join(div[0].get_text().split())
    colon_index = result.find(':') 

    return {"delbarhets-information": result[colon_index + 2:]} if colon_index > 0 else {}

def extract_package_info(soup):
    # List to keep all found product ID:s
    productIDs = []

    # Find all tables in fass-content
    tables = soup.select('.fass-content table')
    
    # Go through all tables
    for table in tables:
        # Get all rows in each table
        table_rows = table.select('tbody tr')

        for row in table_rows:
            # Get all cells for the row
            cells = row.find_all('td')
            # Only extract the product ID
            productIDs.append(cells[PRODUCT_ID_INDEX].get_text().strip())

    return {"product-id": productIDs}          


