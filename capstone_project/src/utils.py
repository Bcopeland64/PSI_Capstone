"""
utils.py: Helper functions for validating and safely managing user input.
"""

def validate_user_input(prompt: str, valid_choices: list) -> str:
    """
    Prompts the user for input and ensures it matches an allowed choice.
    """
    while True:
        try:
            user_input = input(prompt).strip().lower()
            if user_input in valid_choices:
                return user_input
            print(f"❌ Invalid choice! Available options are: {', '.join(valid_choices)}")
        except KeyboardInterrupt:
            print("\n⚠️ Operation cancelled by user.")
            raise
        except Exception as e:
            print(f"❌ An unexpected error occurred during input: {e}")