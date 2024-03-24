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
        
        self._amount = amount
        self._invitation = invitation
        self._ticket: Ticket = None
        
    def _has_invitation(self):
        return self._invitation is not None
    
    def _set_ticket(self, ticket:Ticket):
        self._ticket = ticket
        
    def _minus_amount(self, amount: int):
        self._amount -= amount
    
    def hold(self, ticket:Ticket):
        if self._has_invitation():
            self._set_ticket(ticket)
            return 0
        else:
            self._set_ticket(ticket)
            self._minus_amount(ticket.get_fee())
            return ticket.get_fee()


class Audience:
    def __init__(self, bag: Bag=None):
        self._bag = bag
    
    def buy(self, ticket: Ticket) -> int:
        return self._bag.hold(ticket)
    

class TicketOffice:
    def __init__(self, amount, tickets:list[Ticket]):
        self.amount = amount
        self.tickets = tickets
    
    def _get_ticket(self) -> Ticket:
        return self.tickets.pop()
    
    def _plus_amount(self, amount):
        self.amount += amount
    
    def sell_ticket_to(self, audience: Audience):
        self._plus_amount(audience.buy(self._get_ticket()))


class TicketSeller:
    def __init__(self, ticket_office:TicketOffice):
        self._ticket_office = ticket_office
    
    def sell_to(self, audience: Audience):
        self._ticket_office.sell_ticket_to(audience)
            
            
class Theater:
    def __init__(self, ticket_seller: TicketSeller):
        self.ticket_seller = ticket_seller
    
    def enter(self, audience: Audience):
        self.ticket_seller.sell_to(audience)