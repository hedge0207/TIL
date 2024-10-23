import random

from base_service import BaseService


class MeatService(BaseService):
    _topping_type = "meats"

    def _calc_topping(self):
        i = random.randint(0, 4)
        meats = ["pepperoni", "sausage", "ham", "anchovies", "salami", "bacon", "pepperoni", "sausage", "ham", "anchovies", "salami", "bacon"]
        selection = []
        if i == 0:
            return "none"
        else:
            for _ in range(i):
                selection.append(meats[random.randint(0, 11)])
        return " & ".join(set(selection))

if __name__ == "__main__":
    service = MeatService("pizza-with-cheese", "pizza-with-meats")
    service.start_service()