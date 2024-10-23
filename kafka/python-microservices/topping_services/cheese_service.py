import random

from base_service import BaseService


class CheeseService(BaseService):
    _topping_type = "cheese"

    def _calc_topping(self):
        i = random.randint(0, 6)
        cheeses = ["extra", "none", "three cheese", "goat cheese", "extra", "three cheese", "goat cheese"]
        return cheeses[i]

if __name__ == "__main__":
    service = CheeseService("pizza-with-sauce", "pizza-with-cheese")
    service.start_service()
