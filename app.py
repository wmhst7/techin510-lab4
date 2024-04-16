import streamlit as st
import psycopg2
import pandas as pd

# Function to connect to the database
def connect_to_db():
    conn = psycopg2.connect(
        host="techin510wmh.postgres.database.azure.com",
        dbname="postgres",
        user="mhwu",
        password="Wmh311@pos",
        port=5432
    )
    return conn

# Function to fetch books based on user input
def fetch_books(search_query, sort_by, sort_order):
    conn = connect_to_db()
    if sort_by == "rating":
        # If sorting by rating, convert text ratings to numbers
        sort_clause = f"CASE rating WHEN 'One' THEN 1 WHEN 'Two' THEN 2 WHEN 'Three' THEN 3 WHEN 'Four' THEN 4 WHEN 'Five' THEN 5 END {sort_order}"
    else:
        sort_clause = f"{sort_by} {sort_order}"
    
    query = f"""
    SELECT * FROM books
    WHERE title ILIKE %s OR description ILIKE %s
    ORDER BY {sort_clause}
    """
    df = pd.read_sql(query, conn, params=[f'%{search_query}%', f'%{search_query}%'])
    conn.close()
    return df

# Streamlit user interface
def main():
    st.title('Book Explorer')
    search_query = st.text_input('Search by book name or description')
    sort_by = st.selectbox('Sort by', ['rating', 'price'])
    sort_order = st.selectbox('Sort order', ['ASC', 'DESC'])

    if st.button('Search'):
        results = fetch_books(search_query, sort_by, sort_order)
        if results.empty:
            st.write("No results found.")
        else:
            st.dataframe(results)

if __name__ == "__main__":
    main()
