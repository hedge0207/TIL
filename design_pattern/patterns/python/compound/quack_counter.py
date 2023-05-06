from quackable import Quackable
from observer import Observable, Observer


class QuackCounter(Quackable):
    num_of_quack = 0

    def __init__(self, duck: Quackable):
        self.duck = duck

    def quack(self):
        self.duck.quack()
        QuackCounter.num_of_quack += 1

    @classmethod
    def get_quacks(cls):
        return cls.num_of_quack
    
    def register_observer(self, observer: Observer):
        self.duck.register_observer(observer)
    
    def notify_observer(self):
        self.duck.notify_observer()
