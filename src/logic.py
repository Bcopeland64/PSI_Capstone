import os
import time
import subprocess

class TriageScanner:
    """
    A class to perform Digital Forensics and Incident Response (DFIR) triage operations.
    It encapsulates the state of the target directory and provides methods to extract system artifacts.
    """
    
    def __init__(self, target_directory):
        # Encapsulated state representing the evidence folder
        self.target_directory = target_directory
        
        # Input validation: Ensure the specified directory actually exists
        if not os.path.isdir(self.target_directory):
            raise FileNotFoundError(f"Error: The directory '{self.target_directory}' does not exist.")

    def get_recent_files(self, window_seconds=600):
        """Scan the target directory for artifacts modified within the specified time window."""
        recent_files = []
        current_time = time.time()
        
        try:
            for filename in os.listdir(self.target_directory):
                path = os.path.join(self.target_directory, filename)
                
                # Ensure we only process files, ignoring subdirectories
                if os.path.isfile(path):
                    mtime = os.stat(path).st_mtime
                    
                    # Check if the file's modified time falls within our suspicious window
                    if current_time - mtime <= window_seconds:
                        recent_files.append({
                            "filename": filename, 
                            "age_seconds": int(current_time - mtime)
                        })
        except PermissionError:
            print(f"[-] Permission denied when attempting to access: {self.target_directory}")
            
        return recent_files

    def get_running_processes(self, sample_limit=5):
        """
        Retrieve a sample of currently active processes. 
        Demonstrates external package integration with a standard library fallback.
        """
        try:
            import psutil  # Third-party library for process management
            return [p.info for p in psutil.process_iter(["pid", "name"])][:sample_limit]
            
        except ImportError:
            # Fallback mechanism if the external module is missing (Error Handling)
            try:
                result = subprocess.run(["ps", "aux"], capture_output=True, text=True, check=True)
                return result.stdout.splitlines()[:sample_limit]
            except Exception as e:
                return [f"Process retrieval failed: {e}"]