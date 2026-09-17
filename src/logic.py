import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class QuoteItem:
    """Class representing a single scraped quote object (OOP)."""
    def __init__(self, text, author):
        self.text = text
        self.author = author

    def to_dict(self):
        return {"Text": self.text, "Author": self.author}

class WebScraperEngine:
    """Main business logic for scraping and data processing."""
    BASE_URL = "https://quotes.toscrape.com/page/{}/"

    def __init__(self, max_pages):
        self.max_pages = max_pages
        self.collected_quotes = []

    def scrape_data(self):
        """Connects to the website and extracts items with error handling."""
        print(f"\n[Status] Starting scrape for up to {self.max_pages} pages...")
        
        for page in range(1, self.max_pages + 1):
            url = self.BASE_URL.format(page)
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 404:
                    print(f"[Info] Page {page} not found. Stopping.")
                    break
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                quote_elements = soup.find_all('div', class_='quote')
                
                if not quote_elements:
                    print(f"[Info] No more items found on page {page}.")
                    break
                    
                for elem in quote_elements:
                    text = elem.find('span', class_='text').text.strip()
                    author = elem.find('small', class_='author').text.strip()
                    self.collected_quotes.append(QuoteItem(text, author))
                
                print(f"[Success] Scraped page {page}")
                time.sleep(1)  # Polite scraping gap
                
            except requests.exceptions.RequestException as e:
                print(f"[Error] Failed to connect to page {page}: {e}")
                break

    def save_and_analyze(self, output_filepath):
        """Uses Pandas to save data and show brief analytics summary."""
        if not self.collected_quotes:
            print("[Warning] No data collected to process.")
            return

        # Transform to Dictionary List for Pandas
        data_list = [q.to_dict() for q in self.collected_quotes]
        df = pd.DataFrame(data_list)
        
        # Save to CSV (Data Persistence)
        df.to_csv(output_filepath, index=False, encoding='utf-8')
        print(f"\n[Success] Data saved successfully to: {output_filepath}")
        
        # Perform minor Data Analysis with Pandas
        print("\n=== Data Analytics Report ===")
        print(f"Total Items Collected: {len(df)}")
        print(f"Unique Authors Found: {df['Author'].nunique()}")
        print("\nTop Authors by Count:")
        print(df['Author'].value_counts().head(3))
        print("=============================")
