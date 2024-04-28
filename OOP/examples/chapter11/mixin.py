from __future__ import annotations
from datetime import datetime
from typing_extensions import Self
from typing import List
from abc import ABC, abstractmethod


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

    def times(self, percent: float) -> Self:
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
    
    @property
    def from_(self):
        return self._from
    
    @property
    def to(self):
        return self._to


class Phone(ABC):

    def __init__(self):
        self._calls: List[Call] = []

    def call(self, call: Call):
        self._calls.append(call)

    @property
    def calls(self):
        return self._calls


class BasicRatePolicy(ABC):
    def calculate_fee(self, phone: Phone) -> Money:
        result = Money.wons(0)
        for call in phone.calls:
            result = result.plus(self._calculate_call_fee(call))
        return result

    @abstractmethod
    def _calculate_call_fee(self, call) -> Money:
        pass


class RegularPolicy(BasicRatePolicy):
    def __init__(self, amount: Money, seconds: int):
        self.amount = amount
        self.seconds = seconds

    def _calculate_call_fee(self, call: Call) -> Money:
        return self.amount.times(call.get_duration().total_seconds() / self.seconds)
    

class NightlyDiscountPolicy(BasicRatePolicy):

    LATE_NIGHT_HOUR = 22

    def __init__(self, nightly_amount: Money, regular_amount: Money, seconds: int):
        self._nightly_amount = nightly_amount
        self._regular_amount = regular_amount
        self._seconds = seconds
    
    def _calculate_call_fee(self, call: Call) -> Money:
        if call._from.hour >= self.LATE_NIGHT_HOUR:
            return self._nightly_amount.times(call.get_duration().total_seconds() / self._seconds)
        else:
            return self._regular_amount.times(call.get_duration().total_seconds() / self._seconds)


class TaxablePolicy(BasicRatePolicy):
    
    def __init__(self, tax_ratio: float):
        self._tax_ratio = tax_ratio

    def calculate_fee(self, phone: Phone):
        fee: Money = super().calculate_fee(phone)
        return fee.plus(fee.times(self._tax_ratio))


class RateDiscountPolicy(BasicRatePolicy):

    def __init__(self, discount_amount: Money):
        self._discount_amount = discount_amount

    def calculate_fee(self, phone: Phone):
        fee: Money = super().calculate_fee(phone)
        return fee.minus(self._discount_amount)


class TaxableRegularPolicy(TaxablePolicy, RegularPolicy):
    def __init__(self, amount: Money, seconds: int, tax_ratio: float):
        RegularPolicy.__init__(self, amount, seconds)
        TaxablePolicy.__init__(self, tax_ratio)

    

if __name__ == "__main__":
    policy = TaxableRegularPolicy(Money(10), 10, 0.02)
    phone = Phone()
    phone.call(Call(datetime(2024, 11, 11, 22, 30, 0), datetime(2024, 11, 12)))
    phone.call(Call(datetime(2024, 12, 10, 22, 30, 0), datetime(2024, 12, 11)))
    print(policy.calculate_fee(phone)._amount)