"""
main.py: Main entry point for running the application.
"""
from logic import DataPipeline
from utils import validate_user_input

def main():
    print("=" * 45)
    print("🚀 Welcome to Python Capstone Pipeline")
    print("=" * 45)

    API_URL = "https://jsonplaceholder.typicode.com/posts"
    pipeline = DataPipeline(api_url=API_URL)

    choice = validate_user_input(
        prompt="Do you want to run the data pipeline? (yes/no): ",
        valid_choices=["yes", "no", "y", "n"]
    )

    if choice in ["yes", "y"]:
        if pipeline.fetch_data():
            pipeline.clean_and_transform()
            pipeline.save_to_csv()
            pipeline.generate_report()
            print("\n🎉 Pipeline executed successfully!")
    else:
        print("👋 Application exited by user.")

if __name__ == "__main__":
    main()