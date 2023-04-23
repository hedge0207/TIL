from abc import ABCMeta, abstractmethod
import random


class State(metaclass=ABCMeta):
    
    @abstractmethod
    def insert_quarter(self):
        pass

    @abstractmethod
    def eject_quarter(self):
        pass

    @abstractmethod
    def turn_crank(self):
        pass

    @abstractmethod
    def dispense(self):
        pass

class HasQuarterState(State):
    def __init__(self, gumball_machine):
        self.gumball_machine = gumball_machine
    
    # 부적절
    def insert_quarter(self):
        print("이미 동전을 넣으셨습니다.")
    
    def eject_quarter(self):
        print("동전을 반환합니다.")
        self.gumball_machine.set_state(self.gumball_machine.get_not_quarter_state())
    
    def turn_crank(self):
        print("손잡이를 돌리셨습니다.")
        winner = random.choices([True, False], weights=[0.1, 0.9])[0]

        if winner and self.gumball_machine.get_count() > 1:
            self.gumball_machine.set_state(self.gumball_machine.get_winner_state())
        else:
            self.gumball_machine.set_state(self.gumball_machine.get_sold_state())
    
    # 부적절
    def dispense(self):
        print("캡슐을 내보낼 수 없습니다.")
    


class NoQuarterState(State):
    
    def __init__(self, gumball_machine):
        self.gumball_machine = gumball_machine
    
    def insert_quarter(self):
        print("동전을 넣으셨습니다.")
        self.gumball_machine.set_state(self.gumball_machine.get_has_quarter_state())
    
    def eject_quarter(self):
        print("반환 할 동전이 없습니다.")
    
    def turn_crank(self):
        print("먼저 동전을 넣어주세요.")
    
    def dispense(self):
        print("먼저 동전을 넣어주세요.")


class SoldState(State):
    def __init__(self, gumball_machine):
        self.gumball_machine = gumball_machine
    
    # 부적절
    def insert_quarter(self):
        print("캡슐을 내보내고 있습니다.")
    
    # 부적절
    def eject_quarter(self):
        print("이미 캡슐을 뽑으셨습니다.")
    
    # 부적절
    def turn_crank(self):
        print("이미 손잡이를 돌리셨습니다.")
    
    def dispense(self):
        self.gumball_machine.release_ball()
        if self.gumball_machine.get_count > 0:
            self.gumball_machine.set_state(self.gumball_machine.get_no_quarter_state())
        else:
            print("캡슐이 모두 떨어졌습니다.")
            self.gumball_machine.set_state(self.gumball_machine.get_sold_out_state())

class SoldOutState(State):
    def __init__(self, gumball_machine):
        self.gumball_machine = gumball_machine
    
    def insert_quarter(self):
        print("캡슐이 모두 떨어졌습니다.")
    
    def eject_quarter(self):
        print("반환 할 동전이 없습니다.")
    
    def turn_crank(self):
        print("캡슐이 모두 떨어졌습니다.")
    
    def dispense(self):
        print("캡슐이 모두 떨어졌습니다.")


class WinnerState(State):
    def __init__(self, gumball_machine):
        self.gumball_machine = gumball_machine
    
    # 부적절
    def insert_quarter(self):
        print("캡슐을 내보내고 있습니다.")
    
    # 부적절
    def eject_quarter(self):
        print("이미 캡슐을 뽑으셨습니다.")
    
    # 부적절
    def turn_crank(self):
        print("이미 손잡이를 돌리셨습니다.")
    
    def dispense(self):
        self.gumball_machine.release_ball()
        if self.gumball_machine.get_count() == 0:
            self.gumball_machine.set_state(self.gumball_machine.get_sold_out_state())
        else:
            print("축하드립니다. 캡슐을 하나 더 드리겠습니다.")
            self.gumball_machine.release_ball()
            if self.gumball_machine.get_count > 0:
                self.gumball_machine.set_state(self.gumball_machine.get_no_quarter_state())
            else:
                print("캡슐이 모두 떨어졌습니다.")
                self.gumball_machine.set_state(self.gumball_machine.get_sold_out_state())
