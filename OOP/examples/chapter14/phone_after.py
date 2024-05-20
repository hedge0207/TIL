from __future__ import annotations
from datetime import datetime, date, timedelta, time
from abc import ABC, abstractmethod
from typing_extensions import Self
from typing import List
from functools import reduce



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


class FeeCondition(ABC):

    def find_time_intervals(self, call: Call):
        ...


class TimeOfDayFeeCondition(FeeCondition):

    def __init__(self, from_: time, to: time):
        self._from = from_
        self._to = to
    
    def find_time_intervals(self, call: Call):
        result = []
        for interval in call.get_interval().split_by_day():
            from_time = self._get_from(interval)
            to_time = self._get_to(interval)
            if from_time <= to_time:
                result.append(DateTimeInterval(
                    datetime(interval.from_.year, interval.from_.month, interval.from_.day, from_time.hour, from_time.minute, from_time.second), 
                    datetime(interval.to.year, interval.to.month, interval.to.day, to_time.hour, to_time.minute, to_time.second)
                ))
        
        return result
    
    def _get_from(self, interval: DateTimeInterval):
        return self._from if interval.from_.time() < self._from else interval.from_.time()
    
    def _get_to(self, interval: DateTimeInterval):
        return self._to if interval.to.time() > self._to else interval.to.time()
    

class DayOfWeekFeeCondition(FeeCondition):

    def __init__(self, day_of_week: list[int]):
        self._day_of_week = day_of_week

    def find_time_intervals(self, call: Call):
        result = []
        for interval in call.get_interval().split_by_day():
            if interval.from_.weekday() in self._day_of_week:
                result.append(interval)
        return result


class DurationFeeCondition(FeeCondition):

    def __init__(self, from_: int, to: int):
        self._from = from_
        self._to = to
    
    def find_time_intervals(self, call: Call):
        # 구현
        ...



    

class FeePerduration:

    def __init__(self, fee: Money, duration: int):
        self._fee = fee
        self._duration = duration
    
    def calculate(self, interval: DateTimeInterval):
        return self._fee.times(round(interval.duration().seconds / self._duration))


class FeeRule:
     
    def __init__(self, fee_condition: FeeCondition, fee_per_duration: FeePerduration):
         self._fee_condition = fee_condition
         self._fee_per_duration = fee_per_duration
    
    def calculate_fee(self, call: Call):
        return reduce(lambda acc, val: acc.plus(val), 
               map(lambda duration: self._fee_per_duration.calculate(duration), 
                   self._fee_condition.find_time_intervals(call)), 
               Money.wons(0))
        

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

    def __init__(self, fee_rules: List[FeeRule]):
        self._fee_rules = fee_rules

    def calculate_fee(self, phone: Phone):
        return reduce(lambda acc, val: acc.plus(val), 
                      map(lambda call: self._calculate(call), phone.calls), 
                      Money.wons(0))
    
    def _calculate(self, call: Call):
        return reduce(lambda acc, val: acc.plus(val), 
                      map(lambda rule: rule.calculate_fee(call), self._fee_rules), 
                      Money.wons(0))
    

if __name__ == "__main__":
    phone = Phone(BasicRatePolicy([
        FeeRule(
            TimeOfDayFeeCondition(
                time(5, 0, 0), time(0, 0, 0)
            ),
            FeePerduration(Money.wons(2), 5)
        ),
        FeeRule(
            TimeOfDayFeeCondition(
                time(0, 0, 0), time(0, 5, 0)
            ),
            FeePerduration(Money.wons(1), 5)
        )
    ]))
    phone.call(Call(datetime(2024, 11, 11, 23, 0, 0), datetime(2024, 11, 12, 1, 0, 0)))
    # phone.call(Call(datetime(2024, 12, 11, 22, 0, 0), datetime(2024, 12, 11, 23, 0, 0)))

    print(phone.calculate_fee()._amount)