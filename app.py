import streamlit as st
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


# Connect to our database
conn = psycopg2.connect(user=os.getenv("USERNAME"), password=os.getenv("PASSWORD"), host=os.getenv("HOSTNAME"), port=5432, database="postgres")
cur = conn.cursor()


# Function to fetch books based on user input
def fetch_books(search_query, sort_by, sort_order):
    if sort_by == "rating":
        sort_clause = f"CASE rating WHEN 'One' THEN 1 WHEN 'Two' THEN 2 WHEN 'Three' THEN 3 WHEN 'Four' THEN 4 WHEN 'Five' THEN 5 END {sort_order}"
    else:
        sort_clause = f"{sort_by} {sort_order}"

    query = f"""
    SELECT id, title, price, rating, url, description, availability
    FROM books
    WHERE title ILIKE %s OR description ILIKE %s
    ORDER BY {sort_clause}
    """
    df = pd.read_sql(query, conn, params=[f'%{search_query}%', f'%{search_query}%'])
    conn.close()
    return df

# Streamlit user interface with enhanced book display
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
            for index, row in results.iterrows():
                with st.expander(f"**{row['title']}** | Rating: ({row['rating']}) | Price: {row['price']}"):
                    st.markdown(f"**URL:** [Link]({row['url']})")
                    st.markdown(f"**ID:** {row['id']}")
                    st.markdown(f"**Avaliable** {row['availability']}")
                    st.markdown(f"**Description:** {row['description']}")

if __name__ == "__main__":
    main()
