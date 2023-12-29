import psycopg2

# Connect to database
conn = psycopg2.connect("dbname=mydatabase user=myuser password=mypassword host=localhost")
cur = conn.cursor()

# Query the database
cur.execute("SELECT * FROM products")
records = cur.fetchall()
print(records)

# Insert a new record
cur.execute("INSERT INTO products (name) VALUES (%s)", ('New product',))
conn.commit()

# Query again to see the inserted data
cur.execute("SELECT * FROM products")
new_records = cur.fetchall()
print(new_records)

# Terminate
cur.close()
conn.close()
