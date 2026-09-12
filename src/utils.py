import json
import requests
import os

from rich.console import Console
from rich.panel import Panel

console = Console()

def show_daily_tip():
    try:
        response = requests.get("https://api.adviceslip.com/advice")
        data = response.json()
        advice = data['slip']['advice']
        
        console.print(Panel(
            f"[bold italic cyan]{advice}[/bold italic cyan]", 
            title="Tip of the Day", 
            border_style="green",
            expand=False
        ))
        print() 
    except:
        print("\nWelcome to the Ticket System!\n")

def load_data(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
            
    except FileNotFoundError:
        print("[System] No previous saves found. Starting a fresh database!")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        return []
        
    except Exception as error:
        print(f"[Error] Something went wrong loading data: {error}")
        return []

def save_data(filepath, data_list):
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as file:
            json.dump(data_list, file, indent=4)
    except Exception as error:
        print(f"[Error] Could not save file: {error}")