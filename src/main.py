from logic import (
    add_incident,
    view_incidents,
    search_incident,
    update_status,
    delete_incident
)


def main():
    while True:
        print("\n=== Cyber Incident Tracker ===")
        print("1. Add Incident")
        print("2. View All Incidents")
        print("3. Search Incident")
        print("4. Update Status")
        print("5. Delete Incident")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_incident()

        elif choice == "2":
            view_incidents()

        elif choice == "3":
            search_incident()

        elif choice == "4":
            update_status()

        elif choice == "5":
            delete_incident()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()