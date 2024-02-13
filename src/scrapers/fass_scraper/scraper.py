# Scarping method for extracting the bipacksedel subcategory on fass.se
# Example page: https://www.fass.se/LIF/product?userType=2&nplId=20190822000136&docType=7&scrollPosition=352
def extract_medical_text(soup):
    data = {}
    
    fass_content = soup.select('.fass-content')[0]
    # Every section is labled with an <h2> tag defining what information followes
    #   used as index for our data dictionary
    headers = fass_content.find_all("h2", recursive=True)

    for section in headers:
        try:
            title = section.find('a', id=True).get('id')
        except:
            continue

        # Collect all html between two <a> tags
        html = ""
        for tag in section.next_siblings:
            if tag.name == 'h2':
                break
            else:
                html += str(tag.get_text())

        # Merge and clean data
        # Clean up text removing \n \t and whitespace
        info = " ".join(html.split())
        data[title] = data.get(title, "") + info

    return data

# Scarping method for extracting the bipacksedel subcategory on fass.se
# Example page: https://www.fass.se/LIF/product?userType=2&nplId=20190822000136&docType=7&scrollPosition=352
def extract_product_leaflet(soup):
    data = {}
    fass_content = soup.select('.fass-content')[0]
    # Every section is labled with an a tag defining what information followes
    #   used as index for our data dictionary
    headers = fass_content.find_all('a', recursive=True, id=True)

    for section in headers:
        try:
            title = section.get('id')
        except:
            continue

        # Collect all html between two <a> tags
        html = ""
        for tag in section.next_siblings:
            if tag.name == 'a':
                break
            else:
                html += str(tag.get_text())

        # Merge and clean data
        # Clean up text removing \n \t and whitespace
        info = " ".join(html.split())
        data[title] = data.get(title, "") + info

    return data


# Extracts infromation about how the pill can be consumed or split
# Example page: https://www.fass.se/LIF/product?userType=2&nplId=20190822000136&docType=2000&scrollPosition=820
def extract_delbarhet(soup):
    div = soup.select(".tablet-delbarhet-information ")
    if len(div) == 0:
        return {}

    result = " ".join(div[0].get_text().split())    # Text cleanup
    # Information format "Delbarhetsinformation: ..."
    colon_index = result.find(':')
    # this finds the index of the colon

    return {"delbarhets-information": result[colon_index + 2:]} if colon_index > 0 else {}
