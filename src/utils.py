import os
import json

def check_file_exists(filepath: str) -> bool:
    return os.path.exists(filepath) and os.path.isfile(filepath)

def save_summary_json(data: dict, output_path: str) -> bool:
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        
        print(f"[-] Error saving JSON report: {e}")
        return False