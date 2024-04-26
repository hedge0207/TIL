# 상속과 코드 재사용

- 중복 코드

  - 중복 코드의 문제점
    - 중복 코드는 변경을 방해하며, 이것이 중복 코드를 제거해야 하는 가장 크 이유다.
    - 어떤 코드가 중복인지를 찾아야 하고, 찾은 후에는 찾아낸 모든 코드를 일관되게 수정해야 한다.
    - 모든 중복 코드를 개별적으로 테스트해서 동일한 결과를 내놓는지 확인해야만 한다.

  - 중복 여부 판단
    - 중복 여부를 판단하는 기준은 변경이다.
    - 요구사항이 변경됐을 때 두 코드를 함께 수정해야 한다면 이 코드는 중복이다.
    - 중복 코드를 결정하는 기준은 코드의 모양이 아니다.
    - 모양이 유사하다는 것은 단지 중복의 징후일 뿐이며, 중복 여부를 결정하는 기준은 코드가 변경에 반응하는 방식이다.

  - DRY(Don't Repeat Yourself) 원칙
    - 모든 지식은 시스템 내에서 단일하고, 애매하지 않고, 정말로 믿을 만한 표현 양식을 가져야 한다는 원칙으로 핵심은 코드 안에 중복이 존재해선 안 된다는 것이다.
    - 엔드류 헌트와 데이비드 토마스가 처음 소개했다.
    - 한 번, 단 한번(Once and Only Once) 원칙 또는 단일 지점 제어(Single-Point Control)원칙이라고도 부른다.
  - 중복 코드는 새로운 중복 코드를 부른다.
    - 중복 코드를 제거하지 않은 상태에서 코드를 수정할 수 있는 유일한 방법은 새로운 중복 코드를 추가하는 것뿐이다.
    - 새로운 중복 코드를 추가하는 과정에서 코드의 일관성이 무너질 위험이 항상 도사리고 있다.
    - 더 큰 문제는 중복 코드가 들어날수록 애플리케이션은 변경에 취약해지고 버그가 발생할 가능성이 높어진다는 것이다.



- 중복과 변경

  - 중복 코드의 문제점을 이해하기 위해 간단한 애플리케이션을 개발할 것이다.
    - 한 달에 한 번씩 가입자별로 전화 요금을 계산하는 애플리케이션이다.
    - 전화 요금을 계산하는 규칙은 통화 시간을 단위 시간당 요금으로 나눠 주는 것이다.

  - `Call` 클래스를 구현한다.
    - 개별 통솨 시간을 저장하기 위한 클래스이다.

  ```python
  from datetime import datetime
  
  
  class Call:
      def __init__(self, from_: datetime, to: datetime):
          self.from_ = from_
          self.to = to
      
      def get_duration(self):
          return self.to-self.from_
  ```

  - `Phone` 클래스를 구현한다.
    - 통화 요금을 계산할 객체다.
    - 전체 통화 목록에 대해 알고 있는 정보 전문가에게 요금을 계산할 책임을 할당해야 하는데, 일반적으로 통화 목록은 전화기 안에 보관되므로 `Phone` 클래스에게 맡긴다.
    - `_amount`에는 단위 요금을, `_seconds`에는 단위 시간이 저장된다.

  ```python
  class Phone:
      def __init__(self, amount: Money, seconds: int):
          self._amount = amount
          self._seconds = seconds
          self._calls = []
  
      def call(self, call: Call):
          self._calls.append(call)
  
      def calculate_fee(self) -> Money:
          result = Money.wons(0)
          for call in self._calls:
              result = result.plus(self._amount.times(call.get_duration().total_seconds() / self._seconds))
          return result
  
  if __name__ == "__main__":
      # 10초당 요금이 5원인 요금제에 가입한 사용자가
      phone = Phone(Money.wons(5), 10)
      # 1시간 30분간 전화를 했을 때의 요금
      phone.call(Call(datetime(2024, 11, 11, 10, 30, 0), datetime(2024, 11, 11, 12)))
      print(phone.calculate_fee()._amount)
  ```

  - 요구사항이 변경되어 심야 할인 요금제가 생겼다.

    - 밤 10시 이후의 통화에 대해 요금을 할인해주는 방식이다.

    - 이를 반영하기 위해 `Phone`의 코드를 복사해서 `NightlyDiscountPhone`이라는 새로운 클래스를 만든다.
    - `_nightly_amount`에는 밤 10시 이후 적용할 통화 요금이, `_regular_amount`에는 밤 10시 전에 적용될 통화 요금이 저장된다.

  ```python
  class NightlyDiscountPhone:
  
      LATE_NIGHT_HOUR = 22
  
      def __init__(self, nightly_amount: Money, regular_amount: Money, seconds: int):
          self._nightly_amount = nightly_amount
          self._regular_amount = regular_amount
          self._seconds = seconds
          self._calls: List[Call] = []
  
      def call(self, call: Call):
          self._calls.append(call)
  
      def calculate_fee(self) -> Money:
          result = Money.wons(0)
          for call in self._calls:
              if call._from.hour >= self.LATE_NIGHT_HOUR:
                  result = result.plus(self._nightly_amount.times(call.get_duration().total_seconds() / self._seconds))
              else:
                  result = result.plus(self._regular_amount.times(call.get_duration().total_seconds() / self._seconds))
          return result
  
  
  if __name__ == "__main__":
      phone = NightlyDiscountPhone(Money.wons(1), Money.wons(5), 10)
      phone.call(Call(datetime(2024, 11, 11, 22, 30, 0), datetime(2024, 11, 12)))
      print(phone.calculate_fee()._amount)
  ```

  - 중복 코드 변경하기
    - `Phone`의 코드를 복사한 후 일부 수정해서 `NightlyDiscountPhone` 클래스를 만들었기에 둘 사이에 중복 코드가 생기게 되었다.
    - 이 상황에서 통화 요금에 부과할 세금을 계산해야 한다는 요구사항이 추가되었다.
    - 현재 통화 요금을 계산하는 로직은 두 클래스 모두에 구현되어 있기 때문에 세금을 추가하기 위해서는 두 클래스를 함께 수정해야 한다.

  ```python
  class Phone:
      def __init__(self, amount: Money, seconds: int, tax_rate: float):
          self._amount = amount
          self._seconds = seconds
          self._tax_rate = tax_rate
          self._calls: List[Call] = []
  
      def call(self, call: Call):
          self._calls.append(call)
  
      def calculate_fee(self) -> Money:
          result = Money.wons(0)
          for call in self._calls:
              result = result.plus(self._amount.times(call.get_duration().total_seconds() / self._seconds))
          return result.plus(result.times(self._tax_rate))
  
  
  class NightlyDiscountPhone:
  
      LATE_NIGHT_HOUR = 22
  
      def __init__(self, nightly_amount: Money, regular_amount: Money, seconds: int, tax_rate: float):
          self._nightly_amount = nightly_amount
          self._regular_amount = regular_amount
          self._seconds = seconds
          self._tax_rate = tax_rate
          self._calls: List[Call] = []
  
      def call(self, call: Call):
          self._calls.append(call)
  
      def calculate_fee(self) -> Money:
          result = Money.wons(0)
          for call in self._calls:
              if call._from.hour >= self.LATE_NIGHT_HOUR:
                  result = result.plus(self._nightly_amount.times(call.get_duration().total_seconds() / self._seconds))
              else:
                  result = result.plus(self._regular_amount.times(call.get_duration().total_seconds() / self._seconds))
          return result.minus(result.times(self._tax_rate))
  ```

  - 일어날 수 있는 실수들
    - 위 코드에서 `Phone`에는 세금을 더했지만, `NightlyDiscountPhone`에는 세금을 뺐다.
    - 이처럼 중복 코드가 있을 경우 중복 코드를 서로 다르게 수정하는 경우가 있을 수 있다.
    - 또한 실수로 중복 코드들 중 일부만 수정하고 일부는 수정하지 않는 경우도 있을 수 있다.



- 상속을 이용한 중복 코드 제거

  - 상속의 기본 아이디어
    - 이미 존재하는 클래스와 유사한 클래스가 필요하다면 코드를 복사하지 말고 상속을 이용해 코드를 재사용하라는 것이다.
    - 따라서 상속을 이용하여 위 문제를 해결할 수 있다.
    - 그러나 상속을 염두에 두고 설계되지 않은 클래스를 상속을 이용해 재사용하는 것은 생각처럼 쉽지 않다.
  - 상속을 이용하도록 변경하기
    - 세금 부과는 안 한다고 가정한다.
    - 먼저 `Phone` 클래스의 `calculate_fee` 메서드로 일반 요금제에 따라 요금을 계산한 후, 만약 밤 10시 이후라면, 할인 받는 만큼을 일반 요금제로 계산된 금액에서 빼준다.
    - 이렇게 구현된 이유는 `Phone`을 최대한 재사용하고자 했기 때문이다.
    - 그러나, 이는 직관에 어긋난다.
    - 일반적으로 이 코드를 볼 때는 10시 이전의 요금에서 10시 이후의 차감하는 것이 아니라 10시 이전의 요금과 10시 이후의 요금을 더해서 전체 요금을 계산하는 것을 기대할 것이다.
    - 그러나, 이 코드는 먼저 10시 이전의 요금을 구한 후, 만약 10시 이후 요금에 따라 계산해야 한다면, 할인 금액 만큼을 빼는 방식을 사용하고 있다.

  ```python
  class NightlyDiscountPhone(Phone):
  
      LATE_NIGHT_HOUR = 22
  
      def __init__(self, nightly_amount: Money, regular_amount: Money, seconds: int):
          super(self).__init__(regular_amount, seconds)
          self._nightly_amount = nightly_amount
  
      def call(self, call: Call):
          self._calls.append(call)
  
      def calculate_fee(self) -> Money:
          result = super(self).calculate_fee()
  
          nighlty_fee = Money.wons(0)
          for call in self._calls:
              if call._from.hour >= self.LATE_NIGHT_HOUR:
                  nighlty_fee = nighlty_fee.plus(self._amount.minus(self._nightly_amount).times(call.get_duration().total_seconds() / self._seconds))
          
          return result.minus(nighlty_fee)
  ```

  - 상속은 부모 클래스와 자식 클래스를 강하게 결합시킨다.
    - 상속을 이용해 코드를 재사용하기 위해서는 부모 클래스의 개발자가 세웠던 가정이나 추론 과정을 정확히 히해해야 한다.
    - 이는 자식 클래스의 작성자가 부모 클래스의 구현 방법에 대한 정확한 지식을 가져야 한다는 것을 의미한다.
    - 따라서 상속은 결합도를 높이고, 이는 코드를 수정하기 어렵게 만든다.
  - `Phone`과 `NightlyDiscountPhone`은 강하게 결합되어 있다.
    - `NightlyDiscountPhone.calculate_fee`는 부모 클래스의 `calculate_fee`를 호출한다.
    - 즉 `NightlyDiscountPhone.calculate_fee`는 자신이 오버라이딩한 `Phone.calculate_fee` 메서드가 모든 통화 요금에 대한 요금의 총합을 반환한다는 사실에 기반하고 있다.
    - 만약 이 때 세금을 부과하는 요구사항이 추가된다고 가정해보자.
    - `NightlyDiscountPhone`는 생성자에서 전달 받은 `tax_rate`을 부모 클래스의 생성자로 전달해야 하며, `Phone`과 동일하게 값을 반환할 때 `tax_rate`을 이용해 세금을 부과해야 한다.
    - `NightlyDiscountPhone`를 `Phone`의 자식 클래스로 만든 이유는 `Phone`의 코드를 재사용하기 위함이었음에도 변경 사항을 수용하기 또 다시 중복 코드를 만들게 된다.
    - 이는 부모 클래스와 자식 클래스가 너무 강하게 결합되어 있기 때문이다.

  ```python
  class Phone:
      def __init__(self, amount: Money, seconds: int, tax_rate: float):
          self._amount = amount
          self._seconds = seconds
          self._tax_rate = tax_rate
          self._calls: List[Call] = []
  
      def call(self, call: Call):
          self._calls.append(call)
  
      def calculate_fee(self) -> Money:
          result = Money.wons(0)
          for call in self._calls:
              result = result.plus(self._amount.times(call.get_duration().total_seconds() / self._seconds))
          return result.plus(result.times(self._tax_rate))
  
  
  class NightlyDiscountPhone(Phone):
  
      LATE_NIGHT_HOUR = 22
  
      def __init__(self, nightly_amount: Money, regular_amount: Money, seconds: int, tax_rate: float):
          super(self).__init__(regular_amount, seconds, tax_rate)
          self._nightly_amount = nightly_amount
  
      def call(self, call: Call):
          self._calls.append(call)
  
      def calculate_fee(self) -> Money:
          result = super(self).calculate_fee()
  
          nighlty_fee = Money.wons(0)
          for call in self._calls:
              if call._from.hour >= self.LATE_NIGHT_HOUR:
                  nighlty_fee = nighlty_fee.plus(self._amount.minus(self._nightly_amount).times(call.get_duration().total_seconds() / self._seconds))
          
          return result.minus(nighlty_fee.plus(nighlty_fee.times(self._tax_rate)))
  ```





## 취약한 기반 클래스 문제

- 취약한 기반 클래스 문제(Fragile Base Class Problem, Brittle Base Class problem)
  - 상속 관계로 연결된 자식 클래스가 부모 클래스의 변경에 취약해지는 현상을 의미한다.
    - 취약한 기반 클래스 문제는 코드 재사용을 목적으로 상속을 사용할 때 발생하는 가장 대표적인 문제다.
    - 상속을 사용한다면 피할 수 없는 객치제향 프로그래밍의 근본적인 취약성이다.
    - 겉보기에는 안전한 방식으로 기반 클래스를 수정한 것처럼 보이더라도 이 새로운 행동이 파생 클래스에게 상속될 경우 파생 클래스의 잘못된 동작을 초래할 수 있기 때문에 기반 클래스는 취약하다.
    - 단순히 기반 클래스의 메서드들만을 조사하는 것만으로는 기반 클래스를 변경하는 것이 안전하다고 확신할 수 없다.
    - 모든 파생 클래스들을 살펴봐야한다.
  - 상속이라는 문맥 안에서 결합도가 초래하는 문제점을 가리키는 용어다.
    - 상속은 자식 클래스를 점진적으로 추가해서 기능을 확장하는 데는 용이하지만 높은 결합도로 인해 부모 클래스를 점진적으로 개선하는 것은 어렵게 만든다.
    - 취약한 기반 클래스 문제는 캡슐화를 약화시키고 결합도를 높인다.
    - 상속은 자식 클래스가 부모 클래스의 구현 세부사항에 의존하게 만들기 때문에 캡슐화를 약화시킨다.
    - 따라서 상속을 이용하면 부모 클래스의 퍼블릭 인터페이스가 아닌 구현을 변경하더라도 자식 클래스가 영향을 받기 쉬워진다.



- 불필요한 인터페이스 상속 문제
  - 상속받은 부모 클래스의 메서드가 자식 클래스의 내부 구조에 대한 규칙을 깨트릴 수 있다.
    - 부모 클래스에서 상속받은 메서드를 사용할 경우 자식 클래스의 규칙이 위반될 수 있다.
    - 예를 들어 아래와 같이 임의의 위치에 데이터를 추가하거나 삭제할 수 있는 메서드를 가진 클래스 `List`가 있다.
    - 가장 마지막에만 요소를 추가나 삭제를 할 수 있는 스택을 구현하기 위해 `Stack` 클래스를 생성하고, 마지막에 데이터를 추가하는 기능을 구현할 때, 임의의 위치에 데이터를 추가할 수 있는 `List`의 기능을 사용하기 위해 `List`를 상속 받도록 구현했다.
    - 문제는 `Stack`은 `List`를 상속 받았으므로 퍼블릭 인터페이스가 합쳐져 `Stack`에게 상속 된 `List`의 퍼블릭 인터페이스인 `insert` 사용하면 임의의 위치에서 요소를 추가하거나 삭제할 수 있다는 것이다.
    - 따라서 맨 마지막 위치에만 요소를 추가하거나 삭제해야 하는 Stack의 규칙을 쉽게 위반할 수 있다.
  
  ```python
  class List:
      def __init__(self):
          self._elements = []
  
      def insert(self, idx, element):
          self._elements.insert(idx, element)
          
  
  class Stack(List):
  
      def __str__(self):
          return str(self._elements)
      
      def push(self, element):
          self.insert(len(self._elements), element)
      
  
  stack = Stack()
  stack.push(1)
  stack.push(2)
  stack.insert(0, 3)
  print(stack)		# [3, 1, 2]
  ```
  
  - 인터페이스는 제대로 쓰기엔 쉽게, 엉터리로 쓰기엔 어렵게 만들어야 한다.
  - 퍼블릭 인터페이스에 대한 고려 없이 단순히 코드 재사용을 위해 상속을 이용하는 것은 매우 위험하다.
    - 단순히 코드를 재사용하기 위해 불필요한 오퍼레이션이 인터페이스에 스며들도록 방치해서는 안 된다.




- 메서드 오버라이딩의 오작용 문제

  - 자식 클래스가 부모 클래스의 메서드를 오버라이딩 할 경우 부모 클래스가 자신의 메서드를 사용하는 방법에 자식 클래스가 결합될 수 있다.
    - 아래 예시에서 `Parent` 클래스는 단순한 인사말을 출력하는 기능을 가지고 있다.
    - 각 메서드가 몇 번 호출되는지를 확인하고자 메서드 호출 횟수를 기록하기 위해 `Parent` 클래스를 상속받는 `Child` 클래스를 생성한다. 
    - `Child` 클래스에는 `cnt` 인스턴스 변수를 추가하고, 부모 클래스의 메서드를 오버라이딩하여 메서드가 호출될 때 마다 `cnt`를 1 증가시키고 원래 기능을 실행하기 위해 부모 클래스의 메서드를 호출한다.
    - 아래와 같이 `child.hello()`를 한 번 실행하면 `child.cnt`의 값이 1이 되야 할 것 같지만, 2가 출력되게 된다.
    - 이는 부모 클래스의 `hello`에서 `bye` 클래스를 호출하기 때문으로, 자식 클래스를 생성할 때 예상하지 못했던 오작용이다.
    - 예시는 매우 단순한 코드라 상대적으로 실수할 확률이 낮지만, 코드가 복잡해질수록 문제를 발견하기 힘들어진다.

  ```python
  class Parent:
      def bye(self):
          print("Bye!")
      
      def hello(self):
          print("Hello World!")
          self.bye()
          
  
  class Child(Parent):
      def __init__(self):
          self.cnt = 0
  
      def bye(self):
          print("Bye!")
          self.cnt += 1
  
      def hello(self):
          self.cnt += 1
          super().hello()
  
  child = Child()
  child.hello()
  print(child.cnt)		# 2
  ```

  - 클래스가 상속되기를 원한다면 상속을 위해 클래스를 설계하고 문서화해야 한다.
    - 내부 구현을 문서화하는 것은 캡슐화를 약화시킬 수 있으나, 이는 어쩔 수 없다.
    - 상속은 코드 재사용을 위해 캡슐화를 희생한다.
    - 완벽한 캡슐화를 원한다면 코드 재사용을 포기하거나 상속 이외의 방법을 사용해야 한다.



- 부모 클래스와 자식 클래스의 동시 수정 문제

  - 음악을 추가할 수 있는 플레이리스트를 구현할 것이다.
  - `Song`과 `Playlist` 클래스를 구현한다.

  ```python
  class Song:
      def __init__(self, title, singer):
          self._title = title
          self._singer = singer
      
      @property
      def title(self):
          return self._title
      
      @property
      def singer(self):
          return self._singer
  
  class PlayList:
      def __init__(self):
          self._tracks = list[Song]
      
      def append(self, song: Song):
          self._tracks.append(song)
  ```
  
  - 플레이리스트에서 음악을 삭제할 수 있는 기능 추가된 `PersonalPlaylist`가 필요해졌다.
    - `Playlist`를 상속 받아 구현한다.
  
  ```python
  class PersonalPlaylist(PlayList):
  
      def remove(self, song: Song):
          self._tracks.remove(song)
  ```
  
  - 요구사항이 변경되어 `Playlist`에서 노래의 목록뿐 아니라 가수별 노래의 제목을 함께 관리하게 되었다.
    - 노래를 추가한 후에 가수의 이름을 키로 노래의 제목을 추가하도록 `Playlist`의 `append` 메서드를 수정해야 한다.
  
  ```python
  class Playlist:
      def __init__(self):
          self._tracks = list[Song]
          self._singers = {}
      
      def append(self, song: Song):
          self._tracks.append(song)
          self._singers[song.singer] = song.title
  ```
  
  - 이에 따라 `PersonalPlaylist`도 함께 수정해야 한다.
    - `Playlist`의 `_tracks`에서 제거되면 `_singers`에서도 제거되어야 하기 때문이다.
  
  ```python
  class PersonalPlaylist(Playlist):
  
      def remove(self, song: Song):
          self._tracks.remove(song)
          del self._singers[song.singer]
  ```
  
  - 상속을 사용하면 자식 클래스가 부모 클래스의 구현에 강하게 결합된다.
    - 이 때문에 위 예시처럼 자식 클래스가 부모 클래스의 메서드를 오버라이딩하거나 불필요한 인터페이스를 상속받지 않았음에도 부모 클래스를 수정할 때 자식 클래스를 함께 수정해야 하는 상황이 발생하게 된다.
    - 상속은 기본적으로 부모 클래스의 구현을 재사용한다는 전제를 따르기 때문에 자식 클래스가 부모 클래스의 내부에 대해 자세히 알도록 강요한다.
  - 클래스를 상속하면 결합도로 인해 자식 클래스와 부모 클래스의 구현을 영원히 변경하지 않거나, 자식 클래스와 부모 클래스를 동시에 변경하거나 둘 중하나를 선택할 수밖에 없다.







## 상속 제대로 사용하기

- 추상화에 의존하기
  - `NightlyDiscountPhone`의 가장 큰 문제는 `Phone`에 강하게 결합되어 있다는 것이다.
  - 이 문제를 해결하는 가장 일반적인 방법은 자식 클래스가 보무 클래스의 구현이 아닌 추상화에 의존하도록 만드는 것이다.
    - 정확히 말하면 부모 클래스와 자식 클래스 모두 추상화에 의존하도록 수정해야 한다.



- 차이를 메서드로 추출하라

  - 중복 코드 안에서 차이점을 별도의 메서드로 추출한다.
    - 이는 "변하는 부분을 찾고 이를 캡슐화 하라"는 객체 지향의 원칙을 메서드에 적용한 것이다.
    - 상속을 사용하지 않은 코드에서 `Phone`과 `NightlyDiscountPhone`는 `calculate_fee`의 구현 방식에 차이가 있다.
    - 이 부분을 동일한 이름을 가진 메서드로 추출한다.

  ```python
  class Phone:
      
      def __init__(self, amount: Money, seconds: int):
          self._amount = amount
          self._seconds = seconds
          self._calls: List[Call] = []
  
      def calculate_fee(self) -> Money:
          result = Money.wons(0)
          for call in self._calls:
              result = result.plus(self.calculate_call_fee(call))
          return result
  
      def calculate_call_fee(self, call: Call) -> Money:
          return self._amount.times(call.get_duration().total_seconds() / self._seconds)
  ```

  - `NightlyDiscountPhone`에서도 동일한 방식으로 메서드를 추출한다.

  ```python
  class NightlyDiscountPhone:
  
      LATE_NIGHT_HOUR = 22
  
      def __init__(self, nightly_amount: Money, regular_amount: Money, seconds: int):
          self._nightly_amount = nightly_amount
          self._regular_amount = regular_amount
          self._seconds = seconds
          self._calls: List[Call] = []
  
      def calculate_fee(self) -> Money:
          result = Money.wons(0)
          for call in self._calls:
              result = result.plus(self._calculate_call_fee(call))
          
          return result.minus(result.times(self._tax_rate))
      
      def _calculate_call_fee(self, call: Call) -> Money:
          if call._from.hour >= self.LATE_NIGHT_HOUR:
              return self._nightly_amount.times(call.get_duration().total_seconds() / self._seconds)
          else:
              return self._regular_amount.times(call.get_duration().total_seconds() / self._seconds)
  ```

  - 두 클래스의 `calculate_fee`에서 차이가 나는 부분을 추출하여, 두 클래스의 `calculate_fee`가 완전히 동일해졌다.



- 중복 코드를 부모 클래스로 올려라.

  - 부모 클래스를 추가한다.
    - 부모 클래스에 `Phone`과 `NightlyDiscountPhone`의 공통 부분(`calculate_fee`)을 이동시킨다.
    - 그리고 이에 필요한 인스턴스 변수도 함께 이동시킨 후 필요한 메서드는 추상 메서드로 선언한다.

  ```python
  class AbstractPhone(ABC):
  
      def __init__(self):
          self._calls = []
  
      def calculate_fee(self) -> Money:
          result = Money.wons(0)
          for call in self._calls:
              result = result.plus(self._calculate_call_fee(call))
          return result
      
      @abstractmethod
      def _calculate_call_fee(sefl) -> Money:
          ...
  ```

  - 이제 `Phone`과 `NightlyDiscountPhone`이 추상 클래스를 상속받도록 변경한다.

  ```python
  class Phone(AbstractPhone):
      def __init__(self, amount: Money, seconds: int):
          self._amount = amount
          self._seconds = seconds
  
      def _calculate_call_fee(self, call: Call) -> Money:
          return self._amount.times(call.get_duration().total_seconds() / self._seconds)
  
  
  class NightlyDiscountPhone(AbstractPhone):
  
      LATE_NIGHT_HOUR = 22
  
      def __init__(self, nightly_amount: Money, regular_amount: Money, seconds: int):
          self._nightly_amount = nightly_amount
          self._regular_amount = regular_amount
          self._seconds = seconds
      
      def _calculate_call_fee(self, call: Call) -> Money:
          if call._from.hour >= self.LATE_NIGHT_HOUR:
              return self._nightly_amount.times(call.get_duration().total_seconds() / self._seconds)
          else:
              return self._regular_amount.times(call.get_duration().total_seconds() / self._seconds)
  ```

  - 위와 같이 공통된 부분을 부모 클래스로 옮기는 것을 "위로 올리기" 전략이라 부른다.
    - 이를 통해 추상화에 의존하는 코드를 작성할 수 있다.



- 추상화에 의존하도록 변경한 후에 얻은 이점들
  - 공통 코드를 이동시킨 후에 각 클래스는 서로 다른 변경의 이유를 가지게 되었다.
    - `AbstractPhone`은 전체 통화 목록을 계싼하는 방법이 바뀔 경우에만 변경된다.
    - `Phone`은 일반 요금제의 통화 한 건을 계산하는 방식이 바뀔 경우에만 변경된다.
    - `NightlyDiscountPhone`은 심야 할인 요금제의 통화 한 건을 계산하는 방식이 바뀔 경우에만 변경된다.
    - 이들은 단일 책임 원칙을 준수하기 때문에 응집도가 높다.
  - 자식 클래스는 부모 클래스의 구현에 의존하지 않게 되었다.
    - 자식 클래스인 `Phone`과 `NightlyDiscountPhone`은 부모 클래스인 `AbstractPhone`의 구체적인 구현에 의존하지 않는다.
    - 오직 부모 클래스에서 정의한 추상 메서드인 `calculate_call_fee`에만 의존한다.
    - `calculate_call_fee`의 시그니처가 변경되지 않는 한 부모 클래스의 내부 구현이 변경되더라도 자식 클래스는 영향을 받지 않는다.
    - 결과적으로 낮은 결합도를 가지게 된다.
  - 의존성 역전 원칙도 준수한다.
    - 요금 계산과 관련된 상위 수준의 정책을 구현하는 `AbstractPhone`이 세부적인 계산 로직을 구현하는 `Phone`과 `NightlyDiscountPhone`에 의존하지 않고 있다.
    - 반대로 `Phone`과 `NightlyDiscountPhone`이 추상화인 `AbstractPhone`에 의존한다.
  - 개방-폐쇄 원칙을 준수한다.
    - 새로운 요금제를 추가하기도 쉬워졌다.
    - 새로운 요금제가 발생한다면 `AbstractPhone`을 상속 받는 새로운 클래스를 추가한 후 `calculate_fee` 메서드만 오버라이딩하면 된다.



- 의도를 드러내는 이름 선택하기

  - 수정된 위 코드에서 한 가지 아쉬운 점이 있다면 클래스의 이름이다.
    - `NightlyDiscountPhone`은 심야 할인 요금제와 관련된 내용을 구현한다는 사실을 명확하게 전달하지만 `Phone`은 그렇지 못한다.
    - 또한 `AbstractPhone` 역시 모든 전화기를 포괄한다는 의미를 명확하게 전달하지 못 한다.
  - 따라서 아래와 같이 이름을 변경한다.

  ```python
  # AbstractPhone
  class Phone(ABC): ...
  # Phone
  class RegularPhone(Phone): ...
  ```



- 변경 사항 수용하기

  - 이전과 마찬가지로 요금에 세금을 부과해야 한다는 요구사항이 추가되었다.
    - 세금은 모든 요금제에 공통으로 적용되는 요구사항이므로 `Phone`에서 처리한다.

  ```python
  class Phone(ABC):
  
      def __init__(self, tax_rate: float):
          self._calls: List[Call] = []
          self._tax_rate = tax_rate
  
      def calculate_fee(self) -> Money:
          result = Money.wons(0)
          for call in self._calls:
              result = result.plus(self._calculate_call_fee(call))
          return result.plus(result.times(self._tax_rate))
  ```

  - 자식 클래스들의 생성자도 `tax_rate`을 받도록 수정한다.
    - 이처럼 책임을 잘 분배했더라도, 부모 클래스에 인스턴스 변수가 추가되면 자식 클래스에도 영향을 미치게 된다.

  ```python
  class RegularPhone(Phone):
      def __init__(self, amount: Money, seconds: int, tax_rate: float):
          super().__init__(tax_rate)
          self._amount = amount
          self._seconds = seconds
  
  class NightlyDiscountPhone(Phone):
      def __init__(self, nightly_amount: Money, regular_amount: Money, seconds: int, tax_rate: float):
          super().__init__(tax_rate)
          self._nightly_amount = nightly_amount
          self._regular_amount = regular_amount
          self._seconds = seconds
  ```



- 상속으로 인한 클래스 사이의 결합을 피할 수 있는 방법은 없다.
  - 상속은 자식 클래스가 부모 클래스의 행동뿐 아니라 인스턴스 변수에도 결합되게 만든다.
    - 인스턴스 변수의 목록이 변하지 않는 상황에서 객체의 행동만 변경된다면 상속 계층에 속한 각 클래스들을 독립적으로 진화시킬 수 있다.
    - 그러나 인스턴스 변수가 추가된다면 자식 클래스는 자신의 인스턴스를 생성할 때 부모 클래스에 정의된 인스턴스 변수를 초기화해야 하기 때문에 자연스럽게 부모 클래스에 추가된 인스턴스 변수는 자식 클래스의 초기화 로직에 영향을 주게 된다.
    - 결과적으로 책임을 아무리 잘 분리하더라도 인스턴스 변수의 추가는 종종 상속 계층 전반에 걸친 변경을 유발한다.
  - 상속은 어떤 방식으로든 부모 클래스와 자식 클래스를 결합시킨다.
    - 메서드 구현에 대한 결합은 추상 메서드를 추가함으로써 어느 정도 완화할 수 있다.
    - 그러나 인스턴스 변수에 대한 잠재젹인 결합을 제거할 수 있는 방법은 없다.



- 차이에 의한 프로그래밍(programming by difference)
  - 기존 코드와 다른 부분만을 추가함으로써 애플리케이션의 기능을 확장하는 방법이다.
    - 상속을 이용하면 이미 존재하는 클래스의 코드를 쉽게 재사용할 수 있기 때문에 애플리케이션의 점진적인 정의가 가능해진다.
  - 차이에 의한 프로그래밍의 목표는 중복 코드를 제거하고 코드를 재사용하는 것이다.
    - 사실 중복 코드 제거와 코드 재사용은 동일한 행동을 카리키는 서로 다른 단어다.
    - 중복을 제거하기 위해서는 코드를 재사용 가능한 단위로 분해하고 재구성해야 한다.
    - 코드를 재사용하기 위해서는 중복 코드를 제거해서 하나의 모듈로 모아야 한다.
  - 재사용 가능한 코드란 심각한 버그가 존재하지 않는 코드다.
    - 코드를 재사용 하는 것은 단순히 문자를 타이핑하는 수고를 덜어주는 수준의 문제가 아니다.
    - 코드를 재사용하면 코드의 품질은 유지하면서도 코드를 작성하는 노력과 테스트는 줄일 수 있다.
  - 상속은 강력한 도구다.
    - 객체지향 세계에서 중복 코드를 제거하고 코드를 재사용할 수 있는 가장 유명한 방법이다(그러나 가장 좋은 방법이지는 않을 수 있다).
    - 상속을 이용하면 새로운 기능을 추가하기 위해 직접 구현해야 하는 코드의 양을 최소화할 수 있다.
  - 그러나 상속의 오용과 남용은 애플리케이션을 이해하고 확장하기 어렵게 만든다.
    - 정말 필요한 경우에만 상속을 사용해야 한다.
    - 상속은 코드 재사용과 관련된 대부분의 경우에 우아한 해결 방법이 아니다.

