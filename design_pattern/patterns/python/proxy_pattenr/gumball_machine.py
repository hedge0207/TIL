from state_pattern.state import State, HasQuarterState, NoQuarterState, SoldState, SoldOutState, WinnerState



class GumballMachine:
    def __init__(self, location, num_gumballs):
        self.location = location
        self.has_quarter_state:State = HasQuarterState()
        self.no_quarter_state:State = NoQuarterState()
        self.sold_state: State = SoldState()
        self.sold_out_state: State = SoldOutState()
        self.winner_state: State = WinnerState()

        self.count = num_gumballs
        if self.count > 0:
            self.state = self.no_quarter_state
        else:
            self.state = self.sold_out_state

    def get_location(self):
        return self.location

    def get_count(self):
        return self.count
    
    def get_state(self):
        return self.state