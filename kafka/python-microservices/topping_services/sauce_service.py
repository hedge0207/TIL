import random

from base_service import BaseService


class SauceService(BaseService):
    _topping_type = "sauce"

    def _calc_topping(self):
        i = random.randint(0, 8)
        sauces = ["regular", "light", "extra", "none", "alfredo", "regular", "light", "extra", "alfredo"]
        return sauces[i]


if __name__ == "__main__":
    service = SauceService("pizza", "pizza-with-sauce")
    service.start_service()
