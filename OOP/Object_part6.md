# 상속과 코드 재사용

- 중복 코드

  - 중복 코드의 문제점
    - 중복 코드는 변경을 방해하며, 이것이 중복 코드를 제거해야 하는 가장 큰 이유다.
    - 어떤 코드가 중복인지를 찾아야 하고, 찾은 후에는 찾아낸 모든 코드를 일관되게 수정해야 한다.
    - 모든 중복 코드를 개별적으로 테스트해서 동일한 결과를 내놓는지 확인해야만 한다.

  - 중복 여부 판단
    - **중복 여부를 판단하는 기준은 변경이다.**
    - 요구사항이 변경됐을 때 두 코드를 함께 수정해야 한다면 이 코드는 중복이다.
    - 중복 코드를 결정하는 기준은 코드의 모양이 아니다.
    - **모양이 유사하다는 것은 단지 중복의 징후일 뿐이며, 중복 여부를 결정하는 기준은 코드가 변경에 반응하는 방식이다.**

  - **DRY(Don't Repeat Yourself) 원칙**
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
    - 개별 통화 시간을 저장하기 위한 클래스이다.

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
    - `_amount`에는 단위 요금이, `_seconds`에는 단위 시간이 저장된다.
  
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
  
  - 중복된 코드가 있는 상태에서 변경하기
    - `Phone`의 코드를 복사한 후 일부 수정해서 `NightlyDiscountPhone` 클래스를 만들었기에 둘 사이에 중복 코드가 생기게 되었다.
    - 이 상황에서 통화 요금에 부과할 세금을 계산해야 한다는 요구사항이 추가되었다.
    - 현재 통화 요금을 계산하는 로직은 두 클래스 모두에 구현되어 있기 때문에 세금을 추가하기 위해서는 두 클래스를 함께 수정해야 한다.
    - 두 클레스의 `calculate_fee` 메서드를 모두 수정한다.
  
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
    - `calculate_fee` 메서드를 수정하면서 `Phone`에는 세금을 더했지만, `NightlyDiscountPhone`에는 세금을 뺐다.
    - 이처럼 중복 코드가 있을 경우 중복 코드를 서로 다르게 수정하는 경우가 있을 수 있다.
    - 또한 실수로 중복 코드들 중 일부만 수정하고 일부는 수정하지 않는 경우도 있을 수 있다.



- 상속을 이용한 중복 코드 제거

  - 상속의 기본 아이디어
    - 이미 존재하는 클래스와 유사한 클래스가 필요하다면 코드를 복사하지 말고 상속을 이용해 코드를 재사용하라는 것이다.
    - 따라서 상속을 이용하여 위 문제를 해결할 수 있다.
    - 그러나 상속을 염두에 두고 설계되지 않은 클래스를 상속을 이용해 재사용하는 것은 생각처럼 쉽지 않다.
  - 상속을 이용하도록 변경하기
    - 세금 부과 이전의 상태를 가지고 변경한다.
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

  - **상속은 부모 클래스와 자식 클래스를 강하게 결합시킨다.**
    - **상속을 이용해 코드를 재사용하기 위해서는 부모 클래스의 개발자가 세웠던 가정이나 추론 과정을 정확히 이해해야 한다.**
    - 이는 자식 클래스의 작성자가 부모 클래스의 구현 방법에 대한 정확한 지식을 가져야 한다는 것을 의미한다.
    - 따라서 **상속은 결합도를 높이고, 이는 코드를 수정하기 어렵게 만든다.**
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

- **취약한 기반 클래스 문제(Fragile Base Class Problem, Brittle Base Class problem)**
  - **상속 관계로 연결된 자식 클래스가 부모 클래스의 변경에 취약해지는 현상**을 의미한다.
    - 취약한 기반 클래스 문제는 **코드 재사용을 목적으로 상속을 사용할 때 발생하는 가장 대표적인 문제**다.
    - 상속을 사용한다면 피할 수 없는 **객치제향 프로그래밍의 근본적인 취약성**이다.
    - 겉보기에는 안전한 방식으로 기반 클래스를 수정한 것처럼 보이더라도 이 새로운 행동이 파생 클래스에게 상속될 경우 파생 클래스의 잘못된 동작을 초래할 수 있기 때문에 기반 클래스는 취약하다.
    - 단순히 **기반 클래스의 메서드들만을 조사하는 것만으로는 기반 클래스를 변경하는 것이 안전하다고 확신할 수 없다.**
    - 모든 파생 클래스들을 살펴봐야한다.
  - 상속이라는 문맥 안에서 결합도가 초래하는 문제점을 가리키는 용어다.
    - 상속은 자식 클래스를 점진적으로 추가해서 기능을 확장하는 데는 용이하지만 높은 결합도로 인해 부모 클래스를 점진적으로 개선하는 것은 어렵게 만든다.
    - **취약한 기반 클래스 문제는 캡슐화를 약화시키고 결합도를 높인다.**
    - 상속은 자식 클래스가 부모 클래스의 구현 세부사항에 의존하게 만들기 때문에 캡슐화를 약화시킨다.
    - 따라서 상속을 이용하면 부모 클래스의 퍼블릭 인터페이스가 아닌 구현을 변경하더라도 자식 클래스가 영향을 받기 쉬워진다.



- **불필요한 인터페이스 상속** 문제
  
  - 부모 클래스로부터 상속받은 메서드가 자식 클래스의 내부 구조에 대한 규칙을 깨트릴 수 있다.
    - 부모 클래스로부터 상속받은 메서드를 사용할 경우 자식 클래스의 규칙이 위반될 수 있다.
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
  
  - 인터페이스는 올바로 쓰기엔 쉽게, 엉터리로 쓰기엔 어렵게 만들어야 한다.
  - **퍼블릭 인터페이스에 대한 고려 없이 단순히 코드 재사용을 위해 상속을 이용하는 것은 매우 위험하다.**
    - 단순히 코드를 재사용하기 위해 불필요한 오퍼레이션이 인터페이스에 스며들도록 방치해서는 안 된다.




- **메서드 오버라이딩의 오작용** 문제

  - 자식 클래스가 부모 클래스의 메서드를 오버라이딩 할 경우 **부모 클래스가 자신의 메서드를 사용하는 방법에 자식 클래스가 결합될 수 있다.**
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
    - **상속은 코드 재사용을 위해 캡슐화를 희생한다.**
    - 완벽한 캡슐화를 원한다면 코드 재사용을 포기하거나 상속 이외의 방법을 사용해야 한다.



- **부모 클래스와 자식 클래스의 동시 수정** 문제

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
  
  - 플레이리스트에서 음악을 삭제할 수 있는 기능이 추가된 `PersonalPlaylist`가 필요해졌다.
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

- **추상화에 의존하기**
  - `NightlyDiscountPhone`의 가장 큰 문제는 `Phone`에 강하게 결합되어 있다는 것이다.
  - 이 문제를 해결하는 가장 일반적인 방법은 **자식 클래스가 부모 클래스의 구현이 아닌 추상화에 의존하도록 만드는 것**이다.
    - 정확히 말하면 **부모 클래스와 자식 클래스 모두 추상화에 의존하도록 수정**해야 한다.



- 차이를 메서드로 추출하라

  - 중복 코드 안에서 차이점을 별도의 메서드로 추출한다.
    - 이는 "변하는 부분을 찾고 이를 캡슐화 하라"는 객체 지향의 원칙을 메서드에 적용한 것이다.
    - 상속을 사용하지 않은 코드에서 `Phone`과 `NightlyDiscountPhone`는 `calculate_fee`의 구현 방식에 차이가 있다.
    - 이 부분을 동일한 이름을 가진 메서드(`_calculate_call_fee`)로 추출한다.

  ```python
  class Phone:
      
      def __init__(self, amount: Money, seconds: int):
          self._amount = amount
          self._seconds = seconds
          self._calls: List[Call] = []
  
      def calculate_fee(self) -> Money:
          result = Money.wons(0)
          for call in self._calls:
              result = result.plus(self._calculate_call_fee(call))
          return result
  
      def _calculate_call_fee(self, call: Call) -> Money:
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



- 중복 코드를 추상 클래스로 올려라.

  - 추상 클래스를 추가한다.
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

  - 위와 **같이 공통된 부분을 부모 클래스로 옮기는 것을 "위로 올리기" 전략**이라 부른다.
    - 이를 통해 추상화에 의존하는 코드를 작성할 수 있다.



- 추상화에 의존하도록 변경한 후에 얻은 이점들
  - **공통 코드를 이동시킨 후에 각 클래스는 서로 다른 변경의 이유를 가지게 되었다.**
    - `AbstractPhone`은 전체 통화 목록을 계산하는 방법이 바뀔 경우에만 변경된다.
    - `Phone`은 일반 요금제의 통화 한 건을 계산하는 방식이 바뀔 경우에만 변경된다.
    - `NightlyDiscountPhone`은 심야 할인 요금제의 통화 한 건을 계산하는 방식이 바뀔 경우에만 변경된다.
    - 이들은 단일 책임 원칙을 준수하기 때문에 응집도가 높다.
  - 자식 클래스는 부모 클래스의 구현에 의존하지 않게 되었다.
    - 자식 클래스인 `Phone`과 `NightlyDiscountPhone`은 부모 클래스인 `AbstractPhone`의 구체적인 구현에 의존하지 않는다.
    - 오직 부모 클래스에서 정의한 추상 메서드인 `calculate_call_fee`에만 의존한다.
    - `calculate_call_fee`의 시그니처가 변경되지 않는 한 부모 클래스의 내부 구현이 변경되더라도 자식 클래스는 영향을 받지 않는다.
    - 결과적으로 낮은 결합도를 가지게 된다.
  - **의존성 역전 원칙도 준수한다.**
    - 요금 계산과 관련된 상위 수준의 정책을 구현하는 `AbstractPhone`이 세부적인 계산 로직을 구현하는 `Phone`과 `NightlyDiscountPhone`에 의존하지 않고 있다.
    - 반대로 **`Phone`과 `NightlyDiscountPhone`이 추상화인 `AbstractPhone`에 의존**한다.
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
    - 이처럼 **책임을 잘 분배했더라도, 부모 클래스에 인스턴스 변수가 추가되면 자식 클래스에도 영향을 미치게 된다.**

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



- **상속으로 인한 클래스 사이의 결합을 피할 수 있는 방법은 없다.**
  - **상속은 자식 클래스가 부모 클래스의 행동뿐 아니라 인스턴스 변수에도 결합되게 만든다.**
    - 인스턴스 변수의 목록이 변하지 않는 상황에서 객체의 행동만 변경된다면 상속 계층에 속한 각 클래스들을 독립적으로 진화시킬 수 있다.
    - 그러나 인스턴스 변수가 추가된다면 자식 클래스는 자신의 인스턴스를 생성할 때 부모 클래스에 정의된 인스턴스 변수를 초기화해야 하기 때문에 자연스럽게 부모 클래스에 추가된 인스턴스 변수는 자식 클래스의 초기화 로직에 영향을 주게 된다.
    - 결과적으로 **책임을 아무리 잘 분리하더라도 인스턴스 변수의 추가는 종종 상속 계층 전반에 걸친 변경을 유발한다.**
  - **상속은 어떤 방식으로든 부모 클래스와 자식 클래스를 결합시킨다.**
    - 메서드 구현에 대한 결합은 추상 메서드를 추가함으로써 어느 정도 완화할 수 있다.
    - 그러나 **인스턴스 변수에 대한 잠재적인 결합을 제거할 수 있는 방법은 없다.**



- **차이에 의한 프로그래밍(programming by Difference)**
  - 기존 코드와 다른 부분만을 추가함으로써 애플리케이션의 기능을 확장하는 방법이다.
    - 상속을 이용하면 이미 존재하는 클래스의 코드를 쉽게 재사용할 수 있기 때문에 애플리케이션의 점진적인 정의가 가능해진다.
  - **차이에 의한 프로그래밍의 목표는 중복 코드를 제거하고 코드를 재사용하는 것이다.**
    - 사실 중복 코드 제거와 코드 재사용은 동일한 행동을 카리키는 서로 다른 단어다.
    - 중복을 제거하기 위해서는 코드를 재사용 가능한 단위로 분해하고 재구성해야 한다.
    - 코드를 재사용하기 위해서는 중복 코드를 제거해서 하나의 모듈로 모아야 한다.
  - 재사용 가능한 코드란 심각한 버그가 존재하지 않는 코드다.
    - 코드를 재사용 하는 것은 단순히 문자를 타이핑하는 수고를 덜어주는 수준의 문제가 아니다.
    - 코드를 재사용하면 코드의 품질은 유지하면서도 코드를 작성하는 노력과 테스트는 줄일 수 있다.
  - 상속은 강력한 도구다.
    - 객체지향 세계에서 중복 코드를 제거하고 코드를 재사용할 수 있는 가장 유명한 방법이다(그러나 가장 좋은 방법인 것은 아닐 수 있다).
    - 상속을 이용하면 새로운 기능을 추가하기 위해 직접 구현해야 하는 코드의 양을 최소화할 수 있다.
  - 그러나 **상속의 오용과 남용은 애플리케이션을 이해하고 확장하기 어렵게 만든다.**
    - 정말 필요한 경우에만 상속을 사용해야 한다.
    - **상속은 코드 재사용과 관련된 대부분의 경우에 우아한 해결 방법이 아니다.**







# 합성과 유연한 설계

- 상속과 합성

  - 상속과 합성은 객체지향 프로그래밍에서 가장 널리 사용되는 코드 재사용 기법이다.
    - 상속은 is-a 관계라고 부른다.
    - 합성은 has-a 관계라고 부른다.
  - 코드 재사용에서의 차이
    - 상속은 부모 클래스와 자식 클래스를 연결해서 부모 클래스의 코드를 재사용한다.
    - 합성은 전체를 표현하는 객체가 부분을 표현하는 객체를 포함해서 부분 코드의 객체를 재사용한다.
    - 상속은 부모 클래스 안에 구현된 코드 자체를 재사용한다.
    - **합성은 포함되는 객체의 퍼블릭 인터페이스를 재사용한다.**
  - 의존성 해결 시점에서의 차이
    - 상속에서 부모 클래스와 자식 클래스 사이의 의존성은 컴파일타임에 해결된다.
    - **합성에서 두 객체 사이의 의존성은 런타임에 해결된다.**

  - 상속은 자식 클래스와 부모 클래스 사이의 결합도를 높인다.
    - 상속을 제대로 활용하기 위해서는 부모 클래스의 내부 구현에 대해 상세하게 알아야 하기 때문이다.
    - 결과적으로 상속은 코드를 재사용할 수 잇는 쉽고 간단한 방법이지만 우아한 방법은 아니다.
  - 합성은 상속과 달리 구현에 의존하지 않는다.
    - **합성은 내부에 포함되는 객체의 구현이 아닌 퍼블릭 인터페이스에 의존한다.**
    - 따라서 합성을 사용하면 포함된 객체의 내부 구현이 변경되더라도 영향을 최소화할 수 있기에 변경에 더 안정적인 코드를 얻을 수 있게 된다.
  - **상속 대신 합성을 사용하면 변경하기 쉽고 유연한 설계를 얻을 수 있다.**
    - 상속은 클래스 사이의 정적인 관계인데 반해 합성은 객체 사이의 동적인 관계다.
    - 코드 작성 시점에 결정한 상속 관계는 변경이 불가능하지만 합성 관계는 실행시에 동적으로 변경할 수 있다.



- 상속 대신 합성을 사용할 경우의 이점

  - 코드 재사용을 위해 상속을 남용했을 때 발생할 수 있는 세 가지 문제점은 아래와 같다.
    - 불필요한 인터페이스 상속
    - 메서드 오버라이딩 오작용
    - 부모 클래스와 자식 클래스 동시 수정
  - 합성을 사용하면 불필요한 인터페이스 상속 문제를 해결할 수 있다.
    - 이전 장에서 `List`를 상속한 `Stack`을 예시로 불필요한 인터페이스 상속 문제를 살펴봤다.
    - 해당 코드를 상속이 아닌 합성을 사용하도록 아래와 같이 변경했다.
    - `List`의 인스턴스를 `Stack`의 인스턴스 변수로 선언한다.
    - 이제 `Stack`의 퍼블릭 인터페이스에는 불필요한 `List`의 오퍼레이션이 포함되지 않는다.
    - 따라서 마지막 위치에만 요소를 추가할 수 있다.

  ```python
  class List:
      def __init__(self):
          self._elements = []
  
      def insert(self, idx, element):
          self._elements.insert(idx, element)
  
      @property
      def elements(self):
          return self._elements
          
  
  class Stack:
      def __init__(self, list_: List):
          self._list = list_
  
      def __str__(self):
          return str(self._list.elements)
      
      def push(self, element):
          self._list.insert(len(self._list.elements), element)
      
  
  stack = Stack(List())
  stack.push(1)
  stack.push(2)
  try:
      stack.insert(0, 3)
  except Exception as e:
      print(e)			# 'Stack' object has no attribute 'insert'
  print(stack)			# [1, 2]
  ```

  - 합성을 이용하면 메서드 오버라이딩 오작용 문제를 해결할 수 있다.
    - 이전 장에서 `Parent` 클래스와 `Child` 클래스를 통해 상속시에 발생할 수 있는 메서드 오버라이딩 오작용에 대해 살펴봤다.
    - 이 역시 합성을 이용하면 해결이 가능하다.

  ```python
  class Parent:
      def bye(self):
          print("Bye!")
      
      def hello(self):
          print("Hello World!")
          self.bye()
          
  
  class Child:
      def __init__(self, parent: Parent):
          self.cnt = 0
          self._parent = parent
  
      def bye(self):
          print("Bye!")
          self.cnt += 1
  
      def hello(self):
          self.cnt += 1
          self._parent.hello()
  
  child = Child(Parent())
  child.hello()
  print(child.cnt)		# 1
  ```

  - **합성을 사용하더라도 부모 클래스와 자식 클래스의 동시 수정 문제는 해결할 수 없다.**
    - 앞 장에서 살펴본 변경을 수용하기 위해 `Playlist`와 `PersonalPlaylist`를 함께 수정해야 하는 문제는 해결되지 않는다.
    - 그럼에도 상속보다는 합성이 더 나은데, 그 이유는 변경에 의한 파급효과를 최대한 `PersonalPlaylist` 내부로 캡슐화할 수 있기 때문이다.

  ```python
  class Playlist:
      def __init__(self):
          self._tracks = list[Song]
          self._singers = {}
  
      @property
      def tracks(self):
          return self._tracks
      
      @property
      def singer(self):
          return self._singers
      
      def append(self, song: Song):
          self._tracks.append(song)
          self._singers[song.singer] = song.title
  
  class PersonalPlaylist:
  
      def __init__(self, playlist: Playlist):
          self._playlist = playlist
  
      def append(self, song: Song):
          self._playlist.append(song)
  
      def remove(self, song: Song):
          self._playlist.tracks.remove(song)
          del self._playlist.singer[song.singer]
  ```





## 상속으로 인한 조합의 증가

- 상속으로 인해 결합도가 높아지면 코드를 수정하는 데 필요한 작업의 양이 과도하게 늘어날 수 있다.
  - 가장 일반적인 상황은 작은 기능들을 조합해서 더 큰 기능을 수행하는 객체를 만들어야 하는 경우다.
  - 일반적으로 다음과 같은 두 가지 문제가 발생한다.
    - 하나의 기능을 추가하거나 수정하기 위해 불필요하게 많은 수의 클래스를 추가하거나 수정해야 한다.
    - 단일 상속만 지원하는 언어에서 상속으로 인해 오히려 중복 코드의 양이 늘어날 수 있다.
  - 합성을 사용하면 상속으로 인해 발생하는 클래스의 증가와 중복 코드 문제를 해결할 수 있다.



- 기본 정책과 부가 정책 조합하기
  - 이전 장에서 봤던 핸드폰 과금 시스템에 새로운 요구사항을 추가한다.
    - 현재 시스템에는 일반 요금제와 할인 요금제라는 두 가지 요금제가 존재한다.
    - 새로운 요구 사항은 이 두 요금제에 부가 정책을 추가하는 것이다.
    - 지금부터는 핸드폰 요금제가 기본 정책과 부가 정책을 조합해서 구성된다.
    - 기본 정책은 가입자의 통화 정보를 기반으로 하며, 한달 통화량을 기준으로 부과할 요금을 계산한다.
    - 부가 정책은 통화량과 무관하게 기본 정책체 선택적으로 추가할 수 있는 요금 방식을 의미하며, 이전 장에서 봤던 세금이 이에 해당한다.
    - 세금과 관련된 부가 정책을 세금 정책, 최종 계산된 요금에서 일정 금액을 할인해주는 부가 정책을 할인 정책이라 부른다.
  - 부가 정책은 아래와 같은 특성을 가진다.
    - 기본 정책의 계산 결과에 적용된다.
    - 선택적으로 적용할 수 있다.
    - 조합 가능하다(여러 개의 부가 정책을 함께 적용하는 것도 가능하다).
    - 부가 정책은 임의의 순서로 적용이 가능하다.
  - 결국 현재의 기본 정책 2개와 부가 정책 2개를 조합하면 총 10개의 조합이 가능하다.
    - 일반요금제
    - 심야할인요금제
    - 일반요금제 - 세금 정책
    - 일반요금제 - 할인 정책
    - 일반요금제 - 세금 정책 - 할인 정책
    - 일반요금제 - 할인 정책 - 세금 정책
    - ...



- 상속을 이용해서 기본 정책 구현하기

  - 아래 코드는 기존 코드에서 세금을 더하는 부분만 제외한 것이다.
  - `RegularPhone` 또는 `NightlyDiscountPhone`의 인스턴스만 단독으로 생성한다는 것은 부가 정책은 적용하지 않고 기본 정책만으로 요금을 계산한다는 것을 의미한다.

  ```python
  class Phone(ABC):
  
      def __init__(self):
          self._calls: List[Call] = []
  
      def call(self, call: Call):
          self._calls.append(call)
  
      def calculate_fee(self) -> Money:
          result = Money.wons(0)
          for call in self._calls:
              result = result.plus(self._calculate_call_fee(call))
          return result
      
      @abstractmethod
      def _calculate_call_fee(sefl) -> Money:
          ...
      
      
  class RegularPhone(Phone):
      def __init__(self, amount: Money, seconds: int):
          self._amount = amount
          self._seconds = seconds
  
      def _calculate_call_fee(self, call: Call) -> Money:
          return self._amount.times(call.get_duration().total_seconds() / self._seconds)
  
      
  class NightlyDiscountPhone(Phone):
  
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



- 기본 정책에 세금 정책 조합하기

  - `RegularPhone` 클래스를 상속 받는 `TaxableRegularPhone` 클래스를 추가한다.
    - 부모 클래스의 `calculate_fee` 메서드를 오버라이딩하여 `super` 호출을 통해 부모 클래스에게 `calculatr_fee` 메시지를 전송한다.
    - `RegularPhone.calulcate_fee` 메서드는 일반 요금제 규칙에 따라 계산된 요금을 반환하므로 이 반환값에 세금을 부과해서 반환하면 일반 요금제와 세금 정책을 조합한 요금을 계산할 수 있다.

  ```python
  class TaxableRegularPhone(RegularPhone):
  
      def __init__(self, amount: Money, seconds: int, tax_rate: float):
          super().__init__(amount, seconds)
          self._tax_rate = tax_rate
  
      def calculate_fee(self) -> Money:
          fee = super().calculate_fee()
          return fee.plus(fee.times(self._tax_rate))
  ```

  - 위 방식의 문제점
    - `super`를 사용하는 방식은 원하는 결과를 쉽게 얻을 수는 있지만 자식 클래스와 부모 클래스의 결합도가 높아진다는 문제가 있다.
    - 결합도를 낮추기 위헤서는 자식 클래스가 부모 클래스의 메서드를 호출하지 않도록 부모 클래스에 추상 메서드를 제공하는 것이다.
  - `Phone` 클래스에 추상 메서드 추가하기
    - 부모 클래스가 자신이 정의한 추상 메서드를 호출하고 자식 클래스가 이 메서드를 오버라이딩해서 부모 클래스가 원하는 로직을 제공하도록 수정하여 결합도를 느슨하게 만든다.
    - 이 방법은 자식 클래스가 부모 클래스의 구현이 아니라 필요한 동작의 명세를 기술하는 추상화에 의존하도록 만든다.

  ```python
  class Phone(ABC):
  	
      def calculate_fee(self) -> Money:
          result = Money.wons(0)
          for call in self._calls:
              result = result.plus(self._calculate_call_fee(call))
          # 부모 클래스의 다른 메서드에서 자신이 정의한 추상 메서드를 호출하도록 만든다.
          return self._after_calculated(result)
      
      @abstractmethod
      def _after_calculated(self, fee: Money) -> Money:
          ...
  ```

  - 자식 클래스는 위에서 정의한 `after_calculated` 메서드를 오버라이딩한다.
    - 일반 요금제와 심야 할인 요금제는 요금을 수정할 필요가 없기에 인자로 받은 값을 그대로 반환하도록 한다.

  ```python
  class RegularPhone(Phone):
      # ...
      def _after_calculated(self, fee: Money):
          return fee
      
  class NightlyDiscountPhone(Phone):
      # ...
      def _after_calculated(self, fee: Money):
          return fee
  ```

  - 위 방식의 문제점
    - 부모 클래스에 추상 메서드를 추가하면 모든 자식 클래스들이 추상 메서드를 오버라이딩해야 한다.
    - 또한 모든 추상 메서드의 구현이 동일하다.
    - 유연성은 유지하면서도 중복 코드를 제거할 수 있는 방법은 `Phone`에서 `after_calculated` 메서드에 대한 기본 구현을 함께 제공하는 것이다.

  - `Phone.after_calculated`이 기본 구현을 제공하도록 수정한다.
    - 이제 자식 클래스들은 `after_calculated`를 오버라이딩 할 필요가 없다.

  ```python
  class Phone(ABC):
      
      def calculate_fee(self) -> Money:
          result = Money.wons(0)
          for call in self._calls:
              result = result.plus(self._calculate_call_fee(call))
          return self._after_calculated(result)
  
      # ...
      def _after_calculated(self, fee: Money) -> Money:
          return fee
      
  class RegularPhone(Phone):
      # ...
      # def _after_calculated(self, fee: Money):
      #     return fee
      
  class NightlyDiscountPhone(Phone):
      # ...
      # def _after_calculated(self, fee: Money):
      #     return fee
  ```

  - `TaxableRegularPhone`을 수정한다.
    - `_after_calculated` 메서드를 오버라이딩한 후 `fee`에 세금을 더해서 반환하도록 한다.

  ```python
  class TaxableRegularPhone(RegularPhone):
  
      def __init__(self, amount: Money, seconds: int, tax_rate: float):
          super().__init__(amount, seconds)
          self._tax_rate = tax_rate
      
      def _after_calculated(self, fee: Money) -> Money:
          return fee.plus(fee.times(self._tax_rate))
  ```

  - 심야 할인 요금제에도 세금을 부과할 수 있도록 `NightlyDiscountPhone`의 자식 클래스인 `TaxableNightlyDiscountPhone`을 추가한다.
    - `TaxableRegularPhone`와 중복 코드가 생기게 되었다.

  ```python
  class TaxableNightlyDiscountPhone(NightlyDiscountPhone):
  
      def __init__(self, nightly_amount: Money, regular_amount: Money, seconds: int, tax_rate: float):
          super().__init__(nightly_amount, regular_amount, seconds)
          self._tax_rate = tax_rate
  
      def _after_calculated(self, fee: Money) -> Money:
          return fee.plus(fee.times(self._tax_rate)) 
  ```



- **추상 메서드와 훅 메서드**

  - OCP를 만족하는 설계를 만들 수 있는 한 가지 방법은 **부모 클래스에 새로운 추상 메서드를 추가하고 부모 클래스의 다른 메서드 안에서 호출**하는 것이다.
    - 자식 클래스는 추상 메서드를 오버라이딩하고 자신만의 로직을 구현해서 부모 클래스에서 정의한 플로우에 개입할 수 있게 된다.
    - 처음에 `Phone` 클래스에 추상 메서드인 `_calculate_call_fee`와 `_after_calculated`를 선언하고 자식 클래스에서 두 메서드를 오버라이딩한 것 역시 이 방법을 사용한 것이다.

  ```python
  class Phone(ABC):
  
      def __init__(self):
          self._calls: List[Call] = []
  
      def call(self, call: Call):
          self._calls.append(call)
  	
      # 이 메서드에서 추상 메서드인 _calculate_call_fee 호출한다.
      def calculate_fee(self) -> Money:
          result = Money.wons(0)
          for call in self._calls:
              result = result.plus(self._calculate_call_fee(call))
          return result
      
      # 추상 메서드 선언
      @abstractmethod
      def _calculate_call_fee(sefl) -> Money:
          ...
  ```
  
  - **훅 메서드(hook method)**
    - 추상 메서드의 단점은 상속 계층에 속하는 모든 자식 클래스가 추상 메서드를 오버라딩해야 한다는 것이다.
    - 대부분의 자식 클래스가 추상 메서드를 동일한 방식으로 구현한다면 상속 계층 전반에 걸쳐 중복 코드가 존재하게 될 것이다.
    - 해결 방법은 메서드에 기본 구현을 제공하는 것이다.
    - 이처럼 **추상 메서드와 동일하게 자식 클래스에서 오버라이딩할 의도로 메서드를 추가했지만 편의를 위해 기본 구현을 제공하는 메서드를 훅 메서드라고 부른다.**
    - 아래 예시에서는 `_after_calculated`가 훅 메서드에 해당한다.
  
  ```python
  class Phone(ABC):
      
      def calculate_fee(self) -> Money:
          result = Money.wons(0)
          for call in self._calls:
              result = result.plus(self._calculate_call_fee(call))
          return self._after_calculated(result)
  
      # 오버라이딩할 의도로 메서드를 추가했지만, 편의를 위해 기본 구현은 제공한다.
      def _after_calculated(self, fee: Money) -> Money:
          return fee
  ```



- 기본 정책에 할인 정책 적용하기

  - 일반 요금제에 할인 정책을 조합하기 위해 `RateDiscountableRegularPhone` 클래스를 생성한다.

  ```python
  class RateDiscountableRegularPhone(RegularPhone):
  
      def __init__(self, amount: Money, seconds: int, discount_amount: Money):
          super().__init__(amount, seconds)
          self._discount_amount = discount_amount
  
      def _after_calculated(self, fee: Money) -> Money:
          return fee.minus(self._discount_amount)
  ```

  - 심야 할인 요금제에 할인 정책을 조합하기 위해 `RateDiscountableNightlyDiscountPhone` 클래스를 생성한다.
    - 마찬가지로 `RateDiscountableRegularPhone` 코드와 중복 코드가 생성됐다.

  ```python
  class RateDiscountableNightlyDiscountPhone(NightlyDiscountPhone):
  
      def __init__(self, nightly_amount: Money, regular_amount: Money, seconds: int, discount_amount: Money):
          super().__init__(nightly_amount, regular_amount, seconds)
          self._discount_amount = discount_amount
  
      def _after_calculated(self, fee: Money) -> Money:
          return fee.minus(self._discount_amount)
  ```



- 중복 코드의 덫

  - 상속을 이용한 해결 방법은 모든 가능한 조합별로 자식 클래스를 하나씩 추가하는 것이다.
    - 만약 일반 요금제의 계산 결과에 세금 정책을 조합한 후 할인 정책을 추가하고 싶다면 아래와 같이 `TaxableRegularPhone`을 상속 받는 새로운 자식 클래스를 생성해야 한다.
    - 만약 심야 할인 요금제의 계산 결과에 할인 정책을 조합한 후 세금 정책을 추가하고 싶다면 `RateDiscountableNightlyDiscountPhone`를 상속 받는 새로운 자식 클래스를 생성해야 한다.

  ```python
  class TaxableAndRateDiscountableRegualarPhone(TaxableRegularPhone):
      
      def __init__(self, amount: Money, seconds: int, tax_rate: float, discount_amount: Money):
          super().__init__(amount, seconds, tax_rate)
          self._discount_amount = discount_amount
  
      def _after_calculated(self, fee: Money) -> Money:
          return super()._after_calculated(fee).minus(self._discount_amount)
  ```

  - 이 방식의 문제점은 새로운 정책을 추가하기 어렵다는 것이다.
    - 현재의 설계에 새로운 정책을 추가하기 위해서는 불필요하게 많은 수의 클래스를 상속 계층 안에 추가해야 한다.
    - 만약 새로운 기본 정책이 추가 된다면 새로운 기본 정책 클래스를 포함하여 5개의 새로운 클래스가 추가되어야 한다.
    - 마찬가지로 새로운 부가 정책이 추가된다면 또 다시 많은 수의 클래스가 추가되어야 한다.
  - **클래스 폭발(Class Explosion)**
    - 이처럼 상속의 남용으로 하나의 기능을 추가하기 위해 필요 이상으로 많은 수의 클래스를 추가해야 하는 경우를 클래스 폭발 혹은 조합의 폭발(combinational explosion) 문제라고 부른다.
    - **클래스 폭발 문제는 자식 클래스가 부모 클래스의 구현에 강하게 결합되도록 강요하는 상속의 근본적인 한계 때문에 발생하는 문제다.**
    - **컴파일 타임에 결정된 자식 클래스와 부모 클래스 사이의 관계는 변경될 수 없기 때문**에 자식 클래스와 부모 클래스의 다양한 조합이 필요한 상황에서 유일한 해결 방법은 조합의 수만큼 새로운 클래스를 추가하는 것뿐이다.
  - 클래스 폭발은 새로운 기능을 추가할 때뿐만 아니라 기능을 수정할 때도 문제가 된다.
    - 만약 세금 정책을 변경해야 한다면 세금 정책과 관련된 여러 클래스에 중복된 코드를 모두 찾아 동일한 방식으로 수정해야 한다.
    - 이 클래스 중에 하나라도 누락된다면 버그가 발생하게 될 것이다.





## 합성 관계로 변경하기

- 합성을 사용하면 클래스 폭발 문제를 해결할 수 있다.
  - 상속 관계는 컴파일타임에 결정되고 고정된다.
    - 따라서 코드를 실행하는 도중에는 변경할 수 없다.
    - 여러 기능을 조합해야 하는 설계에서 상속을 이용하면 모든 조합 가능한 경우별로 클래스를 추가해야 한다.
    - 이는 클래스 폭발 문제를 야기한다.
  - **합성은 컴파일타임 관계를 런타임 관계로 변경함으로써 클래스 폭발 문제를 해결한다.**
    - **합성을 사용하면 구현이 아닌 퍼블릭 인터페이스에 대해서만 의존할 수 있기 때문에 런타임에 객체의 관계를 변경할 수 있다.**
    - **컴파일타임 의존성과 런타임 의존성이 멀수록 설계가 유연해진다.**
    - 상속이 조합의 결과를 개별 클래스 안으로 밀어 넣는 방법이라면 합성은 조합을 구성하는 요소들을 개별 클래스로 구현한 후 실행 시점에 인스턴스를 조립하는 방법을 사용하는 것이다.
  - 컴파일 의존성에 속박되지 않고 다양한 방식의 런타임 의존성을 구성할 수 있다는 것이 합성이 제공하는 가장 커다란 장점이다.



- 기본 정책 합성하기

  - 기본 정책과 부가 정책을 포괄하는 `RatePolicy` 인터페이스를 추가한다.
    - `Phone`을 인자로 받아 계산된 요금을 반환하는 `calculate_fee` 오퍼레이션을 포함한다.

  ```python
  class RatePolicy(ABC):
      
      @abstractmethod
      def caclulate_fee(self, phone: Phone):
          ...
  ```

  - 기본 정책 구현하기
    - 기본 정책에 속하는 일반 요금제와 심야 할인 요금제는 개별 요금을 계산하는 방식을 제외한 전체 처리 로직이 거의 동일하다.
    - 중복 코드를 담을 추상 클래스를 생성한다.

  ```python
  class BasicRatePolicy(RatePolicy):
  
      def caclulate_fee(self, phone: Phone):
          result = Money.wons(0)
  
          for call in phone.calls:
              result = result.plus(self._calculate_call_fee(call))
          
          return result
      
      @abstractmethod
      def _calculate_call_fee(self, call: Call):
          ...
  ```

  - 일반 요금제를 구현한다.
    - 추상 클래스인 `BasicRatePolicy`의 자식 클래스로 구현한다.

  ```python
  class RegularPolicy(BasicRatePolicy):
      
      def __init__(self, amount: Money, seconds: int):
          self._amount = amount
          self._seconds = seconds
  
      def _calculate_call_fee(self, call: Call):
          return self._amount.times(call.get_duration().total_seconds() / self._seconds)
  ```

  - 심야 할인 요금제를 구현한다.
    - 마찬가지로 추상 클래스인 `BasicRatePolicy`의 자식 클래스로 구현한다.

  ```python
  class NightlyDiscountPolicy(BasicRatePolicy):
  
      LATE_NIGHT_HOUR = 22
      
      def __init__(self, nightly_amount: Money, regular_amount: Money, seconds: int):
          self._nightly_amount = nightly_amount
          self._regular_amount = regular_amount
          self._seconds = seconds
  
      def _calculate_call_fee(self, call: Call):
          if call._from.hour >= self.LATE_NIGHT_HOUR:
              return self._nightly_amount.times(call.get_duration().total_seconds() / self._seconds)
          else:
              return self._regular_amount.times(call.get_duration().total_seconds() / self._seconds)
  ```

  - 기본 정책을 이용해 요금을 계산할 수 있도록 `Phone`을 수정한다.
    - `Phone` 내부에 `RatePolicy`에 대한 참조자가 포함되어 있는데, 이것이 바로 합성이다.
    - 또한 다양한 요금 정책과 협력할 수 있어야 하므로 `RatePolicy`라는 인터페이스로 정의되어 있다.
    - `Phone`은 이 컴파일타임 의존성을 구체적인 런타임 의존성으로 대체하기 위해 생성자를 통해 `RatePolicy`에 대한 의존성을 주입받는다.
    - 이처럼 다양한 종류의 객체와 협력하기 위해 합성 관계를 사용하는 경우에는 합성하는 개체의 타입을 인터페이스나 추상 클래스로 선언하고 의존성 주입을 사용해 런타임에 필요한 객체를 설정할 수 있도록 구현하는 것이 일반적이다.

  ```python
  class Phone(ABC):
  	
      # 의존성을 주입 받는다.
      def __init__(self, rate_policy: RatePolicy):
          self._calls: List[Call] = []
          self._rate_policy = rate_policy
  
      def call(self, call: Call):
          self._calls.append(call)
  
      def calculate_fee(self) -> Money:
          self._rate_policy.calculate_fee(self)
  
      @property
      def calls(self):
          return self._calls
  ```
  
  - 예시
    - 일반 요금제의 규칙에 따라 통화 요금을 계산하고 싶다면 `Phone`과 `RegularPolicy`의 인스턴스를 합성하면 된다.
    - 심야 할인 요금제의 규칙에 따라 통화 요금을 계산하고 싶다면 `Phone`과 `NightlyDiscountPolicy`의 인스턴스를 합성하면 된다.
  
  ```python
  phone = Phone(RegularPolicy(Money(10), 10))
  phone = Phone(NightlyDiscountPolicy(Money(5), Money(10), 10))
  ```



- 부가 정책 적용하기

  - 부가 정책은 아래와 같은 제약 사항이 있다.
    - 부가 정책은 기본 정책이나 다른 부가 정책의 인스턴스를 참조할 수 있어야 한다. 즉 부가 정책의 인스턴스는 어떤 종류의 정책과도 합성될 수 있어야 한다.
    - `Phone`의 입장에서는 자신이 기본 정책의 인스턴스에게 메시지를 전송하고 있는지, 부가 정책의 인스턴스에게 메시지를 전송하고 있는지를 몰라야 한다. 즉 기본 정책과 부가 정책은 협력 안에서 동일한 역할을 수행해야 한다.
  - 부가 정책을 구현한다.
    - 부가 정책은 `RatePolicy` 인터페이스를 구현하는 방식으로 구현한다.
    - 이는 기본 정책과 부가 정책이 협력 안에서 **동일한 역할을 수행**해야 하기 때문이다.
    - 즉 `Phone`의 입장에서 `AdditionalRatePolicy`는 `RatePolicy`의 역할을 수행하기 때문이다.
    - `AdditionalRatePolicy` 역시 마찬가지로 컴파일타임 의존성을 런타임 의존성으로 쉽게 대체할 수 있도록 `RatePolicy` 타입의 인스턴스를 인자로 받는 생성자를 제공하여 의존성을 주입 받는다.

  ```python
  class AdditionalRatePolicy(RatePolicy):
  
      def __init__(self, next_: RatePolicy):
          self._next = next_
  
      def calculate_fee(self, phone: Phone):
          fee = self._next.calculate_fee(phone)
          return self._after_calculated(fee)
      
      @abstractmethod
      def _after_calculated(self, fee: Money):
          ...
  ```

  - 세금 정책을 구현한다.
    - `AdditionalRatePolicy`를 상속 받아 구현한다.

  ```python
  class TaxablePolicy(AdditionalRatePolicy):
      
      def __init__(self, tax_ratio: float, next_: RatePolicy):
          super().__init__(next_)
          self._tax_ratio = tax_ratio
  
      def _after_calculated(self, fee: Money):
          return fee.plus(fee.times(self._tax_ratio))
  ```

  - 할인 정책을 구현한다.
    - `AdditionalRatePolicy`를 상속 받아 구현한다.

  ```python
  class RateDiscountPolicy(AdditionalRatePolicy):
  
      def __init__(self, amount: Money, next_: RatePolicy):
          super().__init__(next_)
          self._amount = amount
      
      def _after_calculated(self, fee: Money):
          return fee.minus(self._amount)
  ```



- 기본 정책과 부가 정책 합성하기

  - 일반 요금제에 할인 정책을 조합한 결과에 세금 정책을 조합하기

  ```python
  phone = Phone(TaxablePolicy(0.02, RateDiscountPolicy(Money.wons(10), RegularPolicy(Money(10), 10))))
  ```

  - 심야 할인 요금제에 세금 정책을 조합한 결과에 할인 정책을 조합하기

  ```python
  phone = Phone(RateDiscountPolicy(Money.wons(10), TaxablePolicy(0.02, NightlyDiscountPolicy(Money(5), Money(10), 10))))
  ```

  - 이처럼 클래스를 새로 추가하지 않고도 예측 가능하고 일관성 있는 조합이 가능하다.



- **객체 합성이 상속 보다 더 좋은 방법이다.**
  - **상속은 구현을 재사용하는 데 비해 합성은 객체의 인터페이스를 재사용한다.**
  - 다만 이는 구현 상속에 해당하는 이야기로, 앞에서 살펴본 단점들은 모두 구현 상속에 국한되는 것들이다.
    - 인터페이스 상속의 경우 다를 수 있다.





## 믹스인

- 믹스인(Mixin)
  - 객체를 생성할 때 코드 일부를 클래스 안에 섞어 넣어 재사용하는 기법이다.
    - 합성이 실행 시점에 객체를 조합하는 재사용 방법이라면 믹스인은 컴파일 시점에 필요한 코드 조각을 조합하는 재사용 방법이다.
  - 상속과의 차이
    - 상속을 사용하여 부모 클래스의 코드를 재사용할 수 있기는 하지만 상속의 진정한 목적은 자식 클래스를 부모 클래스와 동일한 개념적 범주로 묶어 is-a 관계를 만드는 것이다.
    - 반면 믹스인은 말 그대로 코드를 다른 코드 안에 섞어 넣기 위한 방법이다.
    - 상속이 클래스와 클래스 사이의 관계를 고정시키는 데 비해 믹스인은 유연하게 관계를 재구성할 수 있다.



- 정책 구현하기

  - 기본 정책 구현하기

  ```python
  class BasicRatePolicy(ABC):
      def calculate_fee(self, phone: Phone) -> Money:
          result = Money.wons(0)
          for call in phone.calls:
              result = result.plus(self._calculate_call_fee(call))
          return result
  
      @abstractmethod
      def _calculate_call_fee(self, call) -> Money:
          pass
  
  
  class RegularPolicy(BasicRatePolicy):
      def __init__(self, amount: Money, seconds: int):
          self.amount = amount
          self.seconds = seconds
  
      def _calculate_call_fee(self, call: Call) -> Money:
          return self.amount.times(call.get_duration().total_seconds() / self.seconds)
      
  
  class NightlyDiscountPolicy(BasicRatePolicy):
  
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

  - 부가 정책 구현하기

  ```python
  class TaxablePolicy(BasicRatePolicy):
      
      def __init__(self, tax_ratio: float):
          self._tax_ratio = tax_ratio
  
      def calculate_fee(self, phone: Phone):
          fee: Money = super().calculate_fee(phone)
          return fee.plus(fee.times(self._tax_ratio))
  
  
  class RateDiscountPolicy(BasicRatePolicy):
  
      def __init__(self, discount_amount: Money):
          self._discount_amount = discount_amount
  
      def calculate_fee(self, phone: Phone):
          fee: Money = super().calculate_fee(phone)
          return fee.minus(self._discount_amount)
  ```

  - 상속과의 차이

    - 부가 정책은 `BasicRatePolicy`를 상속받고, `calculate_fee` 안에서 `super`를 통해 부모 클래스의 메서드를 호출한다.
    - 그러나, 이는 상속과 다르다.
    - `BasicRatePolicy`를 상속 받는 것은 믹스인 될 문맥을 제한하기 위한 것이지 상속 그 자체를 위한 것이 아니다.
    - 부가 정책을 `BasicRatePolicy`를 상속 받은 클래스에만 믹스인 될 수 있게 하기 위해 `BasicRatePolicy`를 상속 받는 것이다.
    - 또한 `super` 역시 단순한 상속에서 사용하는 방식과는 차이가 있다.
    - 상속을 사용한 방식에서 `super`는 부모 클래스로 고정되지만, 믹스인 방식에서 `super`는 믹스인 대상에 따라 달라질 수 있다.
    - 즉 `super`가 가리키는 대상이 믹스인 할 때 결정된다.
    - 예를 들어 부가 정책이 `RegularPolicy`와 믹스인 되면 `RegularPolicy.calculate_fee`가 호출 될 것이고,  `NightlyDiscountPolicy`와 믹스인 되면 `NightlyDiscountPolicy.calculate_fee`가 호출 될 것이다.

    - 이것이 믹스인이 상속보다 더 유연한 재사용 기법인 이유다.



- 믹스인 사용하기

  - Python의 경우 다중 상속을 통해 구현이 가능하다.
    - 다만 믹스인 자체를 위한 문법은 없기에 제약이 있을 수 있다.
  - 기본 요금 정책에 세금 정책을 적용하기

  ```python
  class TaxableRegularPolicy(TaxablePolicy, RegularPolicy):
      def __init__(self, amount: Money, seconds: int, tax_ratio: float):
          RegularPolicy.__init__(self, amount, seconds)
          TaxablePolicy.__init__(self, tax_ratio)
  
  if __name__ == "__main__":
      policy = TaxableRegularPolicy(Money(10), 10, 0.02)
      phone = Phone()
      phone.call(Call(datetime(2024, 11, 11, 22, 30, 0), datetime(2024, 11, 12)))
      phone.call(Call(datetime(2024, 12, 10, 22, 30, 0), datetime(2024, 12, 11)))
      print(policy.calculate_fee(phone)._amount)
  ```

  - 결국에는 믹스인할 때 마다 클래스가 늘어난다는 문제는 그대로인 것 아닌가?
    - 클래스 폭발의 문제는 클래스가 늘어난다는 것 자체 보다 클래스의 증가와 함께 중복 코드가 늘어난다는 것이다.
    - 믹스인에서는 이런 문제가 발생하지 않는다.
  - 결국 믹스인하는 클래스를 구현한 순간 정적으로 결정되는 것 아닌가?
    - 믹스인에서 동적으로 변경되는 것은 `super`가 가리키는 대상이다.
    - 상속에서의 `super`는 무조건 부모 클래스를 가리키지만, `mixin`에서의 `super`는 믹스인 대상 클래스를 가리킨다.
    - 예를 들어 아래와 같이 상속을 이용할 경우 `super().calculate_fee(phone)`는 몇 번을 호출하든 `RegularPolicy.calculate_fee()`를 호출한다.
    - 그러나 믹스인을 사용할 경우 `super()`는 믹스인 대상에 따라 `RegularPolicy`가 될 수도 있고, `NightlyDiscountPolicy`가 될 수도 있다.

  ```python
  # 상속을 사용할 경우
  class TaxableRegularPolicy(RegularPolicy):
  
      def __init__(self, discount_amount: Money):
          self._discount_amount = discount_amount
  
      def calculate_fee(self, phone: Phone):
          fee: Money = super().calculate_fee(phone)
          return fee.minus(self._discount_amount)
      
  
  # 믹스인 사용
  class TaxablePolicy(BasicRatePolicy):
      
      def __init__(self, tax_ratio: float):
          self._tax_ratio = tax_ratio
  
      def calculate_fee(self, phone: Phone):
          fee: Money = super().calculate_fee(phone)
          return fee.plus(fee.times(self._tax_ratio))
  ```



- 쌓을 수 있는 변경

  - 믹스인은 특정한 클래스의 메서드를 재사용하고 기능을 확장하기 위해 사용돼 왔다.
    - 핸드폰 과금 시스템의 경우에는 `BasicRatePolicy`의 `calculate_fee` 메서드의 기능을 확장하기 위해 사용했다.
    - 믹스인을 사용하면 특정 클래스에 대한 변경 또는 확장을 독립적으로 구현한 후 필요한 시점에 차례대로 추가할 수 있다.
    - 믹스인의 이러한 특징을 쌓을 수 있는 변경이라 부른다.

  - 믹스인은 상속 계층 안에서 확장한 클래스보다 더 하위에 위치하게 된다.
    - 다시 말해서 믹스인은 대상 클래스의 자식 클래스처럼 사용될 용도로 만들어진다.
    - 따라서 믹스인을 추상 서브클래스라고 부르기도 한다.

  - 믹스인의 주요 아이디어
    - 객체지향 언어에서 부모 클래스는 자식 클래스를 명시하지 않고도 정의할 수 있다.
    - 그러나 자식 클래스를 정의할 때는 부모 클래스를 명시해야 한다.
    - 믹스인은 부모 클래스로부터 상속될 클래스를 명시하는 메커니즘을 표현한다.
    - 하나의 믹스인은 매우 다양한 클래스를 도출하면서 서로 다른 서브클래스를 이용해 인스턴스화될 수 있다.
    - 믹스인의 이런 특성은 다중 클래스를 위한 단일의 점진적인 확장을 정의하는 데 적절하다.
    - 이 클래스들 중 하나를 부모 클래스로 삼아 믹스인이 인스턴스화될 때 행위가 확장된 클래스를 생성한다.





# 핵심

- 모양이 유사하다는 것은 단지 중복의 징후일 뿐이며, 중복 여부를 결정하는 기준은 코드가 변경에 반응하는 방식이다.



- 상속은 부모 클래스와 자식 클래스를 강하게 결합시킨다.



- 퍼블릭 인터페이스에 대한 고려 없이 단순히 코드 재사용을 위해 상속을 이용하는 것은 매우 위험하다.



- 자식 클래스가 부모 클래스의 구현이 아닌 추상화에 의존하도록 만드는 것이다.



- 상속으로 인한 클래스 사이의 결합을 피할 수 있는 방법은 없다.



- 합성은 포함되는 객체의 퍼블릭 인터페이스를 재사용한다.



- 컴파일타임 의존성과 런타임 의존성이 멀수록 설계가 유연해진다.
