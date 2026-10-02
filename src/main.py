import hashlib
import os
import sys
import time

def compute_file_hash(filepath):
    """Computes and returns the SHA-256 hash of a given file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        print(f"[-] Error: The file '{filepath}' was not found.")
        return None
    except Exception as e:
        print(f"[-] An unexpected error occurred: {e}")
        return None

def check_processes():
    """Return a short list of running process names/pids."""
    try:
        import psutil
        return [p.info for p in psutil.process_iter(["pid", "name"])][:5]
    except ImportError:
        import subprocess
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        return result.stdout.splitlines()[:5]

def check_recent_files(folder, window_seconds=600):
    """Return files in `folder` modified within the last `window_seconds`."""
    current_time = time.time()
    recent = []
    try:
        for name in os.listdir(folder):
            path = os.path.join(folder, name)
            if os.path.isfile(path):
                mtime = os.stat(path).st_mtime
                if current_time - mtime <= window_seconds:
                    recent.append((name, int(current_time - mtime)))
    except FileNotFoundError:
        pass
    return recent

def run_triage(folder="sample_evidence"):
    """Combine system and file checks into a comprehensive report."""
    print(f"--- Triage Report for Target: '{folder}' ---")

    print("\n[+] Running Processes (Sample):")
    for p in check_processes():
        print("   ", p)

    print("\n[+] Recently Modified Files:")
    recent = check_recent_files(folder)
    if recent:
        for name, age in recent:
            print(f"    - {name} (Modified {age}s ago)")
    else:
        print("    - None found within window.")

    print("\n[+] File Hashes (SHA-256):")
    if os.path.isdir(folder):
        for name in os.listdir(folder):
            path = os.path.join(folder, name)
            if os.path.isfile(path):
                digest = compute_file_hash(path)
                if digest:
                    print(f"    - {name}: {digest[:12]}...")
    else:
        print(f"[-] Directory '{folder}' does not exist.")

def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "sample_evidence"
    if not os.path.isdir(folder):
        print(f"[-] Error: '{folder}' is not a valid directory.'")
        sys.exit(1)
    run_triage(folder)

if __name__ == "__main__":
    main()
