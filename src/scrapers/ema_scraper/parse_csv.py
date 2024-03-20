import csv

# Path to your CSV file
EMA_FILE = 'ema_data.csv'

def get_valid_drug_links():
    
    result = []
    
    # Open the CSV file and read it
    with open(EMA_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        
        # Iterate over each row in the CSV
        for row in reader:
            # Check if valid drug
            if row[0] == "Human" and row[7] == "Authorised":
                result.append(row[-1])
                
    return result

