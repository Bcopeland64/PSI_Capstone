import sys
import os

# Adjust path to allow smooth module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic import WebScraperEngine
from utils import validate_positive_integer, ensure_directory_exists

def main():
    print("=========================================")
    print("   Welcome to Web Scraper Capstone Tool  ")
    print("=========================================")
    
    # 1. Input Validation using utils module
    pages_to_scrape = validate_positive_integer("Enter number of pages to scrape: ")
    
    # 2. Ensure directories exist
    output_dir = "data"
    ensure_directory_exists(output_dir)
    output_file = os.path.join(output_dir, "scraped_quotes.csv")
    
    # 3. Instantiate OOP engine & Run logic
    engine = WebScraperEngine(max_pages=pages_to_scrape)
    engine.scrape_data()
    engine.save_and_analyze(output_file)
    
    print("\nThank you for using the application! Goodbye.")

if __name__ == "__main__":
    main()
