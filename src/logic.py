import os
import pandas as pd
import matplotlib.pyplot as plt
from utils import check_file_exists  

class DataPipeline:

    def __init__(self, csv_filepath: str):
        self.csv_filepath = csv_filepath
        self.df = None

    def load_and_clean_data(self) -> bool:
        """Load CSV data into Pandas DataFrame and handle missing values."""
        if not check_file_exists(self.csv_filepath):
            print(f"[-] File not found: {self.csv_filepath}")
            return False

        try:
            self.df = pd.read_csv(self.csv_filepath)
            self.df.dropna(inplace=True)
            if 'path' in self.df.columns:
                self.df['path'] = self.df['path'].str.strip()
            return True
        except Exception as e:
            print(f"[-] Error loading data: {e}")
            return False

    def generate_summary_stats(self) -> dict:
        """Analyze data using Pandas and return key summary statistics."""
        if self.df is None or self.df.empty:
            return {}

        total_records = len(self.df)
        event_counts = self.df['event_type'].value_counts().to_dict() if 'event_type' in self.df.columns else {}
        top_paths = self.df['path'].value_counts().head(3).to_dict() if 'path' in self.df.columns else {}

        return {
            "total_records": total_records,
            "event_distribution": event_counts,
            "top_frequent_paths": top_paths
        }

    def generate_visual_report(self, output_img_path: str) -> bool:
        """Generate and save a bar chart visualization of events."""
        if self.df is None or 'event_type' not in self.df.columns:
            return False

        try:
            plt.figure(figsize=(8, 4))
            self.df['event_type'].value_counts().plot(kind='bar', color='skyblue', edgecolor='black')
            plt.title("Event Types Analytics Summary")
            plt.xlabel("Event Type")
            plt.ylabel("Count")
            plt.tight_layout()

            os.makedirs(os.path.dirname(output_img_path), exist_ok=True)
            plt.savefig(output_img_path)
            plt.close()
            return True
        except Exception as e:
            print(f"[-] Error generating plot: {e}")
            return False
        