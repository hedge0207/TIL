class Movie:
    def __init__(self, title: str, running_time: time, fee: Money, discount_policy: DiscountPolicy):
        self._title = title
        self._running_time = running_time
        self._fee = fee
        self._discount_policy = discount_policy

    # ...
    def calculate_movie_fee(self, screening: Screening):
        # 올바른 screening을 전달하기 위해 인자로 넘기기 전에 체크한다.
        if screening is None and screening.get_start_time() <= datetime.now():
            raise InvalidScreeningException
        return self._fee.minus(self._discount_policy.calculate_discount_amount(screening))


class DiscountPolicy(ABC):

    # ...
    def calculate_discount_amount(self, screening: Screening):
        # 사전조건
        self._check_precondition(screening)
        amount = Money.wons(0)
        for condition in self.conditions:
            if condition.is_satisfied_by(screening):
                amount = self.get_discount_amount(screening)
                # 사후조건
                self._check_postcondition(amount)
                return amount
        # 사후조건
        self._check_postcondition(amount)
        return amount
    
    # 사전조건
    def _check_precondition(self, screening: Screening):
        assert screening is not None and screening.get_start_time() > datetime.now()
    
    # 사후조건
    def _check_postcondition(self, amount: Money):
        assert amount is not None and amount.is_gte(Money.wons(0))
    

class BrokenDiscountPolicy(DiscountPolicy):

    def calculate_discount_amount(self, screening: Screeing):
        self._check_precondition()

        # ...

        self._check_weaker_postcondition()


    def _check_stronger_precondition(self, screening: Screening):
        assert (screening.get_start_time()-datetime.now()).days < 3

    def _check_stronger_postcondition(self, amount: Money):
        assert amount is not None and amount.is_gte(Money.wons(1000))

    def _check_weaker_postcondition(self, amount: Money):
        assert amount is not None