import os

def validate_positive_integer(prompt):
    """Validates that the user input is a positive integer."""
    while True:
        try:
            val = int(input(prompt))
            if val > 0:
                return val
            print("[Error] Please enter a number greater than 0.")
        except ValueError:
            print("[Error] Invalid input. Please enter a valid whole number.")

def ensure_directory_exists(path):
    """Creates directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)
