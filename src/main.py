from logic import scrape_books, get_book_count, get_first_books
from utils import save_to_csv, read_from_csv, validate_url


def main():
    """Run the book scraper end to end: get a URL, scrape it, save it, and show a summary."""
    print("=== Starting Book Scraper Tool ===")

    target_url = input("Enter the URL to scrape (press Enter for default): ").strip()
    if not target_url:  
        target_url = "http://books.toscrape.com/"

    if not validate_url(target_url):  
        print("Invalid URL entered. Please enter a valid URL starting with http:// or https://")
        return

    print(f"Fetching data from: {target_url}")
    scraped_data = scrape_books(target_url)

    if not scraped_data:  
        print("No data was collected due to an error.")
        print("=== Process Finished ===")
        return

    print(f"Successfully scraped {len(scraped_data)} books.")
    save_to_csv(scraped_data)

    print("\n--- Summary Insights ---")
    total_books = get_book_count(scraped_data)
    print(f"Total number of books scraped: {total_books}")

    first_books = get_first_books(scraped_data, n=3)
    for i, book in enumerate(first_books, 1):
        print(f"{i}. {book['Title']} - {book['Price']}")

    print("\n--- Verifying saved data by reading it back ---")
    saved_data = read_from_csv()
    print(f"Rows found in CSV: {len(saved_data)}")

    print("=== Process Finished ===")


if __name__ == "__main__":
    main()