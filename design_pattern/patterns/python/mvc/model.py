from abc import ABCMeta, abstractmethod
import time


class Interface(metaclass=ABCMeta):
    @abstractmethod
    def count_down(self):
        pass

    @abstractmethod
    def on(self):
        pass
    
    @abstractmethod
    def off(self):
        pass

    @abstractmethod
    def set_remain_time(self, bpm):
        pass

    @abstractmethod
    def get_remain_time(self):
        pass

    @abstractmethod
    def register_observer(self, observer):
        pass

    @abstractmethod
    def remove_observer(self, observer):
        pass


class Model(Interface):
    def __init__(self):
        self.observers = []
        self.input_time = 60
        self.start_time = 0
        self.remain_time = 60
        self.stop = False
    
    def count_down(self):
        while 1:
            elapsed_time = time.time()-self.start_time
            yield elapsed_time

    def on(self):
        self.stop = False
        self.start_time = time.time()
        timer = self.count_down()
        while 1:
            self.remain_time = next(timer)
            if self.remain_time <= 0:
                break

    def off(self):
        self.stop = True
        self.remain_time = self.input_times

    def get_remain_time(self):
        return self.remain_time
    
    def set_remain_time(self, remain_time):
        print(self.remain_time)
        self.remain_time = remain_time
        self.notify_observers()
    
    def register_observer(self, observer):
        self.observers.append(observer)
    
    def remove_observer(self, observer):
        self.observers.remove(observer)
    
    def notify_observers(self):
        for observer in self.observers:
            observer.update_remain_time()