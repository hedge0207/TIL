from quackable import Quackable
from goose import Goose
from observer import Observable, Observer


class GooseAdapter(Quackable):
    def __init__(self, goose: Goose):
        self.goose = goose
        self.observable = Observable(self)

    def quack(self):
        self.goose.honk()

    def register_observer(self, observer: Observer):
        self.observable.register_observer(observer)
    
    def notify_observer(self):
        self.observable.notify_observer()