import uuid


class Pizza:
    def __init__(self):
        self.order_id = ''
        self.sauce = ''
        self.cheese = ''
        self.meats = ''
        self.veggies = ''



class PizzaOrder:
    def __init__(self, count):
        self.id = str(uuid.uuid4().int)
        self.count = count
        self.pizzas = []

    def add_pizza(self, pizza):
        self.pizzas.append(pizza)

    def get_pizzas(self):
        return self.pizzas
