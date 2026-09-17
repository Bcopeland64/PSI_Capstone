from utils import save_summary_json
from logic import DataPipeline

def main():
    csv_path = "../data/sample_evidence.csv"
    json_path = "../data/summary_report.json"
    img_path = "../data/events_chart.png"

    # 1. Initialize Pipeline 
    pipeline = DataPipeline(csv_path)

    # 2. Load & Clean Data
    if pipeline.load_and_clean_data():
        print("[+] Data loaded and cleaned successfully.")

        # 3. Generate & Save JSON Summary
        stats = pipeline.generate_summary_stats()
        if save_summary_json(stats, json_path):
            print(f"[+] Summary report saved to {json_path}")

        # 4. Generate & Save Visual Chart
        if pipeline.generate_visual_report(img_path):
            print(f"[+] Event chart saved to {img_path}")

if __name__ == "__main__":
    main()