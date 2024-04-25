from datetime import datetime
from typing_extensions import Self
from typing import List


class Money:
    def __init__(self, amount):
        self._amount = amount

    @classmethod
    def wons(self, amount) -> Self:
        return Money(amount)

    def plus(self, amount: Self) -> Self:
        return Money(self._amount + amount._amount)

    def minus(self, amount: Self) -> Self:
        return Money(self._amount - amount._amount)

    def times(self, percent: int) -> Self:
        return Money(self._amount * percent)

    def is_lt(self, other: Self) -> bool:
        return self._amount < other._amount

    def is_gte(self, other: Self) -> bool:
        return self._amount >= other._amount


class Call:
    def __init__(self, from_: datetime, to: datetime):
        self._from = from_
        self._to = to
    
    def get_duration(self):
        return self._to-self._from
    

class Phone:
    def __init__(self, amount: Money, seconds: int, tax_rate: float):
        self._amount = amount
        self._seconds = seconds
        self._tax_rate = tax_rate
        self._calls: List[Call] = []

    def call(self, call: Call):
        self._calls.append(call)

    def calculate_fee(self) -> Money:
        result = Money.wons(0)
        for call in self._calls:
            result = result.plus(self._amount.times(call.get_duration().total_seconds() / self._seconds))
        return result.plus(result.times(self._tax_rate))


class NightlyDiscountPhone(Phone):

    LATE_NIGHT_HOUR = 22

    def __init__(self, nightly_amount: Money, regular_amount: Money, seconds: int, tax_rate: float):
        super(self).__init__(regular_amount, seconds, tax_rate)
        self._nightly_amount = nightly_amount

    def call(self, call: Call):
        self._calls.append(call)

    def calculate_fee(self) -> Money:
        result = super(self).calculate_fee()

        nighlty_fee = Money.wons(0)
        for call in self._calls:
            if call._from.hour >= self.LATE_NIGHT_HOUR:
                nighlty_fee = nighlty_fee.plus(self._amount.minus(self._nightly_amount).times(call.get_duration().total_seconds() / self._seconds))
        
        return result.minus(nighlty_fee.plus(nighlty_fee.times(self._tax_rate)))



if __name__ == "__main__":
    phone = NightlyDiscountPhone(Money.wons(1), Money.wons(5), 10, 0.02)
    phone.call(Call(datetime(2024, 11, 11, 22, 30, 0), datetime(2024, 11, 12)))
    print(phone.calculate_fee()._amount)
