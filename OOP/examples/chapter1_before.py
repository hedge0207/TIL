from datetime import date


class Invitation:
    def __init__(self):
        self.when: date = None


class Ticket:
    def __init__(self):
        self.fee: int = None
        
    def get_fee(self) -> int:
        return self.fee
    

class Bag:
    def __init__(self, amount=None, invitation: Invitation=None):
        if not amount and not invitation:
            raise Exception()
        
        self.amount = amount
        self.invitation = invitation
        self.ticket: Ticket = None
        
    def has_invitation(self):
        return self.invitation is not None
    
    def has_ticket(self):
        return self.ticket is not None
    
    def set_ticket(self, ticket:Ticket):
        self.ticket = ticket
        
    def minus_amount(self, amount: int):
        self.amount -= amount


class Audience:
    def __init__(self, bag: Bag=None):
        self.bag = bag
    
    def get_bag(self) -> Bag:
        return self.bag
    

class TicketOffice:
    def __init__(self, amount, tickets:list[Ticket]):
        self.amount = amount
        self.tickets = tickets
    
    def get_ticket(self) -> Ticket:
        return self.tickets.pop()
    
    def plus_amount(self, amount):
        self.amount += amount


class TicketSeller:
    def __init__(self, ticket_office:TicketOffice):
        self.ticket_office = ticket_office
    
    def get_ticket_office(self) -> TicketOffice:
        return self.ticket_office


class Theater:
    def __init__(self, ticket_seller: TicketSeller):
        self.ticket_seller = ticket_seller
    
    def enter(self, audience: Audience):
        if audience.get_bag().has_invitation():
            ticket = self.ticket_seller.get_ticket_office().get_ticket()
            audience.get_bag().set_ticket(ticket)
        else:
            ticket = self.ticket_seller.get_ticket_office().get_ticket()
            audience.get_bag().minus_amount(ticket.get_fee())
            self.ticket_seller.get_ticket_office().plus_amount(ticket.get_fee())
            audience.get_bag().set_ticket(ticket)