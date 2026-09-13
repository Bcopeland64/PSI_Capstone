"""
logic.py: Core class for managing data processing, analysis, and plotting.
"""
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt


class DataPipeline:
    """
    Class representing the data pipeline (Fetching, Cleaning, Saving, Plotting).
    """

    def __init__(self, api_url: str, output_dir: str = "data"):
        self.api_url = api_url
        self.output_dir = output_dir
        self.df = None
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_data(self) -> bool:
        """
        Fetch data from an external API with error handling.
        """
        try:
            print("⏳ Fetching data from API...")
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            self.df = pd.DataFrame(data)
            print("✅ Successfully fetched data from API!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"⚠️ API connection error: {e}")
            print("🔄 Attempting to load local fallback data...")
            return self.load_local_data()

    def load_local_data(self) -> bool:
        """
        Load local backup data if the API fails.
        """
        fallback_path = os.path.join(self.output_dir, "sample_data.csv")
        try:
            if os.path.exists(fallback_path):
                self.df = pd.read_csv(fallback_path)
                print(f"✅ Backup data loaded from {fallback_path}.")
                return True
            else:
                print("❌ Local backup data file not found.")
                return False
        except Exception as e:
            print(f"❌ Error reading local file: {e}")
            return False

    def clean_and_transform(self):
        """
        Clean and transform data using Pandas.
        """
        if self.df is None or self.df.empty:
            print("⚠️ No data available to clean.")
            return

        self.df = self.df.drop_duplicates()
        self.df = self.df.fillna("N/A")
        print("✅ Data cleaned and duplicates removed successfully.")

    def save_to_csv(self, filename: str = "processed_data.csv"):
        """
        Save processed data to a CSV file inside the data/ folder.
        """
        if self.df is None:
            print("⚠️ No data available to save.")
            return

        file_path = os.path.join(self.output_dir, filename)
        try:
            self.df.to_csv(file_path, index=False)
            print(f"💾 Data saved to: {file_path}")
        except IOError as e:
            print(f"❌ Error writing to file: {e}")

    def generate_report(self):
        """
        Generate a chart and save it as a report image.
        """
        if self.df is None or self.df.empty:
            print("⚠️ Cannot generate chart without data.")
            return

        try:
            fig, ax = plt.subplots(figsize=(8, 4))
            
            if 'userId' in self.df.columns:
                self.df['userId'].value_counts().head(5).plot(kind='bar', ax=ax, color='purple')
                plt.xlabel("User ID")
                plt.ylabel("Count")
            else:
                self.df.iloc[:5, :2].plot(kind='bar', ax=ax)

            plt.title("Summary Data Chart")
            plt.tight_layout()

            report_path = os.path.join(self.output_dir, "summary_plot.png")
            plt.savefig(report_path)
            plt.close()
            print(f"📊 Summary plot generated at: {report_path}")
        except Exception as e:
            print(f"❌ Failed to generate plot: {e}")