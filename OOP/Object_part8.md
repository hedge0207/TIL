# 일관성 있는 협력

## 일관성 없는 협력 구현하기

- 가능하면 유사한 기능을 구현하기 위해 유사한 협력 패턴을 사용해야 한다.
  - 객체지향의 목표는 적절한 책임을 수행하는 객체들의 협력을 기반으로 결합도가 낮고 재사용 가능한 코드 구조를 창조하는 것이다.
    - 객체지향 패러다임의 장점은 설계를 재사용할 수 있다는 것이다.
    - 재사용을 위해서는 객체들의 협력 방식을 일관성 있게 만들어야 한다.
    - 일관성은 설계와 코드를 이해하는 데 드는 비용을 절감시킨다.
  - 객체들의 협력이 전체적으로 일관성 있는 유사한 패턴을 따른다면 시스템을 이해하고 확장하기 위해 요구되는 부담을 크게 줄일 수 있다.
  - 일관성 있는 협력 패턴을 적용하면 이해하기 쉽고 직관적이며 유연한 코드를 작성할 수 있다.



- 핸드폰 과금 시스템 변경하기

  - 이전장에서 구현한 핸드폰 과금 시스템의 요금 정책을 수정해야 한다고 가정하자.
    - 기본 정책을 아래와 같이 4가지 방식으로 확장할 것이다.
    - 부가 정책에 대한 요구사항은 변경이 없다.

  - 고정요금 방식
    - 일정 시간 단위로 동일한 요금을 부과하는 방식.
    - 모든 통화에 대해 동일하게 10초에 5원을 부과하는 방식이 이에 해당한다.
  - 시간대별 방식
    - 하루 24시간을 특정한 시간 구간으로 나눈 후 각 구간별로 서로 다른 요금을 부과하는 방식.
    - 0~20시까지는 10초당 5원을, 20~24시까지는 10초당 8원을 부과하는 방식이 이에 해당한다.
  - 요일별 방식
    - 요일별로 요금을 차등 부과하는 방식이다.
    - 월요일부터 목요일까지는 10초당 5원, 금요일부터 일요일까지는 10초에 8원을 부과하는 방식이 이에 해당한다.

  - 구간별 방식
    - 전체 통화 시간을 일정한 통화 시간에 따라 나누고 각 구간별로 요금을 차증 부과하는 방식이다.
    - 예를 들어 통화 구간을 1분과 1분 이후로 나눈 후 1분 간은 10초당 5원을, 그 후에는 10초당 3원을 부과하는 방식이 이에 해당한다.



- 고정요금 방식 구현하기

  - 고정 요금 방식은 기존의 일반요금제와 동일하다.

  ```python
  class FixedFeePolicy(BasicRatePolicy):
      
      def __init__(self, amount: Money, seconds: int):
          self._amount = amount
          self._seconds = seconds
  
      def _calculate_call_fee(self, call: Call):
          return self._amount.times(call.get_duration().total_seconds() / self._seconds)
  ```



- 시간대별 방식 구현하기

  - 여러 날에 걸쳐 통화하는 경우도 있을 수 있기에 통화의 시작 시간과 종료 시간뿐 아니라 시작 일자와 종료 일자도 함께 고려해야 한다.
    - 이를 위해 기간을 편리하게 관리할 수 있는 `DateTimeInterval` 클래스를 추가한다.

  ```python
  class DateTimeInterval:
  
      def __init__(self, from_: datetime, to: datetime):
          self._from = from_
          self.to = to
      
      def of(self, from_: datetime, to: datetime):
          return DateTimeInterval(from_, to)
      
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
  ```

  - `Call` 클래스를 수정한다.
    - 기존의 `Call` 클래스는 통화의 시작 시간과 종료 시간을 계산하기 위해 `from_` 과 `to` 라는 인스턴스 변수를 포함하고 있었다.
    - `DateTimeInterval` 클래스를 추가했으므로 `from_`과 `to`를 하나의 인스턴스 변수로 묶을 수 있다.
    - 이에 맞춰 메서드들도 변경한다.

  ```python
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
  ```

  - 시간대별 방식에서 요금을 계산할 수 있는 정보 전문가를 찾는다.
    - 시간대별 방식으로 요금을 계산하기 위해서는 두 단계를 거쳐야 한다.
    - 먼저 통화 기간을 일자별로 분리하고, 그 후에 일자별로 분리된기간을 다시 시간대별 규칙에 따라 분리한 후 각 기간에 대해 요금을 계산해야한다.
    - 통화 기간을 일자별로 나누는 작업의 정보 전문가는 통화 기간에 대한 정보를 가장 잘 알고 있는 `Call`이다.
    - 그러나 `Call`은 기간 자체를 처리하는 방법에 대해서는 전문가가 아니다.
    - 기간을 처리하는 방법에 대한 전문가는 `DateTimeInterval`이다.
    - 따라서 통화 기간을 일자로 나누는 책임은 `DateTimeInterval`에게 할당하고 `Call`이 `DateTimeInterval`에게 분할을 요청하도록 설계하는 것이 적절할 것이다.
    - 두번째 작업인 시간대별로 분할하는 작업의 정보 전문가는 시간대별 기준을 알고 있는 요금 정책이며, 여기서는 `TimeOfDayDiscountPolicy`라는 클래스로 구현하 것이다.
    - 결국 정리하면 `TimeOfDayDiscountPolicy`이 통화 기간을 알고 있는 `Call`에게 일자별로 통화 기간을 분리할 것을 요청한다.
    - `Call`은 이 요청을 `DateTimeInterval`에게 위임하고, `DateTimeInterval`은 기간을 일자 단위로 분할한 후 분할된 목록을 반환한다.
    - `Call`은 반환된 목록을 그대로 `TimeOfDayDiscountPolicy`에게 반환한다.
    - `TimeOfDayDiscountPolicy`는 일자별 기간의 목록을 대상으로 루프를 돌리면서 각 시간대별 기준에 맞는 시작시간과 종료시간을 얻는다.
  - `TimeOfDayDiscountPolicy`를 구현한다.
    - 이 클래스에서 가장 중요한 것은 시간에 따라 서로 다른 요금 규칙을 정의하는 방법을 결정하는 것이다.
    - 하나의 통화 시간대를 구성하는 데는 시작 시간, 종료 시간, 단위 시간, 단위 요금이 필요하다.
    - 그리고 시간대별 방식은 하나 이상의 시간대로 구성되기 때문에 이 4가지 요소가 하나 이상 존재해야 한다.

  ```python
  class TimeOfDayDiscountPolicy(BasicRatePolicy):
      
      def __init__(self):
          self._starts: list[time] = []
          self._ends: list[time] = []
          self._durations: list[int] = []
          self._amounts: list[Money] = []
  
      def _calculate_call_fee(self, call: Call):
          result = Money.wons(0)
          # 통화일별로 순회한다.
          for interval in call.split_by_day():
              # 시작 시간, 종료 시간, 단위 시간, 단위 요금 묶음 별로 순회를 돈다.
              for i in range(len(self._starts)):
                  # 통화 시간대가 어디 속하는지 알기 위해 from_과 to를 계산한다.
                  from_ = self._from(interval, self._starts[i])
                  to = self._to(interval, self._ends[i])
                  # 총 통화시간을 초 단위로 구하기 위해 통화일의 통화 시간을 구한다.
                  delta = datetime.combine(datetime.today(), to) - datetime.combine(datetime.today(), from_)
                  result = result.plus(self._amounts[i].times(delta.seconds / self._durations[i]))
          return result
      
      def _from(self, interval: DateTimeInterval, from_: time):
          return from_ if interval.from_.time() < from_ else interval.from_.time()
      
      def _to(self, interval: DateTimeInterval, to: time):
          return to if interval.to.time() > to else interval.to.time()
  ```

  - `Call`에도 `split_by_day` 메서드를 추가한다.
    - `DateTimeInterval`에 요청을 전달한 후 응답을 반환하는 위임 메서드이다.

  ```python
  class Call:
      
      def split_by_day(self):
          return self._interval.split_by_day()
  ```

  - `DateTimeInterval`에 `split_by_day` 메서드를 추가한다.
    - 통화 기간을 일자별로 분할해서 반환하는 역할을 한다.
    - `days` 메서드는 `from_`과 `to` 사이에 포함된 날짜 수를 반환하며 만약 반환값이 1보다 크다면(여러 날에 걸쳐 있다면) `_split`을 호출하여 날짜 수만큼 분리한다.

  ```python
  class DateTimeInterval:
      # ...
      
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
  	
      # 첫째 날은 첫째날 통화 시작 시간부터 그날 자정까지의 날짜와 시간을 넣는다.
      def _add_first_day(self, result: list[DateTimeInterval]):
          result.append(self.to_midnight(self._from))
  	
      # 중간에 있는 날은 하루를 온전히 넣는다.
      def _add_middle_days(self, result: list[DateTimeInterval], days: int):
          for i in range(1, days):
              result.append(self.during(self._from + timedelta(days=i)))
      
      # 마지막 날은 자정부터 통화 종료 시간까지의 날짜와 시간을 넣는다.
      def _add_last_day(self, result: list[DateTimeInterval]):
          result.append(self.from_midnight(self._to))
  ```




- 요일별 방식 구현하기

  - 요일별 방식은 요일별로 요금을 다르게 설정할 수 있다.
    - 각 규칙은 요일의 목록, 단위 시간, 단위 요금이라는 세 가지 요소로 구성된다.
    - 시간대별 방식에서는 4개의 list를 사용하여 규칙을 정의했지만, 요일별 방식에서는 하나의 클래스로 구성하려고 한다.
    - `DayOfWeekDiscount`라는 클래스에 요일별 방식의 규칙을 구현한다.
  
  ```python
  class DayOfWeekDiscountRule:
      
      def __init__(self, day_of_week: int, duration: int, amount: Money):
          self._day_of_week = day_of_week
          self._duration = duration
          self._amount = amount
  
      def calculate(self, interval: DateTimeInterval):
          if self._day_of_week == interval.from_.weekday():
              return self._amount.times(interval.duration().seconds / self._duration)
          return Money.wons(0)
  ```
  
    - 요일별 방식 구현
      - 요일별 방식 역시 통화 기간이 여러 날에 걸쳐있을 수 있다.
      - 따라서 시간대별 방식과 동일하게 통화 기간을 날짜 경계로 분리하고 분리된 각 통화 기간을 요일별로 설정된 요금 정책에 따라 계산해야 한다.
  
  ```python
  class DayOfWeekDiscountPolicy(BasicRatePolicy):
      
      def __init__(self, rules: list[DayOfWeekDiscountRule]):
          self._rules = rules
  
      def _calculate_call_fee(self, call: Call):
          result = Money.wons(0)
          for interval in call.get_interval().split_by_day():
              for rule in self._rules:
                  result = result.plus(rule.calculate(interval))
          return result
  ```



- 구간별 방식 구현하기

  - 요일별 방식과 마찬기지로 규칙을 정의하는 새로운 클래스를 추가하는 방식으로 구현한다.
    - 요일별 방식과 다른 점은 코드를 재사용하기 위해 `FixedFeePolicy` 클래스를 상속 받는다는 것이다.
    - 단, 이는 코드 재사용을 위한 상속으로, 이해하기 어렵고 결합도가 높은 코드를 만든다.

  ```python
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
  ```

  - 구간별 방식을 구현한다.

  ```python
  class DurationDiscountPolicy(BasicRatePolicy):
  
      def __init__(self, rules: list[DurationDiscountRule]):
          self._rules = rules
      
      def _calculate_call_fee(self, call: Call):
          result = Money.wons(0)
          for rule in self._rules:
              result = result.plus(rule.calculate(call))
          return result
  ```



- 위 코드의 문제점
  - 유사한 문제를 해결하고 있음에도 설계에 일관성이 없다.
    - 기본 정책을 구현한다는 공통의 목적을 공유하지만, 정책을 구현하는 방식은 완전히 다르다.
    - 시간대별 방식에서는 규칙을 list로 관리했지만, 요일별 방식에서는 클래스로 관리했다.
    - 이 두 쿨르새는 요구사항의 관점에서는 여러 개의 규칙을 사용한다는 공통점을 공유하지만 구현 방식은 완전히 다르다.
    - 또 고정요금 방식은 오직 하나의 규칙으로만 구성되기 때문에 전혀 다른 구현 방식을 따른다.
    - 기간 요금 정책 역시 다른 정책들과 다른 방식으로 구현되어 있다.
  - 비일관성은 두 가지 상황에서 발목을 잡는다.
    - 새로운 구현을 추가해야 하는 경우.
    - 기존의 구현을 이해해야 하는 경우.
  - 유사한 기능을 서로 다른 방식으로 구현해서는 안 된다.
    - 대부분의 사람들은 유사한 요구사항을 구현하는 코드는 유사한 방식으로 구현될 것이라고 예상한다.
    - 일관성 없는 설계와 마주한 개발자는 여러 가지 해결 방법 중에서 현재의 요구사항을 해결하기에 가장 적절한 방법을 찾아야 하는 부담을 안게 된다.
    - 객체지향에서  기능을 구현하는 유일한 방법은 객체 사이의 협력을 만드는 것뿐이므로 유지보수 가능한 시스템을 구축하는 첫걸음은 협력을 일관성 있게 만드는 것이다.





## 설계에 일관성 부여하기

- 일관성 있는 설계를 만드는 방법
  - 일관성 있는 설계를 위한 조언
    - 다양한 설계 경험을 익혀라
    - 널리 알려진 디자인 패턴을 학습하고 변경이라는 문맥 안에서 디자인 패턴을 적용해보라.
  - 설계를 일관성 있게 만들기 위한 지침
    - 협력을 일관성 있게 만들기 위한 지침을 따르면 된다.
    - 즉, 변하는 개념을 변하지 않는 개념으로부터 분리하고, 변하는 개념을 캡슐화해야 한다.



- 조건 로직 대 객체 탐색

  - 절차지향 프로그램에서 변경을 처리하는 전통적인 방법은 조건문의 분기를 추가하거나 개별 분기 로직을 수정하는 것이다.
    - 아래 코드에는 두 개의 조건 로직이 존재한다.
    - 하나는 할인 조건의 종류를 결정하는 부분이고, 다른 하나는 할인 정책을 결정하는 부분이다.
    - 이 설계가 나쁜 이유는 변경의 주기가 서로 다른 코드가 한 클래스 안에 뭉쳐있기 때문이다.
    - 또한 새로운 할인 정책이나 할인 조건을 추가하기 위해서는 기존 코드의 내부를 수정해야 하기에 오류가 발생할 확률이 높아진다.

  ```python
  class ReservationAgency:
      def reserve(self, screening: Screening, customer: Customer, audience_count: int):
          movie = screening.movie
  
          discountable = False
          for condition in movie.discount_conditions
          	# 조건 로직1
              if condition.type_ == DiscountConditionType.PERIOD:
                  discountable = screening.when_screen.weekday() == condition.day_of_week \
                                  and condition.start_time <= screening.when_screen \
                                  and condition.end_time >= screening.when_screen
              else:
                  discountable = condition.sequence == screening.sequence
  
              if discountable:
                  break
  
          if discountable:
              discount_amount = Money.wons(0)
  			
              # 조건 로직2
              match movie.movie_type:
                  case MovieType.AMOUNT_DISCOUNT:
                      discount_amount = movie.discount_amount
                  case MovieType.PECENT_DISCOUNT:
                      discount_amount = movie.fee * movie.discount_percent
              
              fee = movie.fee.minus(discount_amount)
          else:
              fee = movie.fee
          
          return Reservation(customer, screening, fee, audience_count)
  ```

  - 객체지향에서 변경을 처리하는 전통적인 방법은 조건 로직을 객체 사이의 이동으로 바꾸는 것이다.
    - 아래 코드를 보면 `Movie`는 현재의 할인 정책이 어떤 종류인지 확인하지 않는다.
    - 단순히 현재의 할인 정책을 나타내는 `_discount_policy`에게 필요한 메시지를 전송할 뿐이다.
    - 할인 정책의 종류를 체크하던 조건문이 `_discount_policy`로의 객체 이동으로 대체된 것이다.
    - 다형성은 바로 이런 조건 로직을 객체 사이의 이동으로 바꾸기 위해 객체지향이 제공하는 설계 기법이다.
    - `DiscountPolicy`와 `DiscountCondition` 사이의 협력 역시 마찬가지다.
    - 객체지향적인 코드는 조건을 판단하지 않는다.
    - 단지 다음 객체로 이동할 뿐이다.

  ```python
  class Movie:
      # ...
  
      def calculate_movie_fee(self, screening: Screening):
          return self._fee.minus(self._discount_policy.calculate_discount_amount(screening))
      
      
  class DiscountPolicy(ABC):
      # ...
  
      def calculate_discount_amount(self, screening: Screening):
          for condition in self.conditions:
              if condition.is_satisfied_by(screening):
                  return self.get_discount_amount(screening)
          return Money.wons(0)
  ```

  - 지금까지 살펴본 것처럼 조건 로직을 객체 사이의 이동으로 대체하기 위해서는 커다란 클래스를 더 작은 클래스들로 분리해야 한다.
    - 클래스를 분리할 때 고려해야 할 가장 중요한 기준은 변경의 이유와 주기다.
    - 클래스는 명확히 단 하나의 이유에 의해서만 변경되어야 하고, 클래스 안의 모든 코드는 함께 변경되어야 한다.
    - 간단히 말해서 SRP를 따르도록 클래스를 분리해야 한다는 것이다.
  - 큰 메서드 안에 뭉쳐있던 조건 로직들을 변경의 압력에 맞춰 작은 클래스들로 분리하고 나면 인스턴스들 사이의 협력 패턴에 일관성을 부여하기가 더 쉬워진다.
    - 유사한 행동을 수행하는 작은 클래스들이 자연스럽게 역할이라는 추상화로 묶이게 되고 역할 사이에서 이뤄지는 협력 방식이 전체 설계의 일관성을 유지할 수 있게 이끌어주기 때문이다.
    - `Movie`와 `DiscountPolicy`, `DiscountCondition` 사이의 협력 패턴은 변경을 기준으로 클래스를 분리함으로써 어떻게 일관성 있는 협력을 얻을 수 있는지를 잘 보여준다.
    - 이 협력 패턴은 말 그대로 일관성이 있기 때문에 이해하기 쉽다.
  - 변하지 않는 개념으로부터 분리하라.
    - 할인 정책과 할인 조건의 타입을 체크하는 하나하나의 조건문이 개별적인 변경이었다.
    - 각 조건문을 개별적인 객체로 분리했고 이 객체들과 일관성 있게 협력하기 위해 타입 계층을 구성했다.
    - 그리고 이 타입 계층을 클라이언트로부터 분리하기 위해 역할을 도입했다.
    - 결과적으로 변하는 개념을 서브타입으로 분리한 후 이 서브타입들을 클라이언트로부터 캡슐화한 것이다.
  - 변하는 개념을 캡슐화하라
    - `Movie`로부터 할인 정책을 분리한 후 추상 클래스인 `DiscountPolicy`를 부모로 삼아 상속 계층을 구성한 이유가 바로 `Movie`로부터 구체적인 할인 정책들을 캡슐화하기 위해서다.
    - 실행 시점에 `Movie`는 자신과 협력하는 객체의 구체적인 타입에 대해 알지 못한다.
    - `Movie`가 알고 있는 사실은 협력하는 객체가 단지 `calculate_discount_amount` 메시지를 이해할 수 있다는 것 뿐이다.
    - 메시지 수진자의 타입은 `Movie`에 대해 완벽하게 캡슐화된다.
    - 핵심은 훌륭한 추상화를 찾아 추상화에 의존하도록 만드는 것이다.



- 캡슐화 다시 살펴보기
  - 캡슐화는 데이터 은닉 이상이다.
    - 많은 사람들이 캡슐화에 관한 이야기를 들으면 반사적으로 데이터 은닉을 떠올린다.
    - 데이터 은닉이란 오직 외부에 공개된 메서드를 통해서만 객체의 내부에 접근할 수 있게 제한함으로써 객체 내부의 상태 구현을 숨기는 기법을 가리킨다.
    - 간단하게 말해서 클래스의 모든 인스턴스 변수는 private으로 선언해야 하고 오직 해당 클래스의 메서드만이 인스턴스 변수에 접근할 수 있어야 한다는 것이다.
    - 그러나 캡슐화란 단순히 데이터를 감추는 것이 아니다.
    - 소프트웨어 안에서 변할 수 있는 모든 "개념"을 감추는 것이다.
    - 즉, 캡슐화란 변하는 어떤 것이든 감추는 것이다.
  - 설계라는 맥락에서 캡슐화를 논의할 때는 그 안에 항상 변경이라는 주제가 녹아 있다.
    - 캡슐화의 가장 대표적인 예는 객체의 퍼블릭 인터페이스와 구현을 분리하는 것이다.
    - 자주 변경되는 내부 구현을 안정적인 퍼블릭 인터페이스 뒤로 숨겨야 한다.
  - 데이터 캡슐화
    - 클래스 내부에서 관리하는 데이터를 캡슐화하는 것을 말한다.
    - 각 객체는 private 인스턴스 변수를 가지고 있다.
  - 메서드 캡슐화
    - 클래스 내부의 행동을 캡슐화하는 것을 말한다.
    - 각 객체는 외부에서 접근해선 안 되고 내부에서만 접근할 수 있는 메서드들을 가지고 있다.
  - 객체 캡슐화
    - 객체와 객체 사이의 관계를 캡슐화하는 것을 말한다.
    - `Movie` 클래스는 `DiscountPolicy` 타입의 인스턴스 변수 `_discount_policy`를 포함하는데, 이 인스턴스 변수는 private 가시성을 가지기에 `Movie`와 `DiscountPolicy` 사이의 관계를 변경하더라도 외부에는 영향을 미치지 않는다.
    - 객체 캡슐화는 합성을 의미한다.
  - 서브타입 캡슐화
    - `Movie`는 `DiscountPolicy`대해서는 알고 있지만 `DiscountPolicy`의 서브 타입인 `AmountDiscountPolicy` 등에 대해서은 알지 못한다.
    - 그러나 실행 시점에는 해당 클래스들의 인스턴스와도 협력할 수 있다.
    - 이는 기반 클래스인 `DiscountPolicy`와의 추상적인 관계가 `AmountDiscountPolicy` 등의 존재를 감추고 있기 때문이다.
    - 서브타입 캡슐화가 다형성의 기반이 된다.
  - 일반적으로 협력을 일관성 있게 만들기 위해서는 서브타입 캡슐화와 객체 캡슐화를 조합한다.
    - 서브타입 캡슐화와 객체 캡슐화를 적용하는 방법은 아래와 같다.
  - 변하는 부분을 분리하여 타입 계층을 만든다.
    - 즉, 변하지 않는 부분으로부터 변하는 부분을 분리한다. 
    - 변하는 부분들의 공통적인 행동을 추상 클래스나 인터페이스로 추상화하고, 변하는 부분들이 이 추상 클래스나 인터페이스를 상속받게 만든다.
  - 변하지 않는 부분의 일부로 타입 계층을 합성한다.
    - 변하는 부분을 분리하여 만든 타입 계층(추상 클래스, 인터페이스)을 변하지 않는 부분에 합성한다.
    - 변하지 않는 부분에서는 구체적인 사항에 결합돼서는 안된다.
    - 의존성 주입과 같이 결합도를 느슨하게 유지할 수 있는 방법을 이용해 오직 추상화에만 의존하게 만든다.
    - 이제 변하지 않는 부분은 변하는 부분의 구체적인 종류에 대해서는 알지 못한다.
    - 즉 변경이 캡슐화된 것이다.





## 일관성 있는 협력 구현하기

- 변경 분리하기
  - 일관성 있는 협력을 만들기 위한 첫 번째 단계는 변하는 부분과 변화하지 않는 개념을 분리하는 것이다.
  - 변하지 않는 부분 알아내기
    - 핸드폰 과금 시스템의 기본 정책에서 변하지 않는 부분을 살펴보기 위해 각 정책이 공유하는 부분을 살펴볼 것이다.
    - 고정요금 정책을 제외한 세 정책의 공통점은 과금을 위한 "규칙"을 가지고 있다는 것이다.
    - 기본 정책은 하나 이상의 규칙으로 구성되며, 하나의 규칙은 적용 조건과 단위 요금의 조합으로 이루어진다는 점은 세 정책 모두 동일하다.
    - 즉, 세 정책 모두 하나 이상의 규칙들의 집합이라는 공통점이 있다.
  - 변하는 부분 알아내기
    - 각 요금 정책의 차이를 통해 변하는 부분을 알아낼 수 있다.
    - 고정요금 정책을 제외한 세 정책은 요금을 계산하는 적용 조건의 형식이 다르다는 점이다.
    - 모든 규칙에 적용 조건이 포함된다는 사실은 변하지 않지만(공통점을 가지지만)실제 조건의 세부적인 내용은 다르다.
  - 변하지 않는 "규칙"으로부터 변하는 적용 조건을 분리해야한다.



- 변경 캡슐화하기

  - 변경을 캡슐화하는 가장 좋은 방법은 변하지 않는 부분으로부터 변하는 부분을 분리하는 것이다.
    - 예시에서 변하지 않는 것은 규칙이며, 변하는 것은 적용 조건이다.
    - 따라서 규칙으로부터 적용 조건을 분리해서 적용 조건을 추상화한 후 각 방식을 이 추상화의 서브타입으로 만들 것이다.
    - 이것이 서브타입 캡슐화다.
    - 그 후에 규칙이 적용 조건을 표현하는 추상화를 합성 관계로 연결한다.
    - 이것이 객체 캡슐화다.
  - 아래 코드는 규칙을 구성하는 데 필요한 클래스들의 관계를 나타낸 것이다.
    - `FeeRule`은 규칙을 구현하는 클래스이다.
    - `FeeCondition`은 적용 조건을 구현하는 인터페이스이며 변하는 부분을 캡슐화하는 추상화다.
    - 각 기본 정책별로 달라지는 부분은 각각의 서브타입으로 구현된다.
    - `FeeRule`이 `FeeCondition`을 함성 관계로 연결하고 있다는 점도 주목해야 한다.
    - `FeeRule`이 오직 `FeeCondition`에만 의존하고 있다는 점도 주목해야 한다.
    - `FeeRule`은 `FeeCondition`의 어떠한 서브타입도 알지 못하므로, 변하는 `FeeCondition`의 서브타입은 변하지 않는 `FeeRule`로부터 캡슐화된다.

  ```python
  class FeeCondition:
      ...
      
  class TimeOfDayFeeCondition(FeeCondition):
      ...
      
  class DayOfWeekFeeCondition(FeeCondition):
      ...
      
  class DurationFeeCondition(FeeCondition):
      ...
  
  class FeeRule:
      def __init__(self, fee_per_duration, fee_condition: FeeCondition):
          self._fee_per_duration=fee_per_duration
          self._fee_condition = fee_condition
  
  class BasicRatePolicy:
      def __init__(self, fee_rule: FeeRule):
          self._fee_rule = fee_rule
  ```

  - 정리
    - 위 코드는 변하지 않는 부분으로부터 변하는 부분을 효과적으로 분리한다.
    - 변하지 않는 부분은 기본 정책이 여러 규칙들의 집합이며, 하나의 규칙은 적용 조건과 단위 요금으로 구성된다는 것이다.
    - 이 관계는 `BasicRatePolicy`, `FeeRule`, `FeeCondition`의 조합으로 구현된다.
    - 변하는 부분은 적용 조건의 세부적인 내용이다.
    - 이것은 `FeeCondition`의 서브타입인 `TimeOfDayFeeCondition`, `DayOfWeekFeeCondition`, `DurationFeeCondition`으로 구현된다.
    - 그리고 `FeeRule`은 추상화인 `FeeCondition`에 대해서만 의존하기 때문에 적용 조건이 변하더라도 영향을 받지 않는다.
    - 즉, 적용 조건이라는 변경에 대해 캡슐화되어 있다.



- 협력 패턴 설계하기

  - 변하는 부분과 변하지 않는 부분을 분리하고, 변하는 부분을 적절히 추상화하고 나면 변하는 부분을 생략한 채 변하지 않는 부분만을 이용해 객체 사이의 협력을 이야기할 수 있다.
    - 추상화만으로 구성한 협력은 추상화를 구체적인 사례로 대체함으로써 다양한 상황으로 확장할 수 있게 된다,
    - 다시 말해서 재사용 가능한 협력 패턴이 선명히 드러나는 것이다.
    - 위 코드에서 변하지 않는 부분만 남기면 아래와 같다.

  ```python
  class BasicRatePolicy:
      def __init__(self, fee_rules: list[FeeRule]):
          self._fee_rules = fee_rules
      
  class FeeRule:
      def __init__(self, fee_condition: FeeCondition):
          self._fee_condition = fee_condition
       
  class FeeCondition:
      ...
  ```

  - 추상화들이 참여하는 협력
    - 추상화인 `BasicRatePolicy`, `FeeRule`, `FeeCondition`가 참여하는 협력은 아래와 같다.
    - `BasicRatePolicy`가 `calculate_fee` 메시지를 수신했을 때 협력이 시작된다.
    - `BasicRatePolicy.calculate_fee` 메서드는 인자로 전달 받은 통화 목록(`list[Call]`)의 전체 요금을 계산한다.
    - `BasicRatePolicy`는 목록에 포함된 각 `Call` 별로 `FeeRule`의 `calculate_fee` 메서드를 실행한다.
    - 하나의 `BasicRatePolicy`는 하나 이상의 `FeeRule`로 구성되기 때문에 `Call` 하나당 `FeeRule`에 다수의 `calculate_fee` 메시지가 전송된다.
    - ``FeeRule``는 하나의 `Call`에 대해 요금을 계산하는 책임을 수행한다.
    - 하나의 `Call` 요금을 계산하기 위해서는 두 개의 작업이 필요하다.
    - 하나는 전체 통화 시간을 각 "규칙"의 "적용 조건"을 만족하는 구간들로 나누는 것이다.
    - 다른 하나는 분리된 통화 구간에 단위 요금을 적용해서 요금을 계산하는 것이다.
    - 객체지향에서는 모든 작업을 객체의 책임으로 생각하기에, 이 두 개의 책임을 객체에게 할당할 것이다.
    - 전체 통화 시간을 각 "규칙"의 "적용 조건"을 만족하는 구간들로 나누는 작업은 적용 조건을 가장 잘 알고 있는 정보 전문가인 `FeeCondition`에게 할당하는 것이 적절할 것이다.
    - 이렇게 분리된 통화 구간에 단위 요금을 계산하는 두 번째 작엄은 요금 기준 정보 전문가인 `FeeRule`이 담당하는 것이 적절할 것이다.
    - 협력에 `FeeCondition`가 참여하고 있다는 것에 주목해야한다.
    - 실제 협력이 수행될 때는 `FeeCondition`의 서브타입이 자리를 대신할 것이다.


