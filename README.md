IT Support Ticket Triage System

Purpose: A command-line tool that allows users to create, view, search, and close IT support tickets while automatically saving all records to a local JSON database. 

Features (Capstone Requirements Met):
- Modular Code: Separated logic into main.py, utils.py, and logic.py.
- OOP: Used a custom Ticket class to manage ticket data and state.
- Data Persistence: Automatically reads and writes to a tickets.json file.
- Error Handling: Uses try-except blocks for file loading, API requests, and user input validation.
- Search Capabilities: Ability to filter tickets dynamically by ID or Status.
- External Packages: Integrates requests for an API call and rich for UI formatting.

Requirements: Python 3.x, plus the requests and rich external packages.

How to run:
python src/main.py

Example output:
Tip of the Day: Vinegar is a powerful cleaning agent.

-------------------------
1. View All Tickets
2. Add a New Ticket
3. Close a Ticket
4. Show a Ticket using ID
5. Show a Ticket using status
6. Save and Exit
-------------------------
Choose an option (1-6): 5
**********
1 to get all open tickets
2 to get all closed tickets
**********
Enter Ticket Status to Show: 2
ID: 2 | Title: MOUSE| Description:MMMM | Status: Closed | creation_date: 2026-09-12 02:33:00 | last_update_date: 2026-09-12 02:34:12

Known limitations: Ticket data is saved locally to a data/tickets.json file, meaning the database is local to your machine and cannot be accessed simultaneously from multiple computers.
