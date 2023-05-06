from abc import ABCMeta, abstractmethod
from quackable import Quackable
from duck import MallardDuck, RedHeadDuck, RubberDuck, DuckCall
from quack_counter import QuackCounter


class AbstractDuckFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_mallard_duck(self) -> Quackable:
        pass

    @abstractmethod
    def create_red_head_duck(self) -> Quackable:
        pass

    @abstractmethod
    def create_rubber_duck(self) -> Quackable:
        pass

    @abstractmethod
    def create_duck_call(self) -> Quackable:
        pass


class CountingDuckFactory(AbstractDuckFactory):
    def create_mallard_duck(self) -> Quackable:
        return QuackCounter(MallardDuck())
    
    def create_red_head_duck(self) -> Quackable:
        return QuackCounter(RedHeadDuck())
    
    def create_rubber_duck(self) -> Quackable:
        return QuackCounter(RubberDuck())
    
    def create_duck_call(self) -> Quackable:
        return QuackCounter(DuckCall())