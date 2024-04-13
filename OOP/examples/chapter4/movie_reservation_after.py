from __future__ import annotations
from datetime import datetime, time
from enum import Enum, auto
from typing_extensions import Self
from abc import ABC, abstractmethod


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


class Movie(ABC):

    def __init__(self, title: str, running_time: time, fee: Money, discount_conditions: list[DiscountCondition]=[]):
        self._title = title
        self._running_time = running_time
        self._fee = fee
        self._discount_conditions = discount_conditions
    
    def calculate_movie_fee(self, screening: Screening):
        if self._is_discountable(screening):
            return self._fee.minus(self._calculate_discount_amount())
        return self._fee
    
    def _is_discountable(self, screening: Screening):
        return any([discount_condition.is_satisfied_by(screening) 
                    for discount_condition in self._discount_conditions])
    
    @abstractmethod
    def _calculate_discount_amount(self):
        ...


class AmountDiscountMovie(Movie):

    def __init__(self, title: str, running_time: time, fee: Money, discount_conditions: list[DiscountCondition], 
                 discount_amount: Money):
        super().__init__(title, running_time, fee, discount_conditions)
        self._discount_amount = discount_amount

    def _calculate_discount_amount(self):
        return self._discount_amount
    

class PercentDiscountMovie(Movie):

    def __init__(self, title: str, running_time: time, fee: Money, discount_conditions: list[DiscountCondition], 
                 percent: float):
        super().__init__(title, running_time, fee, discount_conditions)
        self._percent = percent
    
    def _calculate_discount_amount(self):
        return self._fee * self._percent


class NoneDiscountMovie(Movie):
    def __init__(self, title: str, running_time: time, fee: Money):
        super().__init__(title, running_time, fee)

    def _calculate_discount_amount(self):
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


class DiscountCondition(ABC):

    @abstractmethod
    def is_satisfied_by(self, screening: Screening):
        ...


class PeriodCondition(DiscountCondition):

    def __init__(self, day_of_week: str=None, start_time: time=None, end_time: time=None):
        self._day_of_week = day_of_week
        self._start_time = start_time
        self._end_time = end_time

    def is_satisfied_by(self, screening: Screening):
        return screening._when_screened.weekday() == self._day_of_week and \
               self._start_time <= screening._when_screened() and \
               self._end_time >= screening._when_screened()


class SequenceCondition(DiscountCondition):

    def __init__(self, sequence: int=None):
        self._sequence = sequence

    def is_satisfied_by(self, screening: Screening):
        return self._sequence == screening._sequence