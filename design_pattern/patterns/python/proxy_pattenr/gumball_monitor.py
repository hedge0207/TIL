from gumball_machine import GumballMachine


class GumballMonitor:

    def __init__(self, machine: GumballMachine):
        self.machine = machine

    def report(self):
        print("위치:", self.machine.get_location())
        print("재고:", self.machine.get_count())
        print("상태:", self.machine.get_state())