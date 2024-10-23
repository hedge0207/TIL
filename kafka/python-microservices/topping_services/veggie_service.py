import random

from base_service import BaseService


class VeggieService(BaseService):
    _topping_type = "veggies"

    def _calc_topping(self):
        i = random.randint(0,4)
        veggies = ["tomato", "olives", "onions", "peppers", "pineapple", "mushrooms", "tomato", "olives", "onions", "peppers", "pineapple", "mushrooms"]
        selection = []
        if i == 0:
            return "none"
        else:
            for _ in range(i):
                selection.append(veggies[random.randint(0, 11)])
        return " & ".join(set(selection))

if __name__ == "__main__":
    service = VeggieService("pizza-with-meats", "pizza-with-veggies")
    service.start_service()
