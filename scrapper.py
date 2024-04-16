import requests
from bs4 import BeautifulSoup
import csv

def scrape_book_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    details = {}

    product_information = soup.find('table', class_='table table-striped')
    if product_information:
        for row in product_information.find_all('tr'):
            header = row.th.text.strip()
            value = row.td.text.strip()
            details[header] = value

    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'].strip() if description_tag else 'No description available'
    details['description'] = description

    availability = soup.find('p', class_='instock availability')
    details['Availability'] = availability.text.strip() if availability else 'Not available'
    
    return details

def scrape_books(base_url):
    page_number = 1
    books = []
    while True:
        url = f"{base_url}page-{page_number}.html"
        response = requests.get(url)
        if response.status_code != 200:
            break  # Break the loop if the page does not exist

        print(f"Scraping page {page_number}...")

        soup = BeautifulSoup(response.text, 'html.parser')
        for book in soup.find_all('article', class_='product_pod'):
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text
            rating = book.find('p', class_='star-rating')['class'][1]
            href = book.h3.a['href']
            full_url = requests.compat.urljoin(url, href)
            
            book_details = scrape_book_details(full_url)
            book_details.update({
                'title': title,
                'price': price,
                'rating': rating,
                'url': full_url
            })
            books.append(book_details)
            # print(f"Scraped {title} ({rating})")
        
        page_number += 1  # Increment the page number for the next loop iteration

    return books

def save_to_csv(books, filename):
    keys = books[0].keys() if books else []
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(books)

# Example usage
base_url = 'http://books.toscrape.com/catalogue/'
all_books = scrape_books(base_url)
save_to_csv(all_books, 'results.csv')
print(f"Scraped {len(all_books)} books and saved to 'results.csv'.")
