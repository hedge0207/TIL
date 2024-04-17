from __future__ import annotations
from datetime import datetime, time
from enum import Enum, auto
from typing_extensions import Self


class Screening:
    def __init__(self, movie: Movie, sequence: int, when_screened: datetime):
        self._movie = movie
        self._sequence = sequence
        self._when_screened = when_screened

    def reserve(self, customer: Customer, audience_count: int):
        return Reservation(customer, self, self._calculate_fee(audience_count), audience_count)
    
    def _calculate_fee(self, audience_count: int):
        return self._movie.calculate_movie_fee(self).times(audience_count)
    

class MovieType(str, Enum):
    AMOUNT_DISCOUNT = auto()
    PECENT_DISCOUNT = auto()
    NONE_DISCOUNT = auto()


class Movie:
    
    def __init__(self, title: str, running_time: time, fee: Money, discount_conditions: list[DiscountCondition],
                 movie_type: MovieType, discount_amount: Money, discount_percent: float):
        self._title = title
        self._running_time = running_time
        self._fee = fee
        self._discount_conditions = discount_conditions
        self._movie_type = movie_type
        self._discount_amount = discount_amount
        self._discount_percent = discount_percent

    def calculate_movie_fee(self, screening: Screening):
        if self._is_discountable(screening):
            return self._fee.minus(self._calculate_discount_amount())
        return self._fee
    
    def _is_discountable(self, screening: Screening):
        return any([discount_condition.is_satisfied_by(screening) 
                    for discount_condition in self._discount_conditions])

    def _calculate_discount_amount(self):
        match self._movie_type:
            case MovieType.AMOUNT_DISCOUNT:
                return self._calculate_amount_discount_amount()
            case MovieType.PECENT_DISCOUNT:
                return self._calculate_percent_discount_amount()
            case MovieType.NONE_DISCOUNT:
                return self._calculate_none_discount_anount()

    def _calculate_amount_discount_amount(self):
        return self._discount_amount
    
    def _calculate_percent_discount_amount(self):
        return self._fee.times(self._discount_percent)
    
    def _calculate_none_discount_anount(self):
        return Money.wons(0)


class Customer:
    ...


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


class Reservation:
    ...


class DiscountConditionType(str, Enum):
    SEQUENCE = auto()
    PERIOD = auto()


class DiscountCondition:
    
    def __init__(self, discount_condition_type: DiscountConditionType, sequence: int=None, 
                 day_of_week: str=None, start_time: time=None, end_time: time=None):
        self._discount_condition_type = discount_condition_type
        self._sequence = sequence
        self._day_of_week = day_of_week
        self._start_time = start_time
        self._end_time = end_time

    def is_satisfied_by(self, screening: Screening):
        if self._discount_condition_type == DiscountConditionType.PERIOD:
            return self._is_satisfied_by_period(screening)
        return self._is_satisfied_by_sequence(screening)
    
    def _is_satisfied_by_period(self, screening: Screening):
        return screening._when_screened.weekday() == self._day_of_week and \
               self._start_time <= screening._when_screened() and \
               self._end_time >= screening._when_screened()
    
    def _is_satisfied_by_sequence(self, screening: Screening):
        return self._sequence == screening._sequence