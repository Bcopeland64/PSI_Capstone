"""
This file has some helper functions for my project to validate input and call the API.
"""
import os

from dotenv import load_dotenv

import requests

current_folder = os.path.dirname(os.path.abspath(__file__))
parent_folder = os.path.dirname(current_folder)
env_path = os.path.join(parent_folder, '.env')

load_dotenv(dotenv_path=env_path)

def get_user_input_safely(question, valid_options):
    """
    This asks the user a question and loops until they give a good answer.
    """
    while True:
        answer = input(question)
        answer = answer.strip() # take away extra spaces
        
        # If the valid_options list is empty, just accept anything they typed
        if valid_options == []:
            if len(answer) > 0:
                return answer
            else:
                print("Error: You can't leave this blank!")
        # If we have specific options, check if their answer is in the list
        elif answer in valid_options:
            return answer
        else:
            print("Sorry, that is not a valid input. Please try again.")

def get_data_from_google_api(search_query):
    """
    This function connects to the Google Books API and returns the JSON data.
    """
    api_url = "https://www.googleapis.com/books/v1/volumes"
    # Set up the parameters dictionary for the web request
    api_params = {
        "q": search_query, 
        "maxResults": "1"
    }
    
    # Securely get the API key from the environment
    my_api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    if my_api_key:
        api_params["key"] = my_api_key
        
    try:
        # Make the request to the API and wait up to 10 seconds
        response = requests.get(api_url, params=api_params, timeout=10)
        response.raise_for_status() # Check if we got a bad status code
        return response.json()
    except requests.exceptions.Timeout:
        print("Error: The internet connection timed out.")
    except requests.exceptions.HTTPError as error:
        print(f"Error: There was an HTTP error! {error}")
    except Exception as e:
        # Catch-all for any other weird errors
        print(f"Error: Something went wrong with the API: {e}")
    
    return None