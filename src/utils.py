import hashlib
import os
import json

def generate_sha256(file_path):
    """
    Calculate and return the SHA-256 cryptographic hash of a file.
    Includes error handling for missing files or permission issues.
    """
    if not os.path.isfile(file_path):
        return "Error: File not found."
        
    try:
        # Open file in binary mode for hashing
        with open(file_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        return file_hash
    except PermissionError:
        return "Error: Permission denied."
    except Exception as e:
        return f"Error: {e}"

def export_to_json(data, output_path):
    """
    Persist the provided dictionary data to a JSON file.
    Satisfies the 'Data Persistence' capstone requirement.
    """
    try:
        # Save the data in a human-readable JSON format
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"[+] Report successfully exported to: {output_path}")
        return True
    except Exception as e:
        print(f"[-] Failed to export report: {e}")
        return False