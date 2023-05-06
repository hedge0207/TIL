from typing import List

from quackable import Quackable
from observer import Observer



class Flock(Quackable):
    def __init__(self):
        self.quackers: List[Quackable] = []

    def add(self, qucker:Quackable):
        self.quackers.append(qucker)
    
    def quack(self):
        for quacker in self.quackers:
            quacker.quack()
    
    def register_observer(self, observer: Observer):
        for quacker in self.quackers:
            quacker.register_observer(observer)
    
    def notify_observer(self):
        pass