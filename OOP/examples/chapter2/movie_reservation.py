from __future__ import annotations
from abc import abstractmethod, ABC
from datetime import datetime, time
from typing_extensions import Self


class Customer:
    ...


class Screening:
    def __init__(self, movie: Movie, sequence: int, when_screened: datetime):
        self._movie = movie
        self._sequence = sequence
        self._when_screened = when_screened

    def get_start_time(self):
        return self._when_screened

    def is_sequence(self, sequence: int):
        return self._sequence == sequence

    def get_movie_fee(self):
        return self._movie.get_fee()

    def _calculate_fee(self, audience_count: int):
        return self._movie.calculate_movie_fee(self).times(audience_count)

    def reserve(self, customer: Customer, audience_count: int):
        return Reservation(customer, self, self.calculate_fee(audience_count), audience_count)


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
    def __init__(self, customer: Customer, screening: Screening, fee: Money, audience_count: int):
        self.customer = customer
        self.screening = screening
        self.fee = fee
        self.audience_count = audience_count


class Movie:
    def __init__(self, title: str, running_time: time, fee: Money, discount_policy: DiscountPolicy):
        self._title = title
        self._running_time = running_time
        self._fee = fee
        self._discount_policy = discount_policy

    def get_fee(self) -> Money:
        return self._fee

    def calculate_movie_fee(self, screening: Screening):
        return self._fee.minus(self._discount_policy.calculate_discount_amount(screening))


class DiscountCondition(ABC):
    @abstractmethod
    def is_satisfied_by(self, screening: Screening) -> bool:
        ...


class SequenceCondition(DiscountCondition):
    def __init__(self, sequence: int):
        self._sequence = sequence

    def is_satisfied_by(self, screening: Screening) -> bool:
        return screening.is_sequence(self._sequence)


class PeriodCondition(DiscountCondition):
    def __init__(self, day_of_week: int, start_time: time, end_time: time):
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time

    def is_satisfied_by(self, screening: Screening) -> bool:
        return screening.get_start_time().weekday() == self.day_of_week and \
               self.start_time <= screening.get_start_time() and \
               self.end_time >= screening.get_start_time()


class DiscountPolicy(ABC):

    def __init__(self, conditions: list[DiscountCondition]):
        self.conditions = conditions

    @abstractmethod
    def get_discount_amount(self, screening: Screening) -> Money:
        ...

    def calculate_discount_amount(self, screening: Screening):
        for condition in self.conditions:
            if condition.is_satisfied_by(screening):
                return self.get_discount_amount(screening)

        return Money.wons(0)


class AmountDiscountPolicy(DiscountPolicy):

    def __init__(self, discount_amount: Money, conditions: list[DiscountCondition]):
        super().__init__(conditions)
        self.discount_amount = discount_amount

    def get_discount_amount(self, screening: Screening) -> Money:
        return self.discount_amount


class PercentDiscountPolicy(DiscountPolicy):

    def __init__(self, percent: float, conditions: list[DiscountCondition]):
        super().__init__(conditions)
        self.percent = percent

    def get_discount_amount(self, screening: Screening) -> Money:
        return screening.get_movie_fee().times(self.percent)


class NoneDiscountPolicy(DiscountPolicy):
    
    def calculate_discount_amount(self, screening: Screening) -> Money:
        return Money.wons(0)

if __name__ == "__main__":
    movie = Movie("About Time",
                  time(2, 3),
                  Money.wons(10000),
                  AmountDiscountPolicy(Money.wons(800),
                                       [SequenceCondition(1), SequenceCondition(2),
                                        PeriodCondition(2, datetime(2024, 3, 27, 10), datetime(2024, 3, 27, 12))]
                                       ))
    
    screening = Screening(movie, 8, datetime(2024, 3, 27, 10))
    print(movie.calculate_movie_fee(screening)._amount)
