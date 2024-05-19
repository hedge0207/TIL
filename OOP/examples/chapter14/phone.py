from __future__ import annotations
from datetime import datetime, date, time, timedelta
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
        self._interval = DateTimeInterval(from_, to)
    
    def get_duration(self):
        return self._interval.duration()
    
    def get_from(self):
        return self._interval._from
    
    def get_to(self):
        return self._interval.to
    
    def get_interval(self):
        return self._interval
    
    def split_by_day(self):
        return self._interval.split_by_day()


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


class FixedFeePolicy(BasicRatePolicy):
    
    def __init__(self, amount: Money, seconds: int):
        self._amount = amount
        self._seconds = seconds

    def _calculate_call_fee(self, call: Call):
        return self._amount.times(call.get_duration().total_seconds() / self._seconds)


class DateTimeInterval:

    def __init__(self, from_: datetime, to: datetime):
        self._from = from_
        self._to = to

    @property
    def from_(self):
        return self._from
    
    @property
    def to(self):
        return self._to
    
    def to_midnight(self, from_: datetime):
        return DateTimeInterval(from_, datetime(from_.year, from_.month, from_.day, 23, 59, 59, 999_999))
    
    def from_midnight(self, to: datetime):
        return DateTimeInterval(
            datetime(to.year, to.month, to.day, 0, 0),
            to
        )
    
    def during(self, date_: date):
        return DateTimeInterval(
            datetime(date_.year, date_.month, date_.day, 0, 0),
            datetime(date_.year, date_.month, date_.day, 23, 59, 59, 999_999),
        )

    def duration(self):
        return self.to - self._from
    
    def split_by_day(self):
        days = self._days()
        if days > 0:
            return self._split(days)
        else:
            return [self]
    
    def _days(self):
        return (self._to.date() - self._from.date()).days

    def _split(self, days: int):
        result = []
        self._add_first_day(result)
        self._add_middle_days(result, days)
        self._add_last_day(result)
        return result

    def _add_first_day(self, result: list[DateTimeInterval]):
        result.append(self.to_midnight(self._from))

    def _add_middle_days(self, result: list[DateTimeInterval], days: int):
        for i in range(1, days):
            result.append(self.during(self._from + timedelta(days=i)))
    
    def _add_last_day(self, result: list[DateTimeInterval]):
        result.append(self.from_midnight(self._to))


class TimeOfDayDiscountPolicy(BasicRatePolicy):
    
    def __init__(self):
        self._starts: list[time] = []
        self._ends: list[time] = []
        self._durations: list[int] = []
        self._amounts: list[Money] = []

    def _calculate_call_fee(self, call: Call):
        result = Money.wons(0)
        for interval in call.split_by_day():
            for i in range(len(self._starts)):
                from_ = self._from(interval, self._starts[i])
                to = self._to(interval, self._ends[i])
                delta = datetime.combine(datetime.today(), to) - datetime.combine(datetime.today(), from_)
                result = result.plus(self._amounts[i].times(delta.seconds / self._durations[i]))
        return result
    
    def _from(self, interval: DateTimeInterval, from_: time):
        return from_ if interval.from_.time() < from_ else interval.from_.time()
    
    def _to(self, interval: DateTimeInterval, to: time):
        return to if interval.to.time() > to else interval.to.time()


class DayOfWeekDiscountRule:
    
    def __init__(self, day_of_week: int, duration: int, amount: Money):
        self._day_of_week = day_of_week
        self._duration = duration
        self._amount = amount

    def calculate(self, interval: DateTimeInterval):
        if self._day_of_week == interval.from_.weekday():
            return self._amount.times(interval.duration().seconds / self._duration)
        return Money.wons(0)
    

class DayOfWeekDiscountPolicy(BasicRatePolicy):
    
    def __init__(self, rules: list[DayOfWeekDiscountRule]):
        self._rules = rules

    def _calculate_call_fee(self, call: Call):
        result = Money.wons(0)
        for interval in call.get_interval().split_by_day():
            for rule in self._rules:
                result = result.plus(rule.calculate(interval))
        return result


class DurationDiscountRule(FixedFeePolicy):

    def __init__(self, from_: int, to: int, amount: Money, seconds: int):
        super().__init__(amount, seconds)
        self._from = from_
        self._to = to

    def calculate(self, call: Call):
        
        if call.get_duration().seconds < self._from:
            return Money.wons(0)

        # 부모 클래스의 calculate_fee 메서드는 Phone 클래스의 인스턴스를 파라미터로 받는다.
        # calculate_fee를 재사용하기 위해 임시 Phone을 만든다.
        phone = Phone(None)
        phone.call(Call(call.get_from() + timedelta(seconds=self._from),
                        call.get_from() + timedelta(seconds=self._to) 
                        if call.get_duration().seconds > self._to
                        else call.get_to()))
        print(super().calculate_fee(phone)._amount)
        return super().calculate_fee(phone)
    

class DurationDiscountPolicy(BasicRatePolicy):

    def __init__(self, rules: list[DurationDiscountRule]):
        self._rules = rules
    
    def _calculate_call_fee(self, call: Call):
        result = Money.wons(0)
        for rule in self._rules:
            result = result.plus(rule.calculate(call))
        return result


if __name__ == "__main__":
    phone = Phone(DurationDiscountPolicy([
        DurationDiscountRule(0, 60, Money.wons(10), 10),
        DurationDiscountRule(60, 180, Money.wons(5), 10),
        DurationDiscountRule(180, 600, Money.wons(1), 10),
        DurationDiscountRule(600, 1800, Money.wons(0.5), 10),
    ]))
    phone.call(Call(datetime(2024, 11, 11, 22, 0, 0), datetime(2024, 11, 15, 12, 0, 0)))
    phone.call(Call(datetime(2024, 12, 11, 22, 0, 0), datetime(2024, 12, 11, 23, 0, 0)))
    phone.call(Call(datetime(2024, 11, 11, 0, 0, 0), datetime(2024, 11, 11, 0, 3, 0)))
    print(phone.calculate_fee()._amount)