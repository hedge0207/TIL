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

    def __init__(self, rate_policy: RatePolicy):
        self._calls: List[Call] = []
        self._rate_policy = rate_policy

    def call(self, call: Call):
        self._calls.append(call)

    def calculate_fee(self) -> Money:
        return self._rate_policy.calculate_fee(self)

    @property
    def calls(self):
        return self._calls


class RatePolicy(ABC):

    @abstractmethod
    def calculate_fee(self, phone: Phone):
        ...


class BasicRatePolicy(RatePolicy):

    def calculate_fee(self, phone: Phone):
        result = Money.wons(0)

        for call in phone.calls:
            result = result.plus(self._calculate_call_fee(call))
        
        return result
    
    @abstractmethod
    def _calculate_call_fee(self, call: Call):
        ...


class RegularPolicy(BasicRatePolicy):
    
    def __init__(self, amount: Money, seconds: int):
        self._amount = amount
        self._seconds = seconds

    def _calculate_call_fee(self, call: Call):
        return self._amount.times(call.get_duration().total_seconds() / self._seconds)
    

class NightlyDiscountPolicy(BasicRatePolicy):

    LATE_NIGHT_HOUR = 22
    
    def __init__(self, nightly_amount: Money, regular_amount: Money, seconds: int):
        self._nightly_amount = nightly_amount
        self._regular_amount = regular_amount
        self._seconds = seconds

    def _calculate_call_fee(self, call: Call):
        if call._from.hour >= self.LATE_NIGHT_HOUR:
            return self._nightly_amount.times(call.get_duration().total_seconds() / self._seconds)
        else:
            return self._regular_amount.times(call.get_duration().total_seconds() / self._seconds)


class AdditionalRatePolicy(RatePolicy):

    def __init__(self, next_: RatePolicy):
        self._next = next_

    def calculate_fee(self, phone: Phone):
        fee = self._next.calculate_fee(phone)
        return self._after_calculated(fee)
    
    @abstractmethod
    def _after_calculated(self, fee: Money):
        ...
    

class TaxablePolicy(AdditionalRatePolicy):
    
    def __init__(self, tax_ratio: float, next_: RatePolicy):
        super().__init__(next_)
        self._tax_ratio = tax_ratio

    def _after_calculated(self, fee: Money):
        return fee.plus(fee.times(self._tax_ratio))
    

class RateDiscountPolicy(AdditionalRatePolicy):

    def __init__(self, amount: Money, next_: RatePolicy):
        super().__init__(next_)
        self._amount = amount
    
    def _after_calculated(self, fee: Money):
        return fee.minus(self._amount)


if __name__ == "__main__":
    phone = Phone(TaxablePolicy(0.02, RegularPolicy(Money(10), 10)))
    # phone = Phone(RateDiscountPolicy(Money.wons(10), TaxablePolicy(0.02, NightlyDiscountPolicy(Money(5), Money(10), 10))))
    phone.call(Call(datetime(2024, 11, 11, 22, 30, 0), datetime(2024, 11, 12)))
    phone.call(Call(datetime(2024, 12, 10, 22, 30, 0), datetime(2024, 12, 11)))
    print(phone.calculate_fee()._amount)