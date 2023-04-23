from state import State, HasQuarterState, NoQuarterState, SoldState, SoldOutState, WinnerState



class GumballMachine:
    def __init__(self, num_gumballs):
        # 구성을 활용하여 각 상태에 대한 정보를 가지고 있는다.
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
    
    def insert_quarter(self):
        self.state.insert_quarter()
    
    def eject_quarter(self):
        self.state.eject_quarter()
    
    def turn_crank(self):
        self.state.turn_crank()
        self.state.dispense()
    
    def set_state(self, state: State):
        self.state = state
    
    def release_ball(self):
        print("캡슐을 내보내고 있습니다.")
        
        if self.count > 0:
            self.count -= 1
    
    # 각 상태 객체를 위한 getter 메서드들(get_quarter_state() 등)