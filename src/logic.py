import requests  
from bs4 import BeautifulSoup  #library for parsing HTML


def scrape_books(url="http://books.toscrape.com/"):
    """Scrape book titles and prices from a books.toscrape.com style page."""
    books_list = []

    try:
        response = requests.get(url, timeout=10)  
        response.encoding = "utf-8"  

        if response.status_code != 200:  
            print(f"Error: server returned status code {response.status_code}")
            return books_list

        soup = BeautifulSoup(response.text, "html.parser")  
        books = soup.find_all("article", class_="product_pod") 

        for book in books:  
            title = book.h3.a["title"] 
            price = book.find("p", class_="price_color").text 
            books_list.append({"Title": title, "Price": price})  

    except Exception as e:  
        print(f"An error occurred while scraping: {e}") 

    return books_list


def get_book_count(data):
    """Return how many books are in the scraped data."""
    return len(data)


def get_first_books(data, n=3):
    """Return the first n books from the scraped data (default: 3)."""
    return data[:n]