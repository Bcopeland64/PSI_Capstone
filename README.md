# Capstone Project: Book Library App

Hi, this is my final capstone project. It is a command-line app that lets you search for a book on the internet and save it to a local file on your computer.

## What it does
* Uses Object-Oriented Programming (Classes)
* Saves data to a CSV file so it doesn't get lost
* Connects to the Google Books API
* Has try-except blocks so it doesn't crash if the internet goes down

## How to use it
1. Run `pip install -r requirements.txt` to get the requests library.
2. You need a Google Books API key to avoid rate limits. Rename '.env.example' to '.env' and paster your key inside
3. Run `python -m src.main` to start the program!
