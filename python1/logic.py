import pandas as pd
import json

class TriageTool:
    def __init__(self):
        self.df = None

    def load_data(self, file_path):
        try:
            if file_path.endswith('.csv'):
                self.df = pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                self.df = pd.read_json(file_path)
            else:
                print("Error: Unsupported file format. Please use CSV or JSON.")
                return False
            
           
            self.df.columns = self.df.columns.str.strip()
            return True
        except Exception as e:
            print("Error loading file:", e)
            return False

    def filter_severity(self, level):
        if self.df is None:
            print("No data loaded.")
            return None
        
       
        cols_lower = {col.lower(): col for col in self.df.columns}
        if 'severity' not in cols_lower:
            print(f"Error: Column 'severity' not found in data. Found columns: {list(self.df.columns)}")
            return None

        sev_col = cols_lower['severity']
        filtered = self.df[self.df[sev_col].astype(str).str.upper() == level.upper()]
        return filtered

    def export_summary(self, output_name):
        if self.df is None or self.df.empty:
            print("No data available to export.")
            return False

        cols_lower = {col.lower(): col for col in self.df.columns}
        sev_col = cols_lower.get('severity', None)

        summary_data = {
            "total_incidents": len(self.df),
            "severity_counts": self.df[sev_col].value_counts().to_dict() if sev_col else {}
        }

        try:
            with open(output_name, 'w') as f:
                json.dump(summary_data, f, indent=4)
            print("Summary successfully exported to", output_name)
            return True
        except Exception as e:
            print("Failed to save report:", e)
            return False