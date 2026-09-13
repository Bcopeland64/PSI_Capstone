import csv  
import os 


def validate_url(url):
    """Check that url is a text string starting with http:// or https://."""
    if not isinstance(url, str):
        return False
    if url.startswith("http://") or url.startswith("https://"):
        return True
    return False


def save_to_csv(data, file_path="data/books_data.csv"):
    """Write the scraped data (a list of dicts) to a CSV file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  
        with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:  
            fieldnames = ["Title", "Price"]  
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)  
            writer.writeheader() 
            for row in data:  
                writer.writerow(row)
        print(f"Successfully saved data to {file_path}")
    except IOError as e:  
        print(f"File writing error: {e}")


def read_from_csv(file_path="data/books_data.csv"):
    """Read book data back from a CSV file and return it as a list of dicts."""
    data = []
    try:
        with open(file_path, mode="r", newline="", encoding="utf-8") as csv_file:  
            reader = csv.DictReader(csv_file)  
            for row in reader:  
                data.append(row)
    except FileNotFoundError:
        print(f"Error: file not found at {file_path}")
    return data