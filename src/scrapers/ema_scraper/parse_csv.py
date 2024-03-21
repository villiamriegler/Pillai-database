import csv

# Path to CSV file with all EMA drugs
EMA_FILE = 'ema_data.csv'
STATUS_INDEX = 7
PATIENT_TYPE_INDEX = 0
DRUG_LINK_INDEX = -1

def get_valid_drug_links():
    """
    Get al list of all valid links to approved human drug pages on EMA

    Returns:
        string array: all valid links
    """

    # List of all valid links
    result = []
    
    # Open the CSV file and read it
    with open(EMA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        
        # Iterate over each row in the CSV
        for row in reader:
            # Check if valid drug
            if row[PATIENT_TYPE_INDEX] == "Human" and row[STATUS_INDEX] == "Authorised":
                # Add the link to the list
                result.append(row[DRUG_LINK_INDEX])
                
    return result

