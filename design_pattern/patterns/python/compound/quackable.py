from abc import abstractmethod

from observer import QuackObervable

class Quackable(QuackObervable):

    @abstractmethod
    def quack(self):
        pass