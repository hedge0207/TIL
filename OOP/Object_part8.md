# 일관성 있는 협력

## 일관성 없는 협력 구현하기

- **가능하면 유사한 기능을 구현하기 위해 유사한 협력 패턴을 사용해야 한다.**
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
  - **유사한 문제를 해결하고 있음에도 설계에 일관성이 없다.**
    - 기본 정책을 구현한다는 공통의 목적을 공유하지만, 정책을 구현하는 방식은 완전히 다르다.
    - 시간대별 방식에서는 규칙을 list로 관리했지만, 요일별 방식에서는 클래스로 관리했다.
    - 이 두 클래스는 요구사항의 관점에서는 여러 개의 규칙을 사용한다는 공통점을 공유하지만 구현 방식은 완전히 다르다.
    - 또 고정요금 방식은 오직 하나의 규칙으로만 구성되기 때문에 전혀 다른 구현 방식을 따른다.
    - 기간 요금 정책 역시 다른 정책들과 다른 방식으로 구현되어 있다.
  - 비일관성은 두 가지 상황에서 발목을 잡는다.
    - 새로운 구현을 추가해야 하는 경우.
    - 기존의 구현을 이해해야 하는 경우.
  - **유사한 기능을 서로 다른 방식으로 구현해서는 안 된다.**
    - 대부분의 사람들은 유사한 요구사항을 구현하는 코드는 유사한 방식으로 구현될 것이라고 예상한다.
    - 일관성 없는 설계와 마주한 개발자는 여러 가지 해결 방법 중에서 현재의 요구사항을 해결하기에 가장 적절한 방법을 찾아야 하는 부담을 안게 된다.
    - 객체지향에서  기능을 구현하는 유일한 방법은 객체 사이의 협력을 만드는 것뿐이므로 유지보수 가능한 시스템을 구축하는 첫걸음은 협력을 일관성 있게 만드는 것이다.





## 설계에 일관성 부여하기

- 일관성 있는 설계를 만드는 방법
  - 일관성 있는 설계를 위한 조언
    - 다양한 설계 경험을 익혀라
    - 널리 알려진 디자인 패턴을 학습하고 변경이라는 문맥 안에서 디자인 패턴을 적용해보라.
  - **설계를 일관성 있게 만들기 위한 지침**
    - 협력을 일관성 있게 만들기 위한 지침을 따르면 된다.
    - 즉, **변하는 개념을 변하지 않는 개념으로부터 분리하고, 변하는 개념을 캡슐화해야 한다.**



- 조건 로직 대 객체 탐색

  - 절차지향 프로그램에서 변경을 처리하는 전통적인 방법은 조건문의 분기를 추가하거나 개별 분기 로직을 수정하는 것이다.
    - 아래 코드에는 두 개의 조건 로직이 존재한다.
    - 하나는 할인 조건의 종류를 결정하는 부분이고, 다른 하나는 할인 정책을 결정하는 부분이다.
    - **이 설계가 나쁜 이유는 변경의 주기가 서로 다른 코드가 한 클래스 안에 뭉쳐있기 때문이다.**
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

  - **객체지향에서 변경을 처리하는 전통적인 방법은 조건 로직을 객체 사이의 이동으로 바꾸는 것이다.**
    - 아래 코드를 보면 `Movie`는 현재의 할인 정책이 어떤 종류인지 확인하지 않는다.
    - 단순히 현재의 할인 정책을 나타내는 `_discount_policy`에게 필요한 메시지를 전송할 뿐이다.
    - 할인 정책의 종류를 체크하던 조건문이 `_discount_policy`로의 객체 이동으로 대체된 것이다.
    - 다형성은 바로 이런 조건 로직을 객체 사이의 이동으로 바꾸기 위해 객체지향이 제공하는 설계 기법이다.
    - `DiscountPolicy`와 `DiscountCondition` 사이의 협력 역시 마찬가지다.
    - **객체지향적인 코드는 조건을 판단하지 않는다. 단지 다음 객체로 이동할 뿐이다.**
  
  ```python
  class Movie:
      # ...
  
      def calculate_movie_fee(self, screening: Screening):
          return self._fee.minus(self._discount_policy.calculate_discount_amount(screening))
  
  
  class DiscountPolicy(ABC):
      def __init__(self, conditions: list[DiscountCondition]):
          self._conditions = conditions
  
      def calculate_discount_amount(self, screening: Screening):
          for condition in self._conditions:
              if condition.is_satisfied_by(screening):
                  return self.get_discount_amount(screening)
          return Money.wons(0)
  ```

  - 지금까지 살펴본 것처럼 **조건 로직을 객체 사이의 이동으로 대체하기 위해서는 커다란 클래스를 더 작은 클래스들로 분리해야 한다.**
    - **클래스를 분리할 때 고려해야 할 가장 중요한 기준은 변경의 이유와 주기다.**
    - 클래스는 명확히 단 하나의 이유에 의해서만 변경되어야 하고, 클래스 안의 모든 코드는 함께 변경되어야 한다.
    - **간단히 말해서 SRP를 따르도록 클래스를 분리해야 한다는 것이다.**
  - 큰 메서드 안에 뭉쳐있던 조건 로직들을 변경의 압력에 맞춰 작은 클래스들로 분리하고 나면 인스턴스들 사이의 협력 패턴에 일관성을 부여하기가 더 쉬워진다.
    - 유사한 행동을 수행하는 작은 클래스들이 자연스럽게 역할이라는 추상화로 묶이게 되고 역할 사이에서 이뤄지는 협력 방식이 전체 설계의 일관성을 유지할 수 있게 이끌어주기 때문이다.
    - `Movie`와 `DiscountPolicy`, `DiscountCondition` 사이의 협력 패턴은 변경을 기준으로 클래스를 분리함으로써 어떻게 일관성 있는 협력을 얻을 수 있는지를 잘 보여준다.
    - 이 협력 패턴은 말 그대로 일관성이 있기 때문에 이해하기 쉽다.
  - **변하지 않는 개념으로부터 분리하라.**
    - 할인 정책과 할인 조건의 타입을 체크하는 각각의 조건문이 개별적인 변경이었다.
    - 각 조건문을 개별적인 객체로 분리했고 이 객체들과 일관성 있게 협력하기 위해 타입 계층을 구성했다.
    - 그리고 이 타입 계층을 클라이언트로부터 분리하기 위해 역할을 도입했다.
    - 결과적으로 변하는 개념을 서브타입으로 분리한 후 이 서브타입들을 클라이언트로부터 캡슐화한 것이다.
  - **변하는 개념을 캡슐화하라**
    - `Movie`로부터 할인 정책을 분리한 후 추상 클래스인 `DiscountPolicy`를 부모로 삼아 상속 계층을 구성한 이유가 바로 `Movie`로부터 구체적인 할인 정책들을 캡슐화하기 위해서다.
    - 실행 시점에 `Movie`는 자신과 협력하는 객체의 구체적인 타입에 대해 알지 못한다.
    - `Movie`가 알고 있는 사실은 협력하는 객체가 단지 `calculate_discount_amount` 메시지를 이해할 수 있다는 것 뿐이다.
    - **메시지 수진자의 타입은 `Movie`에 대해 완벽하게 캡슐화된다.**
    - **핵심은 훌륭한 추상화를 찾아 추상화에 의존하도록 만드는 것이다.**



- 캡슐화 다시 살펴보기
  - **캡슐화는 데이터 은닉 이상이다.**
    - 많은 사람들이 캡슐화에 관한 이야기를 들으면 반사적으로 데이터 은닉을 떠올린다.
    - 데이터 은닉이란 오직 외부에 공개된 메서드를 통해서만 객체의 내부에 접근할 수 있게 제한함으로써 객체 내부의 상태 구현을 숨기는 기법을 가리킨다.
    - 간단하게 말해서 클래스의 모든 인스턴스 변수는 private으로 선언해야 하고 오직 해당 클래스의 메서드만이 인스턴스 변수에 접근할 수 있어야 한다는 것이다.
    - 그러나 캡슐화란 단순히 데이터를 감추는 것이 아니다.
    - 소프트웨어 안에서 변할 수 있는 모든 "개념"을 감추는 것이다.
    - 즉, **캡슐화란 변하는 어떤 것이든 감추는 것이다.**
  - 설계라는 맥락에서 캡슐화를 논의할 때는 그 안에 항상 변경이라는 주제가 녹아 있다.
    - 캡슐화의 가장 대표적인 예는 객체의 퍼블릭 인터페이스와 구현을 분리하는 것이다.
    - 자주 변경되는 내부 구현을 안정적인 퍼블릭 인터페이스 뒤로 숨겨야 한다.
  - **데이터 캡슐화**
    - 클래스 내부에서 관리하는 데이터를 캡슐화하는 것을 말한다.
    - 각 객체는 private 인스턴스 변수를 가지고 있다.
  - **메서드 캡슐화**
    - 클래스 내부의 행동을 캡슐화하는 것을 말한다.
    - 각 객체는 외부에서 접근해선 안 되고 내부에서만 접근할 수 있는 메서드들을 가지고 있다.
  - **객체 캡슐화**
    - 객체와 객체 사이의 관계를 캡슐화하는 것을 말한다.
    - `Movie` 클래스는 `DiscountPolicy` 타입의 인스턴스 변수 `_discount_policy`를 포함하는데, 이 인스턴스 변수는 private 가시성을 가지기에 `Movie`와 `DiscountPolicy` 사이의 관계를 변경하더라도 외부에는 영향을 미치지 않는다.
    - **객체 캡슐화는 합성을 의미한다.**
  - **서브타입 캡슐화**
    - `Movie`는 `DiscountPolicy`대해서는 알고 있지만 `DiscountPolicy`의 서브 타입인 `AmountDiscountPolicy` 등에 대해서는 알지 못한다.
    - 그러나 실행 시점에는 해당 클래스들의 인스턴스와도 협력할 수 있다.
    - 이는 기반 클래스인 `DiscountPolicy`와의 추상적인 관계가 `AmountDiscountPolicy` 등의 존재를 감추고 있기 때문이다.
    - **서브타입 캡슐화가 다형성의 기반이 된다.**

  - 일반적으로 협력을 일관성 있게 만들기 위해서는 서브타입 캡슐화와 객체 캡슐화를 조합한다.



- 서브타입 캡슐화와 객체 캡슐화를 적용하는 방법은 아래와 같다.
  - 먼저 변하는 부분을 분리하여 타입 계층을 만든다.
    - 즉, 변하지 않는 부분으로부터 변하는 부분을 분리한다. 
    - 변하는 부분들의 공통적인 행동을 추상 클래스나 인터페이스로 추상화하고, 변하는 부분들이 이 추상 클래스나 인터페이스를 상속받게 만든다.
  - 다음으로 변하지 않는 부분의 일부로 타입 계층을 합성한다.
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

  - **변경을 캡슐화하는 가장 좋은 방법은 변하지 않는 부분으로부터 변하는 부분을 분리하는 것이다.**
    - 예시에서 변하지 않는 것은 규칙이며, 변하는 것은 적용 조건이다.
    - 따라서 규칙으로부터 적용 조건을 분리해서 적용 조건을 추상화한 후 각 방식을 이 추상화의 서브타입으로 만들 것이다.
    - 이것이 서브타입 캡슐화다.
    - 그 후에 규칙이 적용 조건을 표현하는 추상화를 합성 관계로 연결한다.
    - 이것이 객체 캡슐화다.
  - 아래 코드는 규칙을 구성하는 데 필요한 클래스들의 관계를 나타낸 것이다.
    - `FeeRule`은 규칙을 구현하는 클래스이다.
    - `FeeCondition`은 적용 조건을 구현하는 인터페이스이며 변하는 부분을 캡슐화하는 추상화다.
    - 각 기본 정책별로 달라지는 부분은 각각의 서브타입으로 구현된다.
    - `FeeRule`이 `FeeCondition`을 합성 관계로 연결하고 있다는 점도 주목해야 한다(객체 캡슐화).
    - `FeeRule`이 오직 `FeeCondition`에만 의존하고 있다는 점도 주목해야 한다.
    - `FeeRule`은 `FeeCondition`의 어떠한 서브타입도 알지 못하므로, 변하는 `FeeCondition`의 서브타입은 변하지 않는 `FeeRule`로부터 캡슐화된다(서브타입 캡슐화).

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
          self._fee_per_duration = fee_per_duration
          # 합성
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

  - **변하는 부분과 변하지 않는 부분을 분리하고, 변하는 부분을 적절히 추상화하고 나면 변하는 부분을 생략한 채 변하지 않는 부분만을 이용해 객체 사이의 협력을 이야기할 수 있다.**
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
    - `FeeRule`은 하나의 `Call`에 대해 요금을 계산하는 책임을 수행한다.
    - 하나의 `Call` 요금을 계산하기 위해서는 두 개의 작업이 필요하다.
    - 하나는 전체 통화 시간을 각 "규칙"의 "적용 조건"을 만족하는 구간들로 나누는 것이다.
    - 다른 하나는 분리된 통화 구간에 단위 요금을 적용해서 요금을 계산하는 것이다.
    - 객체지향에서는 모든 작업을 객체의 책임으로 생각하기에, 이 두 개의 책임을 객체에게 할당할 것이다.
    - 전체 통화 시간을 각 "규칙"의 "적용 조건"을 만족하는 구간들로 나누는 작업은 적용 조건을 가장 잘 알고 있는 정보 전문가인 `FeeCondition`에게 할당하는 것이 적절할 것이다.
    - 이렇게 분리된 통화 구간에 단위 요금을 계산하는 두 번째 작엄은 요금 기준 정보 전문가인 `FeeRule`이 담당하는 것이 적절할 것이다.
    - 협력에 `FeeCondition`가 참여하고 있다는 것에 주목해야한다.
    - 실제 협력이 수행될 때는 `FeeCondition`의 서브타입이 자리를 대신할 것이다.



- 추상화 수준에서 협력 패턴 구현하기

  - 먼저 적용 조건을 표현하는 추상화인 `FeeCondition`에서 시작한다.
    - `find_time_intervals`이라는 하나의 오퍼레이션을 포함하는 인터페이스로 구현한다.
    - `find_time_intervals`는 인자로 받은 `Call`의 통화 기간 중에서 적용 조건을 만족하는 기간을 구한 후 배열에 담아 반환한다.

  ```python
  class FeeCondition(ABC):
  
      def find_time_intervals(self, call: Call):
          ...
  ```

  - 다음으로 규칙을 표현하는 `FeeRule`을 구현한다.
    - 단위 요금과 적용 조건을 저장하는 두 개의 인스턴스 변수로 구성된다.
    - `calculate_fee` 메서드는 `FeeCondition`에게 `find_time_intervals` 메시지를 전송해서 조건을 만족하는 시간의 목록을 받아온 후 요금을 계산한다.

  ```python
  class FeeRule:
       
      def __init__(self, fee_condition: FeeCondition, fee_per_duration: FeePerduration):
           self._fee_condition = fee_condition
           self._fee_per_duration = fee_per_duration
      
      def calculate_fee(self, call: Call):
          reduce(lambda acc, val: acc + val, 
                 map(lambda duration: self._fee_per_duration.calculate(duration), 
                     self._fee_condition.find_time_intervals(call)), 
                 Money.wons(0))
  ```

  - `FeePerduration` 클래스를 구현한다.
    - "단위 시간당 요금"이라는 개념을 표현하기 위한 클래스로 이 정보를 이용해 일정 기간 동안의 요금을 계산한는 `calculate` 메서드를 구현한다.

  ```python
  class FeePerduration:
  
      def __init__(self, fee: Money, duration: int):
          self._fee = fee
          self._duration = duration
      
      def calculate(self, interval: DateTimeInterval):
          return self._fee.times(round(interval.duration().seconds / self._duration))
  ```

  - `BasicPolicy`가 `FeeRule`의 집합을 사용하여 전체 통화 요금을 계산하도록 수정한다.

  ```python
  class BasicRatePolicy(RatePolicy):
  
      def __init__(self, fee_rules: List[FeeRule]):
          self._fee_rules = fee_rules
  
      def calculate_fee(self, phone: Phone):
          return [self._calculate(call) for call in phone.calls]
      
      def _calculate(self, call: Call):
          return reduce(lambda acc, val: acc + val, 
                        map(lambda rule: rule.calculate_fee(call), self._fee_rules), 
                        Money.wons(0))
  ```

  - 지금까지 구현한 클래스는 모두 변하지 않는 추상화에 해당한다.
    - 이 요소들을 조합하면 전체적인 협력 구조가 완성된다.
    - 즉 **변하지 않는 요소와 추상적인 요소만으로도 요금 계산에 필요한 전체적인 협력 구조를 설명할 수 있다**는 것이며, 이것이 핵심이다.
    - 변하는 부분과 변하지 않는 부분을 분리하고 변하는 것을 캡슐화한 코드는 오직 변하지 않는 것과 추상화에 대한 의존성만으로도 전체적인 협력을 구현할 수 있다.
    - 변하는 것은 추상화 뒤에 캡슐화되어 숨겨져 있기 때문에 전체적인 협력의 구조에는 영향을 미치지 않는다.



- 구체적인 협력 구현하기

  > 아래 코드는 전체적인 협력의 일관성을 보여주기 위한 코드로, 정상적으로 동작하진 않는다.

  - `FeeCondition` 인터페이스를 실체화하는 클래스를 구현한다.
  - 시간대별 정책 구현하기
    - `TimeOfDayFeeCondition`을 구현한다.
    - `TimeOfDayFeeCondition`의 인스턴스는 협력 안에서 `FeeCondition`을 대체할 수 있어야 한다.

  ```python
  class TimeOfDayFeeCondition(FeeCondition):
  
      def __init__(self, from_: time, to: time):
          self._from = from_
          self._to = to
      
      def find_time_intervals(self, call: Call):
          result = []
          for interval in call.get_interval().split_by_day():
              if self._get_from(interval) < self._get_to(interval):
                  from_time = self._get_from(interval)
                  to_time = self._get_to(interval)
                  result.append(DateTimeInterval(
                      datetime(interval.from_.year, interval.from_.month, interval.from_.day, from_time.hour, from_time.minute, from_time.second), 
                      datetime(interval.to.year, interval.to.month, interval.to.day, to_time.hour, to_time.minute, to_time.second)
                  ))
          return result
      
      def _get_from(self, interval: DateTimeInterval):
          return self._from if interval.from_.time() < self._from else interval.from_.time()
      
      def _get_to(self, interval: DateTimeInterval):
          return self._to if interval.to.time() > self._to else interval.to.time()
  ```

  -  요일별 정책 구현하기

  ```python
  class DayOfWeekFeeCondition(FeeCondition):
  
      def __init__(self, day_of_week: list[int]):
          self._day_of_week = day_of_week
  
      def find_time_intervals(self, call: Call):
          result = []
          for interval in call.get_interval().split_by_day():
              if interval.from_.weekday() in self._day_of_week:
                  result.append(interval)
          return result
  ```

  - 구간별 정책 구현하기

  ```python
  class DurationFeeCondition(FeeCondition):
  
      def __init__(self, from_: int, to: int):
          self._from = from_
          self._to = to
      
      def find_time_intervals(self, call: Call):
          # 구현
          ...
  ```



- 위 예제는 변경을 캡슐화해서 협력을 일관성 있게 만들면 어떤 장점이 있는지를 잘 보여준다.
  - 변하는 부분을 변하지 않는 부분으로부터 분리했기 때문에 변하지 않는 부분을 재사용할 수 있다.
    - 따라서 코드의 재사용성이 향상되고 테스트해야 하는 코드의 양이 감소한다.
  - 그리고 **새로운 기능을 추가하기 위해 오직 변하는 부분만 구현하면 되기 때문에 원하는 기능을 쉽게 완성할 수 있다.**
    - 기능을 추가할 때 따라야 하는 구조를 강제할 수 있기 때문에 기능을 추가하거나 변경할 때도 설계의 일관성이 무너지지 않는다.
    - 새로운 기본 정책을 추가하고 싶다면 `FeeCondition` 인터페이스를 구현하는 클래스를 구현하고 `FeeRule`과 연결하기만 하면 된다.
  - **일관성 있는 협력은 개발자에게 확장 포인트를 강제하기 때문에 정해진 구조를 우회하기 어렵게 만든다.**
    - 개발자는 코드의 형태로 주어진 제약 안에 머물러야 하지만 작은 문제에 집중할 수 있는 자유를 얻는다.
    - 그리고 이 작은 문제에 대한 해결책을 전체 문맥에 연결함으로써 협력을 확장하고 구체화할 수 있다.
  - 공통 코드의 구조와 패턴은 모든 기본 정책에 걸쳐 동일하기 때문에 코드를 한 번 이해하면 이 지식을 다른 코드를 이해하는 데 그대로 적용할 수 있다.



- 개념적 무결성(Conceptual Integrity)
  - 개념적 무결성을 일관성과 동일한 뜻으로 간주해도 무방하다.
    - 시스템이 일관성 있는 몇 개의 협력 패턴으로 구성된다면 시스템을 이해하고, 수정하고, 확장하는 데 필요한 시간과 노력을 아낄 수 있다.
    - 따라서 협력을 설계하고 있다면 항상 기존의 협력 패턴을 따를 수 없는지 고민해야 한다.
  - 유사한 기능에 대해 유사한 협력 패턴을 적용하는 것은 객체지향 시스템에서 개념적 무결성을 유지할 수 있는 가장 효과적인 방법이다.
  - 개념적 무결성을 유지하기 위해서는 지속적으로 개선해야한다.
    - 처음에는 일관성을 유지하는 것처럼 보이던 협력 패턴이 시간이 흐르면서 새로운 요구사항이 추가되는 과정에서 일관성이 조금씩 무너지는 경우가 자주 있다.
    - 협력을 설계하는 초기 단계에서 모든 요구사항을 미리 예상할 수 없기 때문에 이는 자연스러운 현상이다.
    - **협력은 고정된 것이 아니므로, 만약 현재의 협력 패턴이 변경의 무게를 지탱하기 어렵다면 변경을 수용할 수 있는 협력 패턴을 향해 리팩터링해야 한다.**







# 디자인 패턴과 프레임워크

- 디자인 패턴과 프레임워크의 정의
  - 디자인 패턴
    - **소프트웨어 설계에서 반복적으로 발생하는 문제에 대해 반복적으로 적용할 수 있는 해결 방법을 디자인 패턴이라고 부른다.**
    - 디자인 패턴의 목적은 설계를 재사용하는 것이다.
    - **디자인 패턴은 다양한 변경을 다루기 위해 반복적으로 재사용할 수 있는 설계의 묶음이다.**
    - 일단 디자인 패턴을 익히고 나면 변경의 방향과 주기를 이해하는 것만으로도 필요한 역할과 책임, 역할들의 협력 방식을 떠올릴 수 있게 된다.
  - 프레임워크
    - **디자인 패턴이 설계를 재사용하기 위한 것이라면 프레임워크는 설계와 코드를 함께 재사용하기 위한 것이다.**
    - 프레임워크는 애플리케이션의 아키텍처를 구현 코드의 형태로 제공한다.
    - 프레임워크가 제공하는 아키텍처가 요구사항에 적합하다면 다양한 환경에서 테스트를 거친 견고한 구현 코드를 재사용할 수 있다.
    - 프레임워크는 각 애플리케이션 요구에 따라 적절하게 커스터마이징할 수 있는 확장 포인트를 제공한다.
  - **디자인 패턴과 프레임워크 모두 일관성 있는 협력과 관련이 있다.**
    - 디자인 패턴은 특정한 변경을 일관성 있게 다룰 수 있는 협력 템플릿을 제공한다.
    - 디자인 패턴이 협력을 일관성 있게 만들기 위해 재사용할 수 있는 설계의 묶음이라면, 프레임워크는 일관성 있는 협력을 제공하는 확장 가능한 코드라고 할 수 있다.
    - 결론적으로 둘 모두 협력을 일관성 있게 만들기 위한 방법이다.





## 디자인 패턴과 설계 재사용

- 소프트웨어 패턴

  - 패턴의 핵심적인 특징
    - 패턴은 반복적으로 발생하는 문제와 해법의 쌍으로 정의된다.
    - 패턴을 사용함으로써 이미 알려진 문제와 이에 대한 해법을 문서로 정리할 수 있으며, 이 지식을 다른 사람과 의사소통할 수 있다.
    - 패턴은 추상적인 원칙과 실제 코드 작성 사이의 간극을 메워주며 실질적인 코드 작성을 돕는다.
    - 패턴의 요점은 패턴이 실무에서 탄생했다는 점이다.
  - 마틴 파울러의 패턴의 정의
    - **하나의 실무 컨텍스트(practical context)에서 유용하게 사용해 왔고 다른 실무 컨텍스트에서도 유용할 것이라고 예상되는 아이디어.**
    - 아이디어라는 용어를 사용한 이유는 어떤 것도 패턴이 될 수 있기 때문이다.
    - 실무 컨텍스트라는 용어는 패턴이 실제 프로젝트의 실무 경험에서 비롯됐다는 사실을 반영한다.
    - 패턴을 발명했다고 하지 않고 발견했다고 하는 이유는 모델의 유용성이 널리 알려지는 경우에만 패턴으로 인정할 수 있기 때문이다.
    - 실무 프로젝트가 패턴보다 먼저지만 그렇다고 실무 프로젝트의 모든 아이디어가 패턴인 것은 아니다.
    - 패턴은 개발자들이 다른 컨텍스트에서도 유용할 것이라고 생각하는 어떤 것이다.

  - 3의 규칙(Rule of Three)
    - 패턴은 한 컨텍스트에서 유용한 동시에 다른 컨텍스트에서도 유용한 아이디어다.
    - 3의 규칙은 최소 세 가지의 서로 다른 시스템에 특별한 문제 없이 적용할 수 있고 유용한 경우에만 패턴으로 간주할 수 있다는 규칙이다.
  - **패턴은 경험의 산물이다.**
    - 패턴이 지닌 가장 큰 가치는 경험을 통해 축적된 실무 지식을 효과적으로 요약하고 전달할 수 있다는 점이다.
    - 패턴은 실무 현장에서 검증되고 입증된 자신으로, 실무 경험이 적은 초보자라고 하더라도 패턴을 익히고 반복적으로 적용하는 과정 속에서 유연하고 품질 높은 소프트웨어를 개발하는 방법을 익힐 수 있게 된다.
  - 패턴의 이름
    - 패턴은 지식 전달과 커뮤니케이션 수단으로 활용할 수 있기 때문에 패턴의 이름 역시 매우 중요하다.
    - 패턴의 이름은 커뮤니티가 공유할 수 있는 어휘집을 제공한다.
    - 잘 알려진 이름을 사용함으로써 장황한 대화를 패턴으로 단순하게 설명이 가능하다.
  - 패턴은 홀로 존재하지 않는다.
    - 특정 패턴 내에 컴포넌트와 컴포넌트 간의 관계는 더 작은 패턴에 의해 서술될 수 있으며, 패턴을 포함하는 더 큰 패턴 내에 통합될 수 있다.
    - 크리스토퍼 알렉산더는 연관된 패턴들의 집합들이 모여 하나의 패턴 언어(Pattern Language)를 구성한다고 정의하고 있다.
    - 패턴 언어는 연관된 패턴 카테고리뿐만 아니라 패턴의 생성 규칙과 함께 패턴 언어에 속한 다른 패턴과의 관계 및 협력 규칙을 포함한다.
    - POSA1에서는 패턴 언어라는 용어가 지닌 제약 조건을 완화하기 위해 패턴 시스템이라는 특수한 용어의 사용을 제안하기도 했으나 현재 두 용어는 거의 동일한 의미로 사용되고 있다.



- 패턴 분류
  - 패턴을 분류하는 가장 일반적인 방법은 패턴의 범위나 적용 단계에 따라 아래와 같이 4가지로 분류하는 것이다.
    - 아키텍처 패턴(Architecture Pattern)
    - 분석 패턴(Analysis Pattern)
    - 디자인 패턴(Design Pattern)
    - 이디엄(Idiom)
  - 4가지 중 가장 널리 알려진 것은 디자인 패턴이다.
    - 디자인 패턴은 특정 정황 내에서 일반적인 설계 문제를 해력하며, 협력하는 컴포넌트들 사이에서 반복적으로 발생하는 구조를 서술한다.
    - 디자인 패턴은 중간 규모의 패턴으로, 특정한 설계 문제를 해결하는 것을 목적으로 하며, 프로그래밍 언어나 프로그래밍 패러다임에 독립적이다.
  - 디자인 패턴의 상위에는 아키텍처 패턴이 위치한다.
    - 아키텍처 패턴은 소프트웨어의 전체적인 구조를 결정하기 위해 사용한다.
    - 미리 정의된 서브시스탬들을 제공하고, 각 서브시스템의 책임을 정의하며, 서스시스템들 사이의 관계를 조직화하는 규칙과 가이드라인을 포함한다.
    - 아키텍처 패턴은 구체적인 소프트웨어 아키텍처를 위한 템플릿을 제공하며, 디자인 패턴과 마찬가지로 프로그래밍 언어나 패러다임에 독립적이다.
  - 다자인 패턴의 하위에는 이디엄이 위치한다.
    - 이디엄은 특정 프로그래밍 언어에만 국한된 하위 레벨 패턴으로, 주어진 언어의 기능을 사용해 컴포넌트, 혹은 컴포넌트 간의 측면을 구현하는 방법을 서술한다.
    - 이디엄은 언어의 종속적이기 때문에 특정 언어의 이디엄이 다른 언어에서는 무용지물이 될 수 있다.
  - 분석 패턴은 도메인 내의 개념적인 문제를 해결하는 데 초점을 맞춘다.
    - 업무 모델링 시에 발견되는 공통적인 구조를 표현하는 개념들의 집합이다.
    - 분석 패턴은 하나의 도메인에 대해서만 적절할 수도 있고 여러 도메인에 걸쳐 적용할 수도 있다.



- 패턴과 책임-주도 설계

  - 객체지향 설계에서 가장 중요한 일은 올바른 책임을 올바른 객체에게 할당하고 객체 간의 유연한 협력 관계를 구축하는 일이다.
    - 책임과 협력의 윤곽은 캡슐화, 크기, 의존성, 유연성, 성능, 확장 가능성, 재사용성 등의 다양한 요소들의 트레이드오프를 통해 결정된다.
    - 대부분의 경우 훌륭한 품질의 설계를 얻기 위해 많은 시간과 노력을 들여야 한다.

  - 패턴은 공통으로 사용할 수 있는 역할, 책임, 협력의 템플릿이다.
    - 패턴은 반복적으로 발생하는 문제를 해결하기 위해 사용할 수 있는 공통적인 역할과 책임, 협력의 훌륭한 예제를 제공한다.
    - 패턴을 따르면 특정한 상황에 적용할 수 있는 설계를 쉽고 빠르게 떠올릴 수 있다는 사실이다.
    - 특정한 상황에 적용 가능한 패턴을 잘 알고 있다면 책임 주도 설계의 절차를 하나하나 따르지 않고도 시스템 안에 구현할 객체들의 역할과 책임, 협력 관계를 빠르고 손쉽게 구성할 수 있다.
  - **패턴의 구성 요소는 클래스가 아니라 역할이다.**
    - 이 사실은 패턴 템플릿을 구현할 수 있는 다양한 방법이 존재한다는 사실을 암시한다.
    - 역할은 동일한 오퍼레이션에 대해 응답할 수 있는 책임의 집합을 암시하기 때문에 하나의 객체가 여러 역할을 수행하더라도 문제가 없다.
    - 반다로 다수의 클래스가 동일한 역할을 구현할 수도 있다.
    - **어떤 구현 코드가 어떤 디자인 패턴을 따른다고 이야기 할 때는 역할, 책임, 협력의 관점에서 유사성을 공유한다는 것이지 특정한 구현 방식을 강제하는 것은 아니라는 점을 이해하는 것 역시 중요하다.**
  - **디자인 패턴은 단지 역할과 책임, 협력의 템플릿을 제안할 뿐 구체적인 구현 방법에 대해서는 제한을 두지 않는다.**



- 캡슐화와 디자인 패턴

  - **대부분의 디자인 패턴은 특정한 변경을 캡슐화하기 위한 독자적인 방법을 정의하고 있다.**
    - 대부분의 디자인 패턴은 협력을 일관성 있고 유연하게 만드는 것을 목적으로 하기 때문이다.
    - 영화 예매 시스템에서 `Movie`가 `DiscountPolicy` 상속 계층을 합성 관계로 유지하도록 한 것은 STRATEGY 패턴을 사용하여 변경을 캡슐화한 것이다.

  - 합성뿐 아니라 상속을 이용하여 변경을 캡슐화하는 TEMPLATE METHOD 같은 패턴도 있다.
    - 이 패턴은 변하지 않는 부분은 부모 클래스로, 변하는 부분은 자식 클래스로 분리하여 변경을 캡슐화한다.
    - 이처럼 알고리즘을 캡슐화하기 위해 합성이 아닌 상속을 사용하는 것을 TEMPLATE METHOD 패턴이라고 부른다.
    - 상속을 사용할 경우에는 추상 클래스나 인터페이스를 사용해 변경을 캡슐화하는 합성과 달리 추상 메서드를 이용해 변경을 캡슐화해야 한다.
    - 부모 클래스에서 추상 메서드를 호출하고, 자식 클래스들이 이 추상 메서드를 오버라이딩해서 변하는 부분을 구현한다.
  - DEOCRATOR 역시 선택적인 행동의 개수와 순서에 대한 변경을 캡슐화하는 데 사용할 수 있다.



- 패턴은 출발점이다.
  - 패턴은 출발점이지 목적지가 아니다.
    - **패턴은 설계의 목표가 되어서는 안 되며, 목표로 하는 설계에 이를 수 있는 방향을 제시하는 용도로 사용해야 한다.**
  - 패턴을 맹목적으로 사용해선 안 된다.
    - 패턴을 사용하면서 부딪히게 되는 대부분의 문제는 패턴을 맹목적으로 사용할 때 발생한다.
    - 패턴을 적용하는 맥락의 적절성을 고려해야 한다.
    - 해결하려는 문제가 아니라 패턴이 제시하는 구조를 맹목적으로 따르는 것은 불필요하게 복잡하고 유지보수하기 어려운 시스템을 낳는다.
    - 패턴은 복잡성의 가치가 단순성을 넘어설 때에만 정당화돼야 한다.
  - 코드를 공유하는 모든 사람들이 적용된 패턴을 알고 있어야 한다.





## 프레임워크와 코드 재사용

- 코드 재사용 대 설계 재사용
  - 디자인 패턴은 언어에 독립적으로 재사용 가능한 설계 아이디어를 제공하는 것을 목적으로 한다.
    - 따라서 언어에 종속적인 구현 코드를 정의하지 않기 때문에 디자인 패턴을 적용하기 위해서는 설계 아이디어를 프로그래밍 언어의 특성이 맞춰 가공해야 하고 매번 구현 코드를 재작성해야 한다는 단점이 있다.
  - **재사용 관점에서 설계 재사용보다 더 좋은 방법은 코드 재사용이다.**
    - **그러나 코드는 도메인에 따라 달리지므로 재사용 할 수 있을 만큼 일반적인 코드는 소수 밖에 없다.**
  - 프레임워크
    - 추상적인 수준의 설계 재사용을 강조하는 디자인 패턴은 재사용을 위해 매번 유사한 코드를 작성해야만 한다.
    - 도메인에 따라 달라지는 코드는 재사용이 어렵다.
    - 따라서 가장 이상적인 형태의 재사용 방법은 코드 재사용과 설계 재사용을 적절한 수준으로 조합하는 것이며, 이를 위해 프레임워크가 등장했다.
    - 단, 프레임워크는 코드의 재사용 보다는 설계 자체의 재사용을 중시한다.
    - 프레임워크란 '추상 클래스나 인터페이스를 정의하고 인터페이스 사이의 상호작용을 통해 시스템 전체 혹은 일부를 구현해 놓은 재사용 가능한 설계' 또는 '커스터마이징할 수 있는 애플리케이션의 골격'을 의미한다.
    - 첫 번째 정의가 프레임워크의 구조적인 측면에 초점을 맞추고 있다면, 두 번째 정의는 코드와 설계의 재사용이라는 프레임워크의 사용 목적에 초점을 맞춘다.
  - 프레임워크는 코드를 재사용함으로써 설계 아이디어를 재사용한다.
    - 애플리케이션의 아키텍처를 제공하며 문제 해결에 필요한 설계 결정과 이에 필요한 기반 코드를 함께 포함한다.
    - 또한 애플리케이션을 확장할 수 있도록 부분적으로 구현된 추상 클래스와 인터페이스 집합뿐만 아니라 추가적인 작업 없이도 재사용 가능한 다양한 종류의 컴포넌트(재사용 가능한 코드)도 함께 제공한다.
  - 프레임워크는 애플리케이션에 대한 아키텍처를 제공한다.
    - **즉 프레임워크는 클래스와 객체들의 분할, 전체 구조, 클래스와 객체들 간의 상호작용, 객체와 클래스의 조합 방법, 제어 흐름에 대해 미리 정의한다.**
    - **프레임워크는 설계의 가변성을 미리 정의해 뒀기 때문에 애플리케이션 설계자나 구현자는 애플리케이션에 종속된 부분(도메인과 관련된 부분)에 대해서만 설계하면 된다.**
    - 프레임워크는 애플리케이션 영역에 걸쳐 공통의 클래스들을 정의해서 일반적인 설계 결정을 미리 내려 둔다.



- 상위 정책과 하위 정책으로 패키지 분리하기
  - 프레임워크의 핵심은 추상 클래스나 인터페이스와 같은 추상화라고 할 수 있다.
    - 추상 클래스와 인터페이스가 가지는 특징 중 일관성 있는 협력이 프레임워크의 재사용성을 향상시킨다.
  - 추상 클래스와 인터페이스가 일관성 있는 협력을 만드는 핵심 재료이다.
    - 협력을 일관성 있고 유연하게 만들기 위해서는 추상화를 이용해 변경을 캡슐화해야 한다.
    - 협력을 구현하는 코드 안의 의존성은 가급적이면 추상 클래스나 인터페이스와 같은 추상화를 향하도록 작성해야 한다.
  - 프레임워크는 변하는 것과 변하지 않는 것을 분리해야 한다.
    - 상위 정책이 세부 사항에 비해 재사용될 가능성이 높다.
    - 의존성 역전 원칙의 관점에서 세부 사항은 변경을 의미한다.
    - 상위 정책이 변경되는 세부 사항에 의존하게 되면 상위 정책이 필요한 모든 경우에 세부 사항도 함께 존재해야 하기 때문에 상위 정책의 재사용성이 낮아진다.
    - 이 문제를 해결할 수 있는 가장 좋은 방법은 의존성 역전 원칙에 맞게 상위 정책과 세부 사항 모두 추상화에 의존하게 하는 것이다.
    - 이를 위해서는 변하는 것과 변하지 않는 것을 분리해야 한다.
    - 프레임워크는 여러 애플리케이션에서 재사용 가능해야 하기 때문에 변하는 것과 변하지 않는 것을 서로 다른 주기로 배포할 수 있도로 별도의 배포 단위로 분리해야 한다.
    - 이를 위한 첫걸음은 변하는 부분과 변하지 않는 부분을 별도의 패키지로 분리하는 것이다.
  - 별도의 패키지로 분리할 때 중요한 것은 패키지 사이의 의존성의 방향이다.
    - 의존성 역전 원칙에 따라 추상화에만 의존하도록 의존성의 방향을 조정하고 추상화를 경계로 패키지를 분리하기 때문에 세부 사항을 구현한 패키지는 항상 상위 패키지에 의존해야 한다.
    - 이를 통해 상위 정책을 구현하고 있는 패키지를 다른 애플리케이션에 재사용할 수 있게 된다.



- **제어 역전의 원리**
  - 상위 정책을 재사용한다는 것은 결국 도메인에 존재하는 핵심 개념들 사이의 협력 관계를 재사용한다는 것을 의미한다.
    - 객체지향 설계의 재사용성은 개별 클래스가 아니라 객체들 사이의 공통적인 협력 흐름으로부터 나온다.
    - 그리고 그 뒤에는 의존성 역전 원리가 있다.
  - 의존성 역전 원리는 전통적인 설계 방법과 객체지향을 구분하는 가장 핵심적인 원리이다.
    - 의존성 역전 원리에 따라 시스템을 구축해야 협력 흐름을 재사용할 수 있고 변경에 유연하게 대처할 수 있다.
    - 시스템이 진화하는 방향에는 항상 의존성 역전 원리를 따르는 설계가 존재해야 한다.
  - 의존성 역전 원리는 프레임워크의 가장 기본적인 설계 매커니즘이다.
    - **의존성 역전은 의존성의 방향뿐만 아니라 제어 흐름의 주체 역시 역전시킨다.**
    - 정책이 구체적인 세부사항에 의존하는 **전통적인 구조에서는 상위 정책의 코드가 하부의 구체적인 코드를 호출한다.**
    - 즉 애플리케이션의 코드가 재사용 가능한 라이브러리나 툴킷의 코드를 호출한다.
  - **의존성을 역전시키면 제어 흐름의 주체 역시 역전된다.**
    - **의존성을 역전시킨 객체지향 구조에서는 반대로 프레임워크가 애플리케이션에 속하는 서브클래스의 메서드를 호출한다.**
    - 따라서 프레임워크를 사용할 경우 **개별 애플리케이션에서 프레임워크로 제어 흐름의 주체가 이동한다.**
    - 이를 **제어의 역전 원리 혹은 할리우드 원리라고 한다.**
    - 제어의 역전은 프레임워크의 핵심 개념인 동시에 코드의 재사용을 가능하게 하는 힘이다.
  - **훅(Hook)**
    - 프레임워크에서는 **일반적인 해결책만 제공하고 애플리케이션에 따라 달라질 수 있는 특정한 동작은 비워둔다.**
    - **이렇게 완성되지 않은 채로 남겨진 동작을 훅이라고 부른다.**
    - 훅의 구현 방식은 애플리케이션의 컨텍스트에 따라 달라진다.
    - 훅은 프레임워크 코드에서 호출하는 프레임워크의 특정 부분이다.
    - 재정의된 훅은 제어 역전 원리에 따라 프레임워크가 원하는 시점에 호출된다.
  - **협력을 제어하는 것은 프레임워크라는 것에 주목해야 한다.**
    - **개발자는 프레임워크가 적절한 시점에 실행할 것으로 예상되는 코드를 작성할 뿐이다.**
    - **예전에는 개발자가 직접 라이브러리의 코드를 호출했지만 객체지향의 시대에는 그저 프레임워크가 호출하는 코드를 작성해야만 한다.**
    - 제어가 개발자에게서 프레임워크로 넘어간 것이다.
    - 즉 제어가 역전된 것이다.
  - 할리우드 원리
    - 할리우드에서 캐스팅 담당자가 오디션을 보러 온 배우에게 "먼저 연락하지 마세요. 저희가 연락 드리겠습니다."라고 말하는 것처럼 프레임워크는 자신을 찾지 말라고 이야기한다.
    - 우리가 작성한 코드는 수동적인 존재며, 프레임워크가 호출할 때 까지 기다리기만 할 뿐이다.
  - 결국 요약하면 아래와 같다.
    - 프레임워크는 객체들 간의 상호 작용 및 제어 흐름 등을 정의한다.
    - 개발자는 프레임워크가 비워 둔 훅을 작성(재정의)한다.
    - 개발자가 작성한 훅은 프레임워크가 미리 정의해둔 방식으로 다른 객체들과 상호작용 하며 제어 흐름을 따라 동작한다.





# 핵심

- 가능하면 유사한 기능을 구현하기 위해 유사한 협력 패턴을 사용해야 한다.



- 객체지향에서 변경을 처리하는 전통적인 방법은 조건 로직을 객체 사이의 이동으로 바꾸는 것이다.



- 객체지향적인 코드는 조건을 판단하지 않는다. 단지 다음 객체로 이동할 뿐이다.



- 조건 로직을 객체 사이의 이동으로 대체하기 위해서는 커다란 클래스를 더 작은 클래스들로 분리해야 한다.



- 클래스를 분리할 때 고려해야 할 가장 중요한 기준은 변경의 이유와 주기다.



- 캡슐화란 변하는 어떤 것이든 감추는 것이다.



- 변하는 부분과 변하지 않는 부분을 분리하고, 변하는 부분을 적절히 추상화하고 나면 변하는 부분을 생략한 채 변하지 않는 부분만을 이용해 객체 사이의 협력을 이야기할 수 있다.



- 협력은 고정된 것이 아니므로, 만약 현재의 협력 패턴이 변경의 무게를 지탱하기 어렵다면 변경을 수용할 수 있는 협력 패턴을 향해 리팩터링해야 한다.



- 소프트웨어 설계에서 반복적으로 발생하는 문제에 대해 반복적으로 적용할 수 있는 해결 방법을 디자인 패턴이라고 부른다.



- 디자인 패턴은 단지 역할과 책임, 협력의 템플릿을 제안할 뿐 구체적인 구현 방법에 대해서는 제한을 두지 않는다.



- 패턴은 설계의 목표가 되어서는 안 되며, 목표로 하는 설계에 이를 수 있는 방향을 제시하는 용도로 사용해야 한다.



- 의존성을 역전시킨 객체지향 구조에서는 반대로 프레임워크가 애플리케이션에 속하는 서브클래스의 메서드를 호출한다.
