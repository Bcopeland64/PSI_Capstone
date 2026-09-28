import requests

from tasks import tasks, add_task, complete_task, delete_task
from data import save_tasks, load_tasks


def show_menu():
    print("\n===== Cyber Study Planner =====")
    print("1. Add study task")
    print("2. View study tasks")
    print("3. Complete a task")
    print("4. Delete a task")
    print("5. Get study tip")
    print("6. Exit")


def display_tasks():
    if not tasks:
        print("No study tasks yet.")
        return

    print("\nYour study tasks:")

    for number, task in enumerate(tasks, start=1):
        status = "Completed" if task["completed"] else "Not completed"
        print(f"{number}. {task['title']} - {status}")


def get_task_number():
    try:
        number = int(input("Enter task number: "))
        return number

    except ValueError:
        print("Please enter a valid number.")
        return None


def get_study_tip():
    try:
        response = requests.get(
            "https://dummyjson.com/quotes/random",
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        print("\nStudy Tip:")
        print(data["quote"])

    except requests.RequestException:
        print("Could not connect to the study tips service.")


def main():
    loaded_tasks = load_tasks()
    tasks.extend(loaded_tasks)

    while True:
        show_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            task = input("Enter a study task: ").strip()

            if task:
                add_task(task)
                save_tasks(tasks)
                print("Task added successfully!")
            else:
                print("Task cannot be empty.")

        elif choice == "2":
            display_tasks()

        elif choice == "3":
            display_tasks()

            if tasks:
                number = get_task_number()

                if number is not None:
                    if complete_task(number):
                        save_tasks(tasks)
                        print("Task completed successfully!")
                    else:
                        print("Invalid task number.")

        elif choice == "4":
            display_tasks()

            if tasks:
                number = get_task_number()

                if number is not None:
                    if delete_task(number):
                        save_tasks(tasks)
                        print("Task deleted successfully!")
                    else:
                        print("Invalid task number.")

        elif choice == "5":
            get_study_tip()

        elif choice == "6":
            save_tasks(tasks)
            print("Goodbye! Good luck with your studies.")
            break

        else:
            print("Invalid choice. Please choose 1, 2, 3, 4, 5, or 6.")


if __name__ == "__main__":
    main()