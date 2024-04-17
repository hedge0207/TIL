from __future__ import annotations
from enum import Enum, auto
from datetime import time
from typing_extensions import Self


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


class DiscountConditionType(str, Enum):
    SEQUENCE = auto()
    PERIOD = auto()


class DiscountCondition:
    def __init__(self, type_: DiscountConditionType, sequence: int, 
                 day_of_week: str, start_time: time, end_time: time):
        self._type = type_
        self._sequence = sequence
        self._day_of_week = day_of_week
        self._start_time = start_time
        self._end_time = end_time
    
    def _is_discountable(self, screening: Screening):
        if self.type_ == DiscountConditionType.PERIOD:
            return self._is_satisfied_by_period(screening)
    
    def _is_satisfied_by_period(self, screening: Screening):
        return screening.when_screen.weekday() == self._day_of_week \
                and self._start_time <= screening.when_screen \
                and self._end_time >= screening.when_screen
    
    def _is_satisfied_by_sequence(self, screening: Screening):
        return self._sequence == screening.sequence


class MovieType(str, Enum):
    AMOUNT_DISCOUNT = auto()
    PECENT_DISCOUNT = auto()
    NONE_DISCOUNT = auto()


class Movie:
    def __init__(self, title, runnung_time, movie_type: MovieType, 
                 discount_amount: Money, discount_percent: float,
                 fee: Money, discount_conditions: list[DiscountCondition]):
        self._title = title
        self._running_time = runnung_time
        self._movie_type = movie_type
        self._discount_amount = discount_amount
        self._discount_percent = discount_percent
        self._fee = fee
        self._discount_conditions = discount_conditions

    @property
    def movie_type(self):
        return self._movie_type

    @movie_type.setter
    def movie_type(self, movie_type):
        self._movie_type = movie_type

    @property
    def fee(self):
        return self._fee
    
    @fee.setter
    def fee(self, fee):
        self._fee = fee

    # 나머지 인스턴스 변수들의 접근자와 수정자도 추가한다.
    # ...


class Screening:
    def __init__(self, movie: Movie, sequence: int, when_screen: time):
        self._movie = movie
        self._sequence = sequence
        self._when_screen = when_screen

    @property
    def movie(self):
        return self._movie
    
    @movie.setter
    def movie(self, movie:Movie):
        self._movie = movie

    # 나머지 인스턴스 변수들의 접근자와 수정자도 추가한다.
    # ...


class Customer:
    def __init__(self, name, id):
        self._name = name
        self._id = id

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def id_(self):
        return self._id
    
    @id_.setter
    def id_(self, id_):
        self._id = id_


class Reservation:
    def __init__(self, customer: Customer, screening: Screening, fee: Money, audience_count: int):
        self._customer = customer
        self._screening = screening
        self._fee = fee
        self._audience_count = audience_count

    @property
    def customer(self):
        return self._customer
    
    @customer.setter
    def customer(self, customer: Customer):
        self._customer = customer

    # 나머지 인스턴스 변수들의 접근자와 수정자도 추가한다.
    # ...


class ReservationAgency:
    def reserve(self, screening: Screening, customer: Customer, audience_count: int):
        discountable = self._check_discountable(screening)
        fee = self._calculate_fee(screening, discountable, audience_count)
        return self._create_reservation(screening, customer, audience_count, fee)

    def _check_discountable(self, screening: Screening):
        return any([self._is_discountable(discount_condition, screening) 
                    for discount_condition in screening.movie.discount_conditions])
    
    def _calculate_fee(self, screening: Screening, discountable: bool, audience_count: int):
        if discountable:
            return screening.movie.fee.minus()
        
    def _calculate_discount_fee(self, movie: Movie):
        match movie.movie_type:
            case MovieType.AMOUNT_DISCOUNT:
                return self._calculate_amount_discounted_fee(movie)
            case MovieType.PECENT_DISCOUNT:
                return self._calculate_percent_discounted_fee(movie)
            
        return self._calculate_none_discounted_fee(movie)
    
    def _calculate_amount_discounted_fee(self, movie: Movie):
        return movie.discount_amount

    def _calculate_percent_discounted_fee(self, movie: Movie):
        return movie.fee * movie.discount_percent
    
    def _calculate_none_discounted_fee(self, movie: Movie):
        return Money.wons(0)
    
    def _create_reservation(self, screening: Screening, customer: Customer, audience_count: int, fee: Money):
        return Reservation(customer, screening, fee, audience_count)

