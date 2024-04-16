import psycopg2
import csv
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to our database
conn = psycopg2.connect(user=os.getenv("USERNAME"), password=os.getenv("PASSWORD"), host=os.getenv("HOSTNAME"), port=5432, database="postgres")
cur = conn.cursor()

# Create a table with appropriate columns
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        price TEXT,
        rating TEXT,
        url TEXT,
        description TEXT,
        upc TEXT,
        product_type TEXT,
        price_excl_tax TEXT,
        price_incl_tax TEXT,
        tax TEXT,
        availability TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
)
conn.commit()

# Read data from CSV and insert into the database
try:
    with open('results.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        insert_sql = """
        INSERT INTO books (title, price, rating, url, description, upc, product_type, price_excl_tax, price_incl_tax, tax, availability)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        for row in reader:
            cur.execute(insert_sql, (
                row['title'],
                row['price'],
                row['rating'],
                row['url'],
                row['description'],
                row['UPC'],
                row['Product Type'],
                row['Price (excl. tax)'],
                row['Price (incl. tax)'],
                row['Tax'],
                row['Availability']
            ))
        conn.commit()
        print("Books inserted successfully.")
except Exception as e:
    print("Error during inserting the data:", e)
    conn.rollback()
finally:
    cur.close()
    conn.close()

print("SUCCESS: Inserted book data into database.")
