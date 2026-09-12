import os

def validate_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            print("Please enter a number greater than or equal to 0.")
        except ValueError:
            print("Invalid input. Please enter a valid whole number.")

def validate_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
            print("Please enter a number greater than or equal to 0.")
        except ValueError:
            print("Invalid input. Please enter a valid decimal number.")

def ensure_data_folder(file_path):
    folder = os.path.dirname(file_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
