import json
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()  # Load .env file

# Database connection parameters
db_params = {
    "dbname": "postgres",
    "user": "root",
    "password": os.getenv("GC_PASSWORD"),
    "host": "35.225.231.83",
    "port": "5432"  
}

LEAFLETS_DIR = "../../scrapers/data/products"

# Function to insert data into the FASS table
def insert_data(npl, data):
    # Create a connection to the database
    print("Connecting...")
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    
    print("Connected!")
    # Prepare the INSERT statement
    insert_statement = """
    INSERT INTO FASS (npl, preclinicalInfo, dosage, pregnancy, pharmacodynamic, composition, caution, sideEffects, pharmacokinetic, fertility, incompatibility, driving, contraindication, indication, breastfeeding, interaction, envEffect, overdosage, handlingLifeShelfStorage, propertiesMedicine)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    print("Extracting data...")
    # Get all data from JSON
    values = (
        npl,
        data.get("preclinical-info"),
        data.get("dosage"),
        data.get("pregnancy"),
        data.get("pharmacodynamic"),
        data.get("composition"),
        data.get("caution"),
        data.get("side-effects"),
        data.get("pharmacokinetic"),
        data.get("fertility"),
        data.get("incompatibility"),
        data.get("driving"),
        data.get("contraindication"),
        data.get("indication"),
        data.get("breastfeeding"),
        data.get("interaction"),
        data.get("env-effect"),
        data.get("overdosage"),
        data.get("handling-life-shelf-storage"),
        data.get("properties-medicine")
    )
    
    # Execute and commit the insert
    cur.execute(insert_statement, values)
    conn.commit()
    
    print("Inserted data into table")
    
    # Close the connection
    cur.close()
    conn.close()

# Main script to load and insert data from JSON files
def main():
    # Get NPL-ids
    with open('top.txt', 'r') as file:
        npl_ids = file.read().splitlines()
    
    # Go through each file and add data to Google Cloud 
    for npl_id in npl_ids:
        print(f"Handling: {npl_id}")
        json_path = os.path.join(LEAFLETS_DIR, f"{npl_id}.json")
        with open(json_path, 'r') as json_file:
            # Load all data
            data = json.load(json_file)
            
            # Only extract FASS text for example
            fass_text = data.get("fass_text", {})
            
            # Insert the data into Google Cloud
            insert_data(npl_id, fass_text)

if __name__ == "__main__":
    main()
