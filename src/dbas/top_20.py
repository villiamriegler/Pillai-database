import os
import json
from translate import translate_json

DATA_PATH = '../scrapers/data/products'
TOP_19_NAMES = [
    "Alvedon", "Panodil", "Ipren", "Claritine",
    "Zyrtec", "Sudafed", "Bisolvon", "Imodium",
    "Laxoberal", "Losec", "Nexium", "Nicorette", 
    "Nicotinell", "Voltaren", "Canesten", "Daktarin",
    "Bisolvon", "Strepsils", "Läkerol"
]

def matches_top_20(name):
    return any(top_string in name for top_string in TOP_19_NAMES)

def check_file(filename):
    file_path = os.path.join(DATA_PATH, filename)
    # Open and load the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            # Check if 'product_name' key exists and matches the criteria
            if 'product_name' in data and 'product_name' in data['product_name']:
                product_name = data['product_name']['product_name']
                
                # Translate text
                translated_data = translate_json(data)
                
                return matches_top_20(product_name)
                    
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file '{filename}'")

def main():
    matches = []
    
    # Go through all files
    for filename in os.listdir(DATA_PATH):
        # Only process JSON-files
        if filename.endswith('.json'):  
            if check_file(filename):
                matches.append(filename)
                print(f"File '{filename}' contains a product name matching the top 20 list.")
                    
    print(len(matches))
                    
if __name__ == '__main__':
    main()