from abc import ABCMeta, abstractmethod
from view import View


class Interface(metaclass=ABCMeta):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def increase_remain_time(self):
        pass

    @abstractmethod
    def decrease_remain_time(self):
        pass

    @abstractmethod
    def set_remain_time(self):
        pass


class Controller(Interface):
    def __init__(self, model):
        self.model = model
        self.view = View(self, self.model)
        self.view.display()

    def start(self):
        self.model.on()

    def stop(self):
        self.model.off()

    def increase_remain_time(self):
        remain_time = self.model.get_remain_time()
        self.model.set_remain_time(remain_time + 1)
    
    def decrease_remain_time(self):
        remain_time = self.model.get_remain_time()
        self.model.set_remain_time(remain_time - 1)
    
    def set_remain_time(self, remain_time):
        self.model.set_remain_time(remain_time)

