class Ticket:
    def __init__(self, ticket_id, title, creation_date, last_update_date, description =None ,status="Open"):
        self.ticket_id = ticket_id
        self.title = title
        self.creation_date=creation_date
        self.last_update_date=last_update_date
        self.description=description
        self.status = status


    def to_dictionary(self):
        return {
            "id": self.ticket_id,
            "title": self.title,
            "creation_date":str(self.creation_date),
            "last_update_date":str(self.last_update_date),
            "description":self.description,
            "status": self.status
        }