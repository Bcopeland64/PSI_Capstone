from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import show_daily_tip, load_data, save_data
from src.logic import Ticket

FILENAME = "data/tickets.json"

def main():
    show_daily_tip()
    
    raw_data = load_data(FILENAME)
    
    tickets = []
    for item in raw_data:
        ticket_obj = Ticket(item["id"], item["title"], item["creation_date"], item["last_update_date"],item["description"] ,item["status"])
        tickets.append(ticket_obj)

    while True:
        print("-" * 20)
        print("1. View All Tickets")
        print("2. Add a New Ticket")
        print("3. Close a Ticket")
        print("4. Show a Ticket using ID")
        print("5. Show a Ticket using status")
        print("6. Save and Exit")
        print("-" * 20)
        
        choice = input("Choose an option (1-6): ")
        
        if choice == "1":
            print("\n--- ALL TICKETS ---")
            if len(tickets) == 0:
                print("No tickets in the system.")
            else:
                for t in tickets:
                    print(f"ID: {t.ticket_id} | Title: {t.title}| Description:{t.description} | Status: {t.status} | creation_date: {t.creation_date} | last_update_date: {t.last_update_date}")
            print()
            
        elif choice == "2":
            title = input("Enter what needs to be fixed: ")
            
            if title.strip() == "":
                print("Error: Ticket title cannot be empty!\n")
                continue
            desc = input("Descripe the issue (optional): ")
    
            new_id = len(tickets) + 1
            new_ticket = Ticket(new_id, title,datetime.now().strftime("%Y-%m-%d %H:%M:%S"),datetime.now().strftime("%Y-%m-%d %H:%M:%S"),desc)
            tickets.append(new_ticket)
            print(f"Success! Ticket '{title}' added.\n")
            
        elif choice == "3":
            try:
                target_id = int(input("Enter Ticket ID to close: "))
                found = False
                
                for t in tickets:
                    if t.ticket_id == target_id:
                        t.status = "Closed"
                        t.last_update_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        found = True
                        print(f"Success! Ticket {target_id} is now Closed.\n")
                        break
                        
                if not found:
                    print("Error: Ticket ID not found.\n")
                    
            except ValueError:
                print("Error: Please type a valid number!\n")
        elif choice == "4":
                    try:
                        target_id = int(input("Enter Ticket ID to Show: "))
                        found = False
                        
                        for t in tickets:
                            if t.ticket_id == target_id:
                                print(f"ID: {t.ticket_id} | Title: {t.title}| Description:{t.description} | Status: {t.status} | creation_date: {t.creation_date} | last_update_date: {t.last_update_date}")
                                found = True
                                break
                                
                        if not found:
                            print("Error: Ticket ID not found.\n")
                            
                    except ValueError:
                        print("Error: Please type a valid number!\n")  
        elif choice == "5":
            try:
                print("*" * 10)
                print("1 to get all open tickets")
                print("2 to get all closed tickets")
                print("*" * 10)
                target_Status = int(input("Enter Ticket Status to Show: "))
                if target_Status in (1,2):
                    for t in tickets:  
                        if t.status=="Open" and target_Status==1:
                            print(f"ID: {t.ticket_id} | Title: {t.title}| Description:{t.description} | Status: {t.status} | creation_date: {t.creation_date} | last_update_date: {t.last_update_date}")
                            print()  
                        elif t.status=="Closed" and target_Status==2:
                            print(f"ID: {t.ticket_id} | Title: {t.title}| Description:{t.description} | Status: {t.status} | creation_date: {t.creation_date} | last_update_date: {t.last_update_date}")
                            print() 
                else:
                    print("Error: Please type a valid Status!\n")
                    continue
            except ValueError:
                print("Error: Please type a valid Status!\n")
        elif choice == "6":
            data_to_save = []
            for t in tickets:
                data_to_save.append(t.to_dictionary())
                
            save_data(FILENAME, data_to_save)
            print("Data saved successfully. Goodbye!")
            break
            
        else:
            print("Invalid choice, please try again.\n")

if __name__ == "__main__":
    main()