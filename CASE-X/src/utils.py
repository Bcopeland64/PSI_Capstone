from datetime import datetime


def prompt_nonempty(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print("Input cannot be empty.")


def prompt_int(label, minimum=None, maximum=None):
    while True:
        try:
            value = int(input(label).strip())
            if minimum is not None and value < minimum:
                raise ValueError
            if maximum is not None and value > maximum:
                raise ValueError
            return value
        except ValueError:
            bounds = []
            if minimum is not None:
                bounds.append(f">= {minimum}")
            if maximum is not None:
                bounds.append(f"<= {maximum}")
            print(f"Please enter a valid integer ({', '.join(bounds)}).")


def prompt_date(label):
    while True:
        value = input(label).strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Use YYYY-MM-DD.")


def pause():
    input("\nPress Enter to continue...")
