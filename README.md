# TECHIN510-Lab4: Book Explorer App

The Book Explorer is a web application built with Streamlit, designed to query and display books stored in a PostgreSQL database. Users can search for books by name or description and can sort results by rating or price. This application is ideal for quickly accessing detailed information about books, including titles, descriptions, and purchasing details.

## Features

- **Search Functionality**: Allows users to search for books by title or description.
- **Sorting Options**: Users can sort books by rating (numerically adjusted from textual representations) or price.
- **Responsive UI**: Uses Streamlit's native components for a clean and responsive user interface.
- **Expandable Descriptions**: Each book's details can be expanded in place to save space and improve navigation.

## Installation

### Prerequisites

Before you begin, ensure you have the following installed:
- Python (3.6 and above)
- pip (Python package installer)


## User Guide
- Search: Enter a keyword into the search bar to find books by title or description.
- Sort: Select your sorting preference from the dropdown menus for both the sort category (rating or price) and the sort order (ascending or descending).
- View Details: Click on the expander next to each book title to view detailed information about the book, such as the description and purchase URL.

### Web screapper

The web scraper is built using Python and makes use of the requests and BeautifulSoup libraries to extract book information from the target website. It navigates through pages, extracts details such as title, description, rating, and pricing, and prepares this data for storage.

### Storage

Data scraped from the web is stored in a PostgreSQL database. The database schema is designed to accommodate various book attributes including ratings, prices, and descriptions. This section ensures data integrity and provides a robust query interface.

Ensure your PostgreSQL database is set up with the required books table. Use the following SQL command to create the table if it does not exist:

```sql
CREATE TABLE books (
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
);
```

### App

The application layer is built using Streamlit, providing a user-friendly interface to interact with the data. It supports searching, filtering, and sorting functionalities, which enhance the user experience by making information retrieval straightforward and efficient.