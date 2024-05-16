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

  - 요일별 방식 구현하기
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



