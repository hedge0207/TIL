from abc import ABCMeta, abstractmethod
from typing import List


class QuackObervable(metaclass=ABCMeta):
    @abstractmethod
    def register_observer(self, observer):
        pass

    @ abstractmethod
    def notify_observer(self):
        pass


class Observable(QuackObervable):
    def __init__(self, duck):
        self.observers = []
        self.duck = duck
    
    def register_observer(self, observer):
        self.observers.append(observer)
    
    def notify_observer(self):
        for observer in self.observers:
            observer.update(self.duck)


class Observer(metaclass=ABCMeta):
    def update(self, duck: QuackObervable):
        pass

class QuackLogist(Observer):
    def update(self, duck: QuackObervable):
        print("{}가 방금 소리 냈다.".format(duck.__class__.__name__))