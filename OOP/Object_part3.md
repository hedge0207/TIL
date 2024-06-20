# 책임 할당하기

- 책임 주도 설계
  - 데이터 중심의 설계에서 책임 중심의 설계로 전환하기 위해서는 다음의 두 가지 원칙을 따라야한다.
    - 데이터보다 행동을 먼저 결정하라.
    - 협력이라는 문맥 안에서 책임을 결정하라.
  - 데이터보다 행동을 먼저 결정하라.
    - 객체에게 중요한 것은 데이터가 아니라 외부에 제공하는 행동이다.
    - 객체지향 설계에서 가장 중요한 것은 적절한 객체에게 적절한 책임을 할당하는 능력이다.
    - 그리고 적절한 책임을 할당할 수 있는 문맥을 제공하는 것이 협력이다.
  - 협력이라는 문맥 안에서 책임을 결정하라.
    - **객체에게 할당된 책임의 품질은 협력에 적합한 정도로 결정된다.**
    - 객체에게 할당된 책임이 협력에 어울리지 않는다면 그 책임은 나쁜 것이다.
    - 객체의 입장에서는 책임이 조금 어색해 보이더라도 협력에 적합하다면 그 책임은 좋은 것이다.
    - **책임은 객체의 입장이 아니라 객체가 참여하는 협력에 적합해야 한다.**
    - 협력을 시작하는 주체는 메시지 전송자이기 때문에 협력에 적합한 책임이란 메시지 수신자가 아니라 전송자에게 적합한 책임을 의미한다.
    - 즉, **메시지를 전송하는 클라이언트의 의도에 적합한 책임을 할당해야 한다.**
    - 협력에 적합한 책임을 수확하기 위해서는 객체를 결정한 후에 메시지를 선택하는 것이 아니라 메시지를 결정한 후에 객체를 선택해야한다.
  - **객체가 메시지를 선택하는 것이 아니라 메시지가 객체를 선택하게 해야 한다.**
    - 메시지가 존재하기 때문에 그 메시지를 처리할 객체가 필요한 것이다.
    - 메시지는 클라이언트의 의도를 표현하며, 클라이언트는 어떤 객체가 메시지를 수신할지 알지 못한다.
    - 클라이언트는 단지 임의의 객체가 메시지를 수신할 것이라는 사실을 믿고 자신의 의도를 표현한 메시지를 전송할 뿐이다.
    - 메시지를 수신하기로 결정된 객체는 메시지를 처리할 책임을 할당 받게 된다.
    - **메시지를 먼저 결정하기 때문에 송신자는 메시지 수신자에 대한 어떠한 가정도 할 수 없으므로, 전송자 관점에서 수신자는 깔끔하게 캡슐화된다.**





## 책임 할당을 위한 GRASP 패턴

- GRASP(General Responsibility Assignment Sofware Pattern)
  - 크레이그 라만이 책임 할당 기법을 패턴 형식으로 제안한 것이다.
  - 객체에게 책임을 할당할 때 지침으로 삼을 수 있는 원칙들의 집합을 패턴 형식으로 정리한 것이다.



- 도메인 개념에서 출발하기
  - 설계를 시작하기 전에 도메인에 대한 대략적인 모습을 그려 보는 것이 유용하다.
    - 도메인 안에는 무수히 많은 개념들이 존재하며 이 도메인 개념들을 책임 할당의 대상으로 사용하면 코드에 도메인의 모습을 투영하기가 좀 더 수월해진다.
    - 따라서 어떤 책임을 할당해야 할 때 가장 먼저 고민해야 하는 유력한 후보는 바로 도메인 개념이다.
    - 설계의 시작 단계에서 개념들의 의미와 관계를 정확히 정의할 필요는 없으며, 책임을 할당 받을 객체들의 종류와 관계에 대한 유용한 정보만 알아낼 수 있다면 충분하다.
  - 단 하나의 정답이라 부를 수 있는 도메인 모델이란 존재하지 않는다.
    - 올바른 구현을 이끌어낼 수만 있다면 모두 올바른 도메인 모델이라 할 수 있다.
    - 많은 사람들이 도메인 모델은 구현과 무관하다고 생각하지만, 이는 사실이 아니다.
    - 도메인 모델은 도메인을 개념적으로 표현한 것이지만 그 안에 포함된 개념과 관계는 구현의 기반이 되어야 한다.
    - 이는 도메인 모델이 구현을 염두에 두고 구조화되는 것이 바람직하다는 것을 의미한다.
    - 반대로 코드의 구조가 도메인을 바라보는 관점을 바꾸기도 한다.



- 정보 전문가에게 책임을 할당하라.
  - 객체는 어떤 책임을 수행하는 전문가라고 할 수 있으며, 책임을 수행할 정보를 알고 있는 객체에게 책임을 할당해야 한다.
    - GRASP에서는 이를 정보 전문가 패턴이라고 부른다.
    - 정보 전문가 패턴은 객체란 상태와 행동을 함께 가지는 단위라는 객체지향의 가장 기본적인 원리를 책임 할당의 관점에서 표현한다.
    - 객체는 특정한 책임을 수행할 수 있는 행동과 행동을 수행하는 데 필요한 정보를 가지고 있다.
    - 책임 수행에 가장 적절한 정보를 가지고 있는 객체에게 책임을 할당해야 한다.
  - 주의할 점은 **정보 전문가 패턴에서 말하는 정보는 객체 내부의 상태와는 다르다는 점이다.**
    - 책임을 수행하는 객체가 정보를 알고 있다고 해서 그 정보를 상태로 저장하고 있을 필요는 없다.
    - 객체는 해당 정보를 제공할 수 있는 다른 객체에 대해 알고 있거나, 필요한 정보를 계산해서 제공할 수도 있다.



- 낮은 응집도와 높은 결합도
  - 낮은 결합도 패턴
    - 설계의 전체적인 결합도가 낮게 유지되게 책임을 할당해야 한다는 패턴이다.
    - 낮은 결합도는 설계 결정을 평가할 때 적용할 수 있는 평가 원리다.
    - 여러 가지 방식으로 설계가 가능하다면, 추가적인 의존성이 발생하지 않는 설계가 더 좋은 설계라고 할 수 있다.
  - 높은 응집도 패턴
    - 설계의 전체적인 응집도가 높게 유지되게 책임을 할당해야 한다는 패턴이다.
    - 높은 응집도 역시 설계 결정을 평가할 때 적용할 수 있는 평가 원리다.
    - 여러 방식으로 설계가 가능하다면 높은 응집도를 유지할 수 있는 설계를 선택해야 한다.



- 창조자(CREATOR) 패턴
  - 창조자 패턴은 객체를 생성할 책임을 어떤 객체에게 할당할지에 대한 지침을 제공한다.
    - 객체 A를 생성해야 할 때 아래 조건을 최대한 많이 만족하는 B에게 객체 생성 책임을 할당해야한다.
    - B가 A객체를 포함하거나 참조한다.
    - B가 A객체를 기록한다.
    - B가 A 객체를 긴밀하게 사용한다.
    - B가 A 객체를 초기화하는 데 필요한 데이터를 가지고 있다(이 경우 B는 A에 대한 정보 전문가다)
  - 결합도를 높이지 않고 객체를 생성하기 위한 지침이다.
    - 다른 객체를 생성하기 위해서는 많건 적건 생성하려는 객체에 대한 정보를 알고 있어야한다.
    - 따라서 생성될 객체에 대해서 이미 잘 알고 있거나 해당 객체를 사용해야 하는 객체는 이미 생성 할 객체와 연결(결합)되어 있다고 볼 수 있다.
    - 생성 될 객체와 이미 연결되어 있는 객체에게 객체의 생성을 맡기면 결합도의 증가 없이 객체를 생성할 수 있게 된다. 



- 다형성 패턴
  - 객체의 타입에 따라 변하는 행동이 있다면 타입을 분리하고 변화하는 행동을 각 타입의 책임으로 할당하는 것을 GRASP에서는 다형성 패턴이라고 부른다.
  - 다형성 패턴은 객체의 타입을 검사해서 객체의 타입에 따라 여러 대안을 사용하는 조건적인 논리를 사용하지 말라고 경고한다.
    - 프로그램의 if ~ else 등의 조건 논리를 사용해서 설계한다면 새로운 변화가 일어난 경우 조건 논리를 수정해야 한다.
    - 이는 프로그램을 수정하기 어렵고 변경에 취약하게 만든다.
    - 조건 논리 대신 다형성을 이용하면 새로운 변화를 다루기 쉽게 확장할 수 있다.



- 변경 보호(PROTECTED VARIATIONS) 패턴
  - 변경을 캡슐화하도록 책임을 할당하는 것을 GRASP에서는 변경 보호 패턴이라고 부른다.
    - **안정된 인터페이스 뒤로 변경을 캡슐화 하여 변경의 영향이 외부로 퍼지지 않도록 하는 패턴이다.**
    - 책임 할당의 관점에서 캡슐화를 설명하는 패턴으로, '설계에서 변하는 것이 무엇인지 고려하고 변하는 개념을 캡슐화하라'라는 객체지향의 오랜 격언은 변경 보호 패턴의 본질을 잘 설명해준다.
  - 다형성 패턴과의 조합
    - 클래스를 변경에 따라 분리하고 인터페이스를 이용해 변경을 캡슐화하는 것은 설계의 결합도와 응집도를 향상시키는 매우 강력한 방법이다.
    - 하나의 클래스가 여러 타입의 행동을 구현하고 있는 것처럼 보인다면 클래스를 분해하고 다형성 패턴에 따라 책임을 분산시켜라.
    - 예측 가능한 변경으로 인해 여러 클래스들이 불안정해진다면 변경 보호 패턴에 따라 안정적인 인터페이스 뒤로 변경을 캡슐화하라.
    - 적절한 상황에서 두 패턴을 조합하면 코드 수정의 파급 효과를 조절할 수 있고 변경과 확장에 유연하게 대처할 수 있는 설계를 얻을 수 있다.





## 구현을 통한 검증

- `Screening` 구현하기

  - 영화를 예매할 책임을 맡으며, 그 결과로  `Reservation` 인스턴스를 생성할 책임을 수행한다.
    - 즉 예매에 대한 정보 전문가인 동시에 `Reservation`의 창조자다.
  - 협력의 관점에서 `Screening`은 "예매하라" 메시지에 응답할 수 있어야한다.
    - 따라서 이 메시지를 처리할 수 있는 메서드를 구현한다.

  ```python
  class Screening:
  
      def reserve(self, customer: Customer, audience_count: int):
          pass
  ```

  - 책임이 결정됐으므로 책임을 수행하는 데 필요한 인스턴스 변수를 결정한다.

  ```python
  class Screening:
      def __init__(self, movie: Movie, sequence: int, when_screened: datetime):
          self._movie = movie
          self._sequence = sequence
          self._when_screened = when_screened
  ```

  - 영화 예매를 위해서는 `Movie`에게 "가격을 계산하라" 메시지를 보내서 계산된 영화 요금을 반환받아야 한다.
    - `calculate_fee` 메서드를 구현한다.

  ```python
  class Screening:
      def __init__(self, movie: Movie, sequence: int, when_screened: datetime):
          self._movie = movie
          self._sequence = sequence
          self._when_screened = when_screened
  
      def reserve(self, customer: Customer, audience_count: int):
          return Reservation(customer, self, self._calculate_fee(audience_count), audience_count)
      
      def _calculate_fee(self, audience_count: int):
          return self._movie.calculate_movie_fee(self).times(audience_count)
  ```

  - 위 코드에서 `Movie`에 전송하는 메시지의 시그니처를 `calculate_movie_fee`로 선언했다는 사실에 주목해야 한다.
    - 메시지는 수신자인 `Movie`가 아니라 송신자인 `Screening`의 의도를 표현하며, `Screening`은 `Movie`의 내부 구현에 대한 어떤 지식도 없이 전송할 메시지를 결정했다.
    - 이처럼 `Movie`의 구현을 고려하지 않고 필요한 메시지를 결정하면 `Movie`의 내부 구현을 깔끔하게 캡슐화할 수 있다.
    - 이제 `Screening`과 `Movie`를 연결하는 유일한 연결 고리는 메시지뿐이다.
    - 따라서 메시지가 변경되지 않는 한 `Movie`에 어떤 수정을 가하더라도 `Screening`은 영향을 받지 않는다.
    - 이처럼 **메시지가 객체를 선택하도록 책임 주도 설계의 방식을 따르면 캡슐화와 낮은 결합도라는 목표를 비교적 손 쉽게 달성할 수 있다.**



- `Movie`를 구현한다.

  - `Movie`는 `calculate_movie_fee`라는 메시지로 부터 선택 받았기 때문에, 즉 `Screening`의 메시지에 응답해야 하기 때문에, `calculate_movie_fee` 메서드를 구현해야한다.

  ```python
  class Movie:
      def calculate_movie_fee(self, screening: Screening):
          ...
  ```

  - 요금을 계산하는 데 필요한 데이터들을 인스턴스 변수로 포함시킨다.

  ```python
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
  ```

  - 요금 계산 로직 구현하기
    - `Movie`는 `DiscountCondition` 인스턴스에게 `is_satisfied_by` 메시지를 전송하여 할인 여부를 판단하도록 요청한다.
    - 만약 할인 조건을 만족한다면 할인 요금을 계산하기 위해 `_calculate_discount_amount` 메서드를 호출한다.

  ```python
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
  ```



- `DiscountCondition`을 구현한다.

  - `Movie`는 `DiscountCondition`에게 할인 요금을 계산하라는 메시지를 전송하므로, `DiscountCondition`은 이 메시지를 처리하기 위해 `is_satisfied_by`를 구현해야 한다.

  ```python
  class DiscountCondition:
      
      def is_satisfied_by(self, screening: Screening):
          ...
  ```

  - 메시지를 처리하는 데 필요한 정보들을 인스턴스 변수로 포함시킨다.

  ```python
  class DiscountCondition:
      
      def __init__(self, discount_condition_type: DiscountConditionType, sequence: int=None, 
                   day_of_week: str=None, start_time: time=None, end_time: time=None):
          self._discount_condition_type = discount_condition_type
          self._sequence = sequence
          self._day_of_week = day_of_week
          self._start_time = start_time
          self._end_time = end_time
  ```

  - `is_satisfied_by` 메서드를 구현한다.

  ```python
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
  ```



- **변경의 이유가 둘 이상인 클래스 찾아내기**
  - 일반적으로 설계를 개선하는 작업은 변경의 이유가 하나 이상인 클래스를 찾는 것으로부터 시작하는 것이 좋다.
    - 문제는 클래스 안에서 변경의 이유를 찾는 것이 생각보다 어렵다는 것이다.
    - 다행히도, 변경의 이유가 하나 이상인 클래스에는 위험 징후를 또렷하게 드러내는 몇 가지 패턴이 존재한다.
  - **인스턴스 변수가 초기화되는 시점을 살펴본다.**
    - 응집도가 높은 클래스는 인스턴스를 생성할 때 모든 속성을 함께 초기화한다.
    - 반면 응집도가 낮은 클래스는 객체의 속성 중 일부만 초기화되고 나머지는 초기화되지 않은 상태로 남겨진다.
    - 따라서 초기화되는 속성을 기준으로 코드를 분리해야한다.
  - **메서드들이 인스턴스 변수를 사용하는 방식을 살펴본다.**
    - 모든 메서드가 객체의 모든 속성을 사용한다면 클래스의 응집도는 높다고 볼 수 있다.
    - 반면 메서드들이 사용하는 속성에 따라 그룹이 나뉜다면 클래스의 응집도가 낮다고 볼 수 있다.
    - 이 경우 클래스의 응집도를 높이기 위해서는 속성 그룹과 해당 그룹에 접근하는 메서드 그룹을 기준으로 코드를 분리해야 한다.



- `DiscountCondition`의 문제점
  - `DiscountCondition`은 코드를 수정해야 하는 이유가 하나를 초과하는 변경에 취약한 코드다.
    - 새로운 할인 조건이 추가되면 `is_satisfied_by` 메서드의 조건문을 추가해야 하며, 새로운 할인 조건이 새로운 데이터를 요구하면 인스턴스 변수도 추가해야 한다.
    - 순번 조건을 판단하는 로직이 변경되면 `_is_satisfied_by_sequence` 메서드의 내부 구현을 수정해야 하며, 순번 조건을 판단하는 데 필요한 데이터가 변경되면 `DiscountCondition.sequence` 역시 변경되어야 한다.
    - 기간 조건을 판단하는 로직이 변경되면 `_is_satisfied_by_period` 메서드의 내부 구현을 수정해야 하며, 기간 조건을 판단하는 데 필요한 데이터가 변경되면 `DiscountCondition`의 `_day_of_week`, `_start_time`, `_end_time` 등도 변경해야 한다.
  - 변경의 이유에 따라 클래스를 분리해야한다.
    - `DiscountCondition`은 하나 이상의 변경 이유를 가지기 때문에 응집도가 낮다.
    - 응집도가 낮다는 것은 서로 연관성 없는 기능이나 데이터가 하나의 클래스에 뭉쳐져 있다는 것을 의미한다.
    - 따라서 낮은 응집도가 초래하는 문제를 해결하기 위해 변경의 이유에 따라 클래스를 분리해야 한다.
  - `DiscountCondtion`의 초기화 시점 살펴보기
    - 순번 조건을 표현하는 경우 `_sequence`는 초기화되지만, `_day_of_week`, `_start_time`, `_end_time`은 초기화되지 않는다.
    - 반면에 기간 조건을 표현하는 경우 `_day_of_week`, `_start_time`, `_end_time`은 초기화되지만, `_sequence`는 초기화되지 않는다.
    - 클래스의 속성이 서로 다른 시점에 초기화되거나 일부만 초기화된다는 것은 응집도가 낮다는 증거다.
    - 따라서 초기화되는 속성을 기준으로 코드를 분리해야한다.
  - `DiscountCondition`의 메서드들이 인스턴스 변수를 사용하는 방식 살펴보기
    - `_is_satisfied_by_sequence` 메서드와 `_is_satisfied_by_period` 메서드는 서로 다른 속성들을 사용한다.
    - 즉 `_is_satisfied_by_sequence`는 `_sequence`는 사용하지만 `_day_of_week`, `_start_time`, `_end_time`은 사용하지 않고,   `_is_satisfied_by_period`는 `_day_of_week`, `_start_time`, `_end_time`은 사용하지만 `_sequence`는 사용하지 않는다.
    - 따라서 속성 그룹과 해당 그룹에 접근하는 메서드 그룹을 기준으로 코드를 분리해야 한다.



- 변경 보호 패턴 적용을 위한 분리

  - `DiscountCondition`을 분리한다.
    - `DiscountCondition`의 가장 큰 문제는 순번 조건과 기간 조건이라는 두 개의 독립적인 타입이 하나의 클래스 안에 공존하고 있다는 점이다.
    - 두 개의 서로 다른 변경이 두 개의 서로 다른 클래스 안으로 캡슐화되도록 두 개의 클래스로 분리한다.

  ```python
  class PeriodCondition:
  
      def __init__(self, day_of_week: str=None, start_time: time=None, end_time: time=None):
          self._day_of_week = day_of_week
          self._start_time = start_time
          self._end_time = end_time
  
      def _is_satisfied_by(self, screening: Screening):
          return screening._when_screened.weekday() == self._day_of_week and \
                 self._start_time <= screening._when_screened() and \
                 self._end_time >= screening._when_screened()
  
  
  class SequenceCondition:
      
      def __init__(self, sequence: int=None):
          self._sequence = sequence
  
      def _is_satisfied_by(self, screening: Screening):
          return self._sequence == screening._sequence
  ```

  - 클래스를 변경하면 앞서 살펴본 문제점들이 모두 해결된다.
    - 두 개의 클래스는 자신의 모든 인스턴스 변수를 초기화한다.
    - 클래스 내의 모든 메서드는 동일한 인스턴스 변수 그룹을 사용한다.
    - 결과적으로 개별 클래스들의 응집도가 향상됐다.
  - 새로운 문제
    - 수정 전에는 `Movie`와 협력하는 클래스는 `DiscountCondition` 하나뿐이었다.
    - 그러나 수정 후에는 분리 된 두 개의 클래스 모두와 협력할 수 있어야 한다.
  - 새로운 문제를 해결하기 위한 적절하지 않은 방법
    - `Movie` 클래스 안에서 `SequenceCondtion`의 목록과 `PeriodCondition`의 목록을 따로 관리하면 된다고 생각할 수 있을 것이다.
    - 그러나 이는 `Movie`가 양쪽 클래스 모두와 결합되어 결합도가 증가한다. 
    - 또한 새로운 할인 조건을 추가하려면 `Movie`의 인스턴스 변수로 새로운 할인 조건의 목록을 추가해야 한다.
    - 그리고 새로운 할인 목록의 리스트를 이용해 할인 조건을 만족하는지 여부를 판단하는 메서드도 추가해야한다.
    - 마지막으로 이 메서드를 호출하도록 `is_discountable` 메서드를 수정해야한다.

  ```python
  class Movie:
      def __init__(self, title: str, running_time: time, fee: Money, movie_type: MovieType, 
                   discount_amount: Money, discount_percent: float,
                   period_conditions: list[PeriodCondition], sequence_conditions:list[SequenceCondition]):
          # ...
          self._period_conditions = period_conditions
          self._sequence_conditions = sequence_conditions
  
      def is_discountable(self, screening: Screening):
          return self._check_period_conditions(screening) or self._check_sequence_conditions(screening)
      
      def _check_period_conditions(self, screening: Screening):
          return any([discount_condition.is_satisfied_by(screening) 
                      for discount_condition in self._period_conditions])
  
      def _check_sequence_conditions(self, screening: Screening):
          return any([discount_condition.is_satisfied_by(screening) 
                      for discount_condition in self._sequence_conditions])
      
      # ...
  ```



- 변경 보호 패턴과 다형성 패턴 적용하기

  - 역할의 개념 적용하기
    - `Movie` 입장에서 보면 `SequenceCondition`과 `PeriodCondition`은 아무 차이도 없다.
    - 둘 모두 할인 여부를 판단하는 동일한 책임을 수행하고 있을 뿐이다.
    - 두 클래스가 할인 여부를 판단하기 위한 방법이 다르다는 사실은 `Movie` 입장에서는 그다지 중요하지 않다.
    - 할인 가능 여부를 반환해주기만 하면 `Movie`는 상관하지 않는다.
    - `Movie` 입장에서 `SequenceCondition`과 `PeriodCondition`이 동일한 책임을 수행한다는 것은 동일한 역할을 수행한다는 것을 의미한다.
    - 역할은 협력 안에서 대체 가능성을 의미하기 때문에 두 클래스에 역할의 개념을 적용하면 `Movie`가 구체적인 클래스는 알지 못한 채 오직 역할에 대해서만 결합되도록 의존성을 제한할 수 있다.
  - 역할을 사용하여 추상화하기
    - 역할을 사용하면 객체의 구체적인 타입을 추상화할 수 있다.
    - 역할을 대체할 클래스들 사이에 구현을 공유해야 한다면 추상 클래스를 사용하면 되고, 구현을 공유하지 않고 책임만 정의하고 싶다면 인터페이스를 사용하면 된다.

  ```python
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
  ```

  - `Movie`가 전송한 메시지를 수신한 객체의 구체적인 클래스가 무엇인지에 따라 적절한 메서드가 실행된다.
    - 즉 `Movie`와 `DiscountCondition` 사이의 협력은 다형적이다.
    - 이제 `Movie`는 협력하는 구체적인 타입을 몰라도 상관 없다.
    - 협력하는 객체가 `DiscountCondition` 역할을 수행할 수 있고, `is_satisfied_by` 메시지를 이해할 수 있다는 사실만 알고 있어도 충분하다.
  - 변경되기 쉬운 할인 조건이 `DiscountCondition`이라는 안정적인 인터페이스 뒤로 캡슐화되었다.



- `Movie` 클래스 개선하기

  - `Movie` 클래스의 문제점
    - 변경 이전의 `DiscountCondition`과 동일한 문제를 가지고 있다.
    - 금액 할인 정책 영화와 비율 할인 정책 영화라는 두 가지 타입을 하나의 클래스 안에 구현하고 있으므로, 하나 이상의 이유로 변경될 수 있다.
    - 즉 응집도가 낮다.
  - 개선 방법
    - `DiscountCondition`과 동일하게 역할의 개념을 도입하여 협력을 다형적으로 만든다.
    - 다형성 패턴을 사용하여 서로 다른 행동을 타입별로 분리하여 `Screening`과 `Movie`가 메시지를 통해서만 다형적으로 협력하게 하여 새로운 `Movie` type이 추가되더라도 `Screening`에 영향을 미치지 않게 할 수 있다.
    - 이는 변경 보호 패턴을 이용하여 타입의 종류를 안정적인 인터페이스 뒤로 캡슐화할 수 있다는 것을 의미한다.
  - `Movie` 클래스 수정하기
    - 금액 할인 정책과 비율 할인 정책, 그리고 할인 정책을 적용하지 않는 경우를 분리한다.
    - `DiscountCondition`의 경우에는 구현을 공유할 필요가 없으므로 인터페이스로 구현했으나, `Movie`의 경우에는 일부 구현을 공유해야 하므로 추상 클래스로 구현한다.
    - `_discount_amount`, `_discount_percent` 등의 인스턴스 변수와 이 변수를 사용하는 메서드들을 삭제한다.
    - 할인 금액을 계산하는 메서드를 추상 메서드로 선언한다.

  ```python
  class Movie(ABC):
  
      def __init__(self, title: str, running_time: time, fee: Money, discount_conditions: list[DiscountCondition]):
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
  ```

  - `Movie`를 상속 받는 클래스들을 작성한다.

  ```python
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
  ```

  - 위와 같이 책임 중심 설계로 변경한 결과
    - 변경 결과 모든 클래스의 내부 구현은 캡슐화 되고, 모든 클래스는 변경의 이유를 오직 하나씩만 가진다.
    - 각 클래스는 응집도가 높고 다른 클래스와 최대한 느슨하게 결합되어 있다.
    - 클래스는 오직 한 가지 일만 수행하며 책임은 적절하게 분배되어 있다.



- 변경과 유연성

  - 설계를 주도하는 것은 변경이다.
  - 개발자로서 변경에 대비할 수 있는 방법은 두 가지가 있다.
    - 하나는 코드를 이해하기 쉽도록 최대한 단순하게 설계하는 것이다.
    - 다른 하나는 코드를 수정하지 않고도 변경을 수용할 수 있도록 코드를 더 유연하게 만드는 것이다.
    - 대부분의 경우 전자가 더 좋은 방법이지만 유사한 변경이 반복적으로 발생한다면 복잡성이 증가하더라도 유연성을 추가하는 두 번째 방법이 더 좋다.

  - 상속과 영화 예매 시스템
    - 영화에 설정된 할인 정책을 실행 중에 변경할 수 있어야 한다는 요구사항이 추가되었다.
    - 현재의 설계에서는 할인 정책을 구현하기 위해 상속을 이용하고 있기 때문에 실행 중에 영화의 할인 정책을 변경하기 위해서는 새로운 인스턴스를 생성한 후 필요한 정보를 복사해야 한다.
    - 또한 변경 전후의 인스턴스가 개념적으로는 동일한 객체를 가리키지만 물리적으로 서로 다른 객체이기 때문에 식별자의 관점에서 혼란스러울 수 있다.
    - 새로운 할인 정책이 추가될 때 마다 인스턴스를 생성하고, 상태를 복사하고, 식별자를 관리하는 코드를 추가하는 일은 번거롭고 오류에 취약하다.
    - 따라서 코드의 복잡성이 높아지더라도 할인 정책의 변경을 쉽게 수용할 수 있게 코드를 유연하게 만드는 것이 더 좋은 방법이다.
  - 합성과 영화 예매 시스템
    - 마찬가지로 영화에 설정된 할인 정책을 실행 중에 변경할 수 있어야 한다는 요구사항이 추가되었다.
    - 상속 대신 합성을 이용하기 위해 기존에 `Movie`의 상속 계층 안에 구현된 할인 정책을 독립적인 `DiscountPolicy`로 분리한 후 `Movie`에 합성시킨다.
    - 상속을 이용한 설계에 비해 유연한 설계가 가능하다.
  - 합성을 사용하도록 코드를 수정하면 2장에서 봤던 코드와 동일한 구조가 된다.





## 책임 주도 설계의 대안

- 리팩터링(Refactoring)

  - 책임을 올바르게 할당하는 것은 어렵고 난해한 작업이다

    - 객체지향 프로그래밍 언어를 이용해 절차형 프로그램을 작성하는 대부분의 이유가 바로 책임 할당의 어려움에서 기인한다.

  - 책임 주도 설계에 익숙하지 않은 사람들은 아래와 같은 대안적인 방법을 사용하는 것도 좋다.

    - 먼저 빠르게 절차형 코드로 실행되는 프로그램을 작성한다.
    - 완성된 코드를 객체지향적인 코드로 변경한다.

    - 즉 일단 실행되는 코드를 얻고 난 후에 코드 상에 명확하게 드러나는 책임들을 올바른 위치로 이동시키는 것이다.
    - 이처럼 **이해하기 쉽고 수정하기 쉬운 소프트웨어로 개선하기 위해 겉으로 보이는 동작은 바꾸지 않은 채 내부 구조를 변경하는 것을 리팩터링**이라고 부른다.

  - 주의사항

    - 코드를 수정한 후에 겉으로 드러나는 동작이 바뀌어서는 안 된다.
    - 캡슐화를 향상시키고 응집도를 높이고, 결합도를 낮추면서도 동작은 그대로 유지해야한다.



- 메서드 응집도

  - 데이터 중심 설계로 작성된 코드를 책임 주도 설계로 작성된 코드처럼 변경하기
    - 데이터 중심으로 설계된 영화 예매 시스템에서 도메인 객체들은 단지 데이터의 집합일 뿐이며 영화 예매를 처리하는 모든 절차는 `ReservationAgency`에 집중되어 있었다.
    - 따라서 ReservationAgency에 포함된 로직들을 적절한 객체의 책임으로 분배하면 책임 주도 설계와 거의 유사한 결과를 얻을 수 있다.

  - 아래 코드는 3장 초반에 작성한 `ReservationAgency`의 코드이다.
    - 아래 코드에서 `reserve` method는 너무 길고 이해하기 어렵다.
    - 마이클 페더스는 아래와 같은 메서드를 몬스터 메서드(monster method)라 부른다.
    - 메서드의 응집도가 낮다고 표현할 수 있다.

  ```python
  class ReservationAgency:
      def reserve(self, screening: Screening, customer: Customer, audience_count: int):
          movie = screening.movie
  
          discountable = False
          for condition in movie.discount_conditions:
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

  - 긴 메서드는 아래와 같은 이유로 코드의 유지 보수에 악영향을 미친다.

    - 어떤 일을 수행하는지 한눈에 파악하기 어려워 코드를 이해하는 데 시간이 오래 걸린다.
    - 하나의 메서드 안에서 너무 많은 작업을 처리하기에 변경이 필요할 때 수정할 부분을 찾기 어렵다.
    - 메서드 내부의 일부 로직만 수정하더라도 나머지 부분에서 버그가 발생할 확률이 높다.
    - 로직의 일부만 재사용하는 것이 불가능하다.
    - 코드를 재사용하는 유일한 방법은 원하는 코드를 복사해서 붙여넣는 것 뿐이므로 코드 중복을 초래하기 쉽다.

  - 메서드의 응집도를 높여야 하는 이유

    - 클래스의 응집도를 높이는 이유와 같이 메서드의 응집도를 높이는 이유도 변경과 관련이 깊다.
    - 즉 변경을 수용할 수 있는 코드를 만들기 위해서이다.
    - 응집도 높은 메서드는 변경되는 이유가 단 하나여야 한다.

    - 메서드가 잘게 나뉘어져 있으므로 다른 메서드에서 사용될 확률이 높다.
    - 고수준의 메서드를 볼 때 마치 주석들을 나열한 것처럼 보이기 때문에 코드를 이해하기도 쉽다.

  - 객체에게 책임을 분배할 때 가장 먼저 할 일은 메서드를 응집도 있는 수준으로 분해하는 것이다.

    - 긴 메서드를 작고 응집도 있는 메서드로 분리하면 각 메서드를 적절한 클래스로 이동하기가 더 수월해지기 때문이다.



- `ReservationAgency` 리팩터링하기

  - 위에서 살펴본 대로 메서드를 응집도 있는 수준으로 분해하는 것에서 시작한다.
    - `reserve` 메서드를 응집도 있는 메서드들로 분해한다.
    - 이제 각 메서드들은 하나의 작업만 수행하고, 하나의 변경 이유만 가진다.
    - 비록 클래스의 길이는 더 길어졌지만 일반적으로 명확성의 가치가 클래스의 길이보다 중요하다.

  ```python
  class ReservationAgency:
      
      def reserve(self, screening: Screening, customer: Customer, audience_count: int):
          discountable = self._check_discountable(screening)
          fee = self._calculate_fee(screening, discountable, audience_count)
          return self._create_reservation(screening, customer, audience_count, fee)
  
      def _check_discountable(self, screening: Screening):
          return any([self._is_discountable(discount_condition, screening) 
                      for discount_condition in screening.movie.discount_conditions])
      
      def _is_discountable(self, condition: DiscountCondition, screening: Screening):
          if condition.type_ == DiscountConditionType.PERIOD:
              return self._is_satisfied_by_period(condition, screening)
      
      def _is_satisfied_by_period(self, condition, screening: Screening):
          return screening.when_screen.weekday() == condition.day_of_week \
                  and condition.start_time <= screening.when_screen \
                  and condition.end_time >= screening.when_screen
      
      def _is_satisfied_by_sequence(self, condition, screening: Screening):
          return condition.sequence == screening.sequence
      
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
  ```

  - 수정 후의  `reserve` 메서드
    - 수정 후의  `reserve` 메서드는 이제 상위 수준의 명세를 읽는 것 같은 느낌이 든다.
    - 이제 메서드가 어떤 일을 하는지 한 눈에 알아볼 수 있다.
    - 심지어 메서드의 구현이 주석을 모아놓은 것처럼 보이기까지 한다.
  - 남아 있는 문제점
    - 각 메서드들의 응집도는 높아졌지만 `ReservationAgency`의 응집도는 아직도 낮다.
    - 응집도를 높이기 위해서는 변경의 이유가 다른 메서드들을 적절한 위치로 분배해야 한다.
    - 적절한 위치란 바로 각 메서드가 사용하는 데이터를 정의하는 클래스를 의미한다.

  - 객체를 자율적으로 만드는 방법
    - **어떤 메서드를 어떤 클래스로 이동시킬지 결정하기 위해서는 객체가 자율적인 존재여야 한다는 사실을 떠올리면 된다.**
    - **자신이 소유하고 있는 데이터를 자기 스스로 처리하도록 만드는 것이 자율적인 객체를 만드는 지름길이다.**
    - 따라서 메서드가 사용하는 데이터를 저장하고 있는 클래스로 메서드를 이동시킨다.
  - 코드에 적용하기
    - `_is_discountable` 메서드는 `DiscountCondition`의 `type_`을 확인하여 타입에 따라 각기 다른 메서드를 호출한다.
    - `_is_discountable`가 호출하는 `_is_satisfied_by_period`, `_is_satisfied_by_sequence` 역시 `DiscountCondition`의 내부 데이터를 사용한다.
    - 따라서 이 메서드들이 사용하는 데이터를 가진 클래스인 `DiscountCondition`으로 이동시킨다.
    - 이제, `is_discountable`은 외부에서 호출해야 하므로 private에서 public으로 변경한다.
    - 또한 기존에 `DiscountCondition`에 있던 모든 접근자 메서드를 제거한다.
    - `ReservationAgency`는 이제 접근자 메서드가 아닌 메시지를 통해서만 `DiscountCondition`과 협력한다.
    - 결국 `ReservationAgency`의 응집도는 높어지고, `DiscountCondition`의 캡슐화가 증진되었으며, 둘 사이의 결합도는 낮아지게 된다.

  ```python
  class DiscountCondition:
      def __init__(self, type_: DiscountConditionType, sequence: int, 
                   day_of_week: str, start_time: time, end_time: time):
          self._type = type_
          self._sequence = sequence
          self._day_of_week = day_of_week
          self._start_time = start_time
          self._end_time = end_time
      
      def is_discountable(self, screening: Screening):
          if self.type_ == DiscountConditionType.PERIOD:
              return self._is_satisfied_by_period(screening)
      
      def _is_satisfied_by_period(self, screening: Screening):
          return screening.when_screen.weekday() == self._day_of_week \
                  and self._start_time <= screening.when_screen \
                  and self._end_time >= screening.when_screen
      
      def _is_satisfied_by_sequence(self, screening: Screening):
          return self._sequence == screening.sequence
  
      
  class ReservationAgency:
      # ...
  	
      # 이제 DiscountCondition 객체와 is_discountable 메시지를 통해 협력한다.
      def _check_discountable(self, screening: Screening):
          return any([discount_condition.is_discountable(screening)
                      for discount_condition in screening.movie.discount_conditions])
      
      # ...
  ```







# 핵심

- 책임은 객체의 입장이 아니라 객체가 참여하는 협력에 적합해야 한다.



- 객체가 메시지를 선택하는 것이 아니라 메시지가 객체를 선택하게 해야 한다.



- 메시지가 객체를 선택하도록 책임 주도 설계의 방식을 따르면 캡슐화와 낮은 결합도라는 목표를 비교적 손 쉽게 달성할 수 있다.
