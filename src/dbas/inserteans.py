import json
import os
import psycopg2

JSON_FILE = 'ean.json'

# Load environment variables
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_pass = os.getenv('POSTGRES_PASSWORD')
db_host = 'db'  # Docker Compose service name for the DB

# Insert data into database
def insert_into_database():
    # Connection to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=db_name, 
        user=db_user, 
        password=db_pass, 
        host=db_host
    )

    # Establish cursor
    cursor = conn.cursor()

    try:
        # Open JSON file
        f = open(JSON_FILE)

        # Load data from JSON file
        data = json.load(f)

        # Loop through all EAN-codes in JSON file
        for ean in data:
            nplID = data[ean]
            
            # Insert EAN-codes and nplIDs
            query = "INSERT INTO eans (ean, nplID) VALUES (%s, %s) ON CONFLICT (ean) DO NOTHING"                  # TODO ändra så att det är rätt table med rätt attribut
            cursor.execute(query, (ean, nplID))

        conn.commit()
    except psycopg2.Error as e:
        # Handle errors
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        # Close connection
        cursor.close()
        conn.close()
        f.close()



if __name__ == '__main__':
    insert_into_database()
