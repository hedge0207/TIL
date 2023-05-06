from observer import Observable, Observer


class Goose:
    def __init__(self):
        self.observable = Observable(self)
    
    def honk(self):
        print("honk")
        self.notify_observer()

    def register_observer(self, observer: Observer):
        self.observable.register_observer(observer)
    
    def notify_observer(self):
        self.observable.notify_observer()
    