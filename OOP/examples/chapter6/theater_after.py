class Ticket:
    ...


class Invitation:
    ...


class TicketOffice:
    ...


class Bag:
    def __init__(self, amount=None, invitation: Invitation=None):
        if not amount and not invitation:
            raise Exception()
        
        self.amount = amount
        self.invitation = invitation
        self.ticket: Ticket = None
        
    def has_invitation(self):
        return self.invitation is not None
    
    def set_ticket(self, ticket: Ticket):
        if self.has_invitation():
            self.ticket = ticket
            return 0
        else:
            self.ticket = ticket
            self.minus_amount(ticket.get_fee())
            return ticket.get_fee()
        
    def minus_amount(self, amount: int):
        self.amount -= amount

class Audience:
    def __init__(self, bag: Bag=None):
        self.bag = bag
    
    def set_ticket(self, ticket: Ticket):
        return self.bag.set_ticket(ticket)

class TicketSeller:
    def __init__(self, ticket_office: TicketOffice):
        self.ticket_office = ticket_office
    
    def get_ticket_office(self) -> TicketOffice:
        return self.ticket_office
        
    def set_ticket(self, audience: Audience):
        self.ticket_office.plus_amount(audience.set_ticket(self.ticket_office.get_ticket()))



class Theater:
    def __init__(self, ticket_seller: TicketSeller):
        self.ticket_seller = ticket_seller
    
    def enter(self, audience: Audience):
        self.ticket_seller.set_ticket(audience)