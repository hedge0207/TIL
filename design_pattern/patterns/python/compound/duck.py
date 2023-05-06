from quackable import Quackable
from observer import Observable, Observer


class MallardDuck(Quackable):
    def __init__(self):
        self.observable = Observable(self)
    
    def quack(self):
        print("Quack")
        self.notify_observer()

    def register_observer(self, observer: Observer):
        self.observable.register_observer(observer)
    
    def notify_observer(self):
        self.observable.notify_observer()


class RedHeadDuck(Quackable):
    def __init__(self):
        self.observable = Observable(self)

    def quack(self):
        print("Quack")
        self.notify_observer()
    
    def register_observer(self, observer: Observer):
        self.observable.register_observer(observer)
    
    def notify_observer(self):
        self.observable.notify_observer()


class RubberDuck(Quackable):
    def __init__(self):
        self.observable = Observable(self)

    def quack(self):
        print("Squeak")
        self.notify_observer()
    
    def register_observer(self, observer: Observer):
        self.observable.register_observer(observer)
    
    def notify_observer(self):
        self.observable.notify_observer()


class DuckCall(Quackable):
    def __init__(self):
        self.observable = Observable(self)

    def quack(self):
        print("Quck")
        self.notify_observer()
    
    def register_observer(self, observer: Observer):
        self.observable.register_observer(observer)
    
    def notify_observer(self):
        self.observable.notify_observer()