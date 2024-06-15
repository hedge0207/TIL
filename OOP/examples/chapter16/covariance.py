class Publisher:
    ...

class IndependentPublisher(Publisher):
    ...

class Book:
    def __init__(self, publisher: Publisher):
        self._publisher = publisher
    
class Megazine(Book):
    def __init__(self, publisher: Publisher):
        self._publisher = publisher

class BookStall:
    def sell(self, independent_publisher: IndependentPublisher):
        return Book(independent_publisher)
    
class MegazineStore(BookStall):
    def sell(self, publisher: Publisher):
        return Megazine(publisher=publisher)
        
class Customer:

    def __init__(self):
        self._book: Book = None

    def order(self, book_stall: BookStall):
        self._book = book_stall.sell(IndependentPublisher())