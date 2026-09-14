import os


def check_file_exists(filename):
    if os.path.exists(filename):
        return True
    else:
        return False


def clean_input(text):
    return text.strip()