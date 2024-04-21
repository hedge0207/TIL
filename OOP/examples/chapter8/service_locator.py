class ServiceLocator:
    def __init__(self):
        self._discount_policy = None

    @classmethod
    def discount_policy(self) -> DiscountPolicy:
        return self._discount_policy
    
    @classmethod
    def provide(self, discount_policy = DiscountPolicy):
        self._discount_policy = discount_policy


class Movie:
    def __init__(self, title: str, running_time: time, fee: Money):
        self._title = title
        self._running_time = running_time
        self._fee = fee
        self._discount_policy = ServiceLocator.discount_policy()
    
    # ...


ServiceLocator.provide(AmountDiscountPolicy(Money.wons(800),
                            [SequenceCondition(1), SequenceCondition(2),
                            PeriodCondition(2, datetime(2024, 3, 27, 10), datetime(2024, 3, 27, 12))]
                        ))
Movie("About Time", time(2, 3), Money.wons(10000))