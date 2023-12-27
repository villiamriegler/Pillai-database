
PRODUCT_ID_INDEX = 5


# Scarping method for extracting the bipacksedel subcategory on fass.se
# Example page: https://www.fass.se/LIF/product?userType=2&nplId=20190822000136&docType=7&scrollPosition=352
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

        headerpart_div = fass_content[0].find(id=title).find_next('div').get_text()     # Extract all text content folowing the lable
        info = " ".join(headerpart_div.split())                                         # Clean up text removing \n \t and whitespace
        data[title] = data.get(title, "") + info

    return data


# Scraping method to retrive information from the fass-text subcategory
# Example page: https://www.fass.se/LIF/product?userType=2&nplId=20190822000136&docType=3&scrollPosition=352
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

        headerpart_div = fass_content[0].find(id=title).find_next('div').get_text()     # Extract all text content folowing the lable
        info = " ".join(headerpart_div.split())                                         # Clean up text removing \n \t and whitespace
        data[title] = data.get(title, "") + info

    return data


# Scraping method for the productresume page subcategory
# Example page: https://www.fass.se/LIF/product?userType=2&nplId=20190822000136&docType=6&scrollPosition=820
def extract_product_resume(soup):
    data = {}
    # Select full div containing the medical text
    fass_content = soup.select('.fass-content')

    # Every section is labled with an a tag defining what information followes
    #   used as index for our data dictionary
    headers = fass_content[0].find_all('h2')


    for section in headers:
        # Some sections do not follow the standard even though they exist
        # as if fass.se uses hand written html. Therefor we still extract
        # the information but cannot differatiate the category
        try:
            title = section.find('a', id=True).get('id')
        except:
            title = 'övrig-information'

        # This page does not group the information in a div
        # therefor we extract all the information between two headings
        html = ""
        for tag in section.next_siblings:
            if tag.name == "h2":
                break
            else:
                html += str(tag.get_text())

        info = " ".join(html.split())           # Clean up text removing \n \t and whitespace 
        data[title] = data.get(title, "") + info
    return data


# Extracts infromation about how the pill can be consumed or split
# Example page: https://www.fass.se/LIF/product?userType=2&nplId=20190822000136&docType=2000&scrollPosition=820
def extract_delbarhet(soup):
    div = soup.select(".tablet-delbarhet-information ")
    if len(div) == 0:
        return {}

    result = " ".join(div[0].get_text().split())    # Text cleanup
    colon_index = result.find(':')                  # Information format "Delbarhetsinformation: ..."
                                                    # this finds the index of the colon

    return {"delbarhets-information": result[colon_index + 2:]} if colon_index > 0 else {}


# Extracts the product id from diffrent packages of the same medecine
# Example page: https://www.fass.se/LIF/product?userType=2&nplId=20190822000136&docType=30&scrollPosition=850
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
