# 타입 계층의 구현

- 타입 계층
  - **타입과 클래스는 동일한 개념이 아니다.**
    - **타입은 개념의 분류를 의미하고 클래스는 타입을 구현하는 한 가지 방법일 뿐이다.**
    - 타입은 다양한 방법으로 구현할 수 있다.
    - 객체의 클래스는 객체의 구현을 정의한다.
  - 타입 계층은 타입보다 더 복잡하다.
    - 다양한 방식으로 구현된 타입들을 하나의 타입 계층 안에 조합할 수 있기 때문이다.
    - 예를 들어 Java에서는 인터페이스와 클래스를 이용해 개별 타입을 구현한 후 이 두 가지 종류의 타입 구현체를 함께 포함하도록 타입 계층을 구성할 수 있다.
  - 아래 내용을 반드시 염두에 두어야한다.
    - **타입 계층은 동일한 메시지에 대한 행동 호환성을 전제**로 하기에 아래에서 언급할 모든 방법은 타입 계층을 구현하는 방법인 동시에 다형성을 구현하는 방법이기도 하다.
    - **서브타이핑 관계가 보장되지 않는다면 타입 계층을 올바르게 구현했다고 할 수 없다.**
    - **올바른 타입 계층이 되기 위해서는 서브타입이 슈퍼타입을 대체할 수 있도록 리스코프 치환 원칙을 준수해야 한다.**
    - 리스코프 치환 원칙은 특정한 구현 방법에 의해 보장될 수 없기 때문에, 행동 호환성을 보장하는 것은 전적으로 구현하는 사람의 책임이다.



- 클래스를 이용한 타입  계층 구현

  - 객체지향 언어에서 클래스를 사용자 정의 타입이라고 부른다.
    - **타입은 객체의 퍼블릭 인터페이스를 가리키기 때문**에 결과적으로 클래스는 객체의 타입과 구현을 동시에 정의하는 것과 같기 때문이다.

  - 아래는 [상속과 코드 재사용] 장에서 작성한 `Phone` 클래스이다.
    - `Phone`의 인스턴스는 `calculate_fee` 메시지를 수신할 수 있는 퍼블릭 메서드를 구현한다.
    - 이 메서드는 결과적으로 `Phone`의 퍼블릭 인터페이스를 구성한다.
    - 타입은 퍼블릭 인터페이스를 의미하기 때문에 `Phone` 클래스는 `Phone` 타입을 구현한다고 말할 수 있다.
    - `Phone`은 `calculate_fee` 메시지에 응답할 수 있는 타입을 선언하는 동시에 객체 구현을 정의하고 있는 것이다.

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
  ```

  - 다시 한 번 강조하지만, 타입과 클래스가 동일한 개념인 것은 아니다.
    - `Phone`의 경우처럼 타입을 구현할 수 있는 방법이 한 가지만 존재하는 경우에는 타입과 클래스를 동일하게 취급해도 무방하다.
    - 타입을 구현할 수 있는 다양한 방법이 존재하는 순간부터는 클래스와 타입은 갈라지기 시작한다.
  - `Phone`과 퍼블릭 인터페이스는 동일하지만 다른 방식으로 구현해야 하는 객체가 필요하다고 가정해보자.
    - 다시 말해 구현은 다르지만 `Phone`과 동일한 타입으로 분류되는 객체가 필요하다고 가정해보자.
    - 퍼블릭 인터페이스를 유지하면서 새로운 구현을 가진 객체를 추가할 수 있는 가장 간단한 방법은 상속을 사용하는 것이다.
    - 상속을 이용하면 자식 클래스가 부모 클래스의 구현뿐만 아니라 퍼블릭 인터페이스도 물려받을 수 있기 때문에 타입 계층을 쉽게 구현할 수 있다.
    - 하지만 **상속은 자식 클래스를 부모 클래스의 구현에 강하게 결합시키기 때문에 구체 클래스를 상속 받는 것은 피해야 한다.**
    - 가급적 추상 클래스를 상속 받거나 인터페이스를 구현하는 방법을 사용해야 한다.

  ```python
  class NightlyDiscountPhone(Phone):
      ...
  ```



- 인터페이스를 이용한 타입 계층 구현

  - **인터페이스를 이용해 타입을 정의하고 클래스를 이용해 객체를 구현하면 클래스 상속을 사용하지 않고도 타입 계층을 구현할 수 있다.**
  - 간단한 게임을 개발하고 있다고 가정해보자.
    - 수많은 객체들 중에서 실제로 플레이어의 게임 플레이에 영향을 미치는 객체들을 `GameObject`라는 동일한 타입으로 분류할 것이다.
    - 게임 안에는 `GameObject`로 분류될 수 있는 다양한 객체들이 존재한다.
    - 예를 들어 폭발 효과를 표현하는 `Explosion`과 사운드 효과를 표현하는 `Sound`가 `GameObject`의 타입의 대표적인 예이다.
    - 이 중에서 `Explosion`과 `Sound`는 게임에 필요한 다양한 효과 중 하나이기 때문에 이들을 다시 `Effect` 타입으로 분류할 수 있다.
    - 이 중에서 `Explosion`은 화면에 표시될 수 있기 때문에 `Displayable` 타입으로도 분류할 수 있다.
    - `Displayable` 타입에는 `Player`와 `Monster` 등의 타입도 있다.
  - 이 때 상속을 이용해 이 객체들을 구현하는 방법을 생각해보자.
    - `Explosion` 타입은 `Effect` 타입인 동시에 `Displayable` 타입이기 때문에 두 클래스를 동시에 상속 받아야 한다.
    - 문제는 대부분의 언어들이 다중상속을 지원하지 않는다는 것이다.
    - 게다가 이 클래스들을 동일한 상속 계층 안에 구현하고 싶지도 않다.
    - 클래스들을 상속 관계로 연결하면 자식 클래스가 부모 클래스의 구현에 강하게 결합될 확률이 높다.
    - 결과적으로 상속 계층 안의 클래스 하나를 변경했는데도 게임에 포함된 수 많은 자식 클래스들이 영향을 받을 수 있다.
  - 다중 상속이라는 구현 제약도 해결하고 상속으로 인한 결합도 문제도 해결할 수 있는 방법은 클래스가 아닌 인터페이스를 사용하는 것이다.

  ```java
  public interface GameObject {
      String getName();
  }
  ```

  - `GameObject` 타입은 좀 더 많은 행동을 가진 다른 타입에 의해 확장될 수 있다.
    - 예를 들어 게임의 많은 요소들은 화면에 표시되어야 한다.
    - 이 객체들은 화면 표시라는 동일한 행동을 제공하기 때문에 `Displayable`라는 별도의 타입으로 분류되어야 한다.

  ```java
  public interface Displayable extends GameObject {
      Point getPosition();
      void update(Graphics graphics);
  }
  ```

  - `Displayable` 인터페이스가 `GameObject`를 확장한다는 사실에 주목해야 한다.
    - 위 코드는 `Displayable` 타입을 `GameObject`의 서브타입으로 정의한다.
    - 결과적으로 `Displayable` 타입의 모든 인스턴스는 `GameObject` 타입의 인스턴스 집합에도 포함된다.
    - 이처럼 **인터페이스가 다른 인터페이스를 확장하도록 만들면 슈퍼 타입과 서브 타입간의 타입 계층을 구성할 수 있다.**
  - 화면에 표시될 수 있는 `Displayable` 타입의 인스턴스들 중 다른 요소들과 충돌할 수 있는 객체들을 구현한다.
    - 충돌을 체크하기 위한 `collideWith` 오퍼레이션을 추가한다.

  ```java
  public interface Collidable extends Displayable {
      boolean collideWiht(Collidable other);
  }
  ```

  - `Effect` 타입을 정의한다.
    - 배경 음악과 효과음 등은 특정한 조건에 따라 활성화 되어야 하므로 `activate` 오퍼레이션을 추가한다.

  ```java
  public interface Effect extends GameObject {
      void activate();
  }
  ```

  - 이제 타입에 속할 객체들을 구현한다.
    - 인터페이스로 정의한 타입을 구현하기 위해 클래스를 사용할 것이다.
    - 인터페이스와 클래스를 함께 조합하면 다중 상속의 딜레마에 빠지지 않을 수 있고 단일 상속 계층으로 인한 결합도 문제를 피할 수 있다.

  ```java
  public class Player implemnets Colliable {
      @Override
      public String getName(){
          // ...
      }
      
      @Override
      public boolean collideWith(Collidable other){
          // ...
      }
      
      @Override
      public Point getPosition(){
          // ...
      }
      
      @Override
      public void update(Graphics graphic){
          // ...
      }
  }
  
  public class Monster implemnets Colliable {
      // Player와 퍼블릭 인터페이스는 동일하다.
  }
  
  public class Sound implements Effect {
      @Override
      public STring getName() {
          // ...
      }
      
      @Override
      public void activate() {
          // ...
      }
  }
  
  public class Explosion implements Displayable, Effec {
      @Override
      public String getName(){
          // ...
      }
      
      @Override
      public Point getPosition(){
          // ...
      }
      
      @Override
      public void update(Graphics graphic){
          // ...
      }
      
      @Override
      public void activate() {
          // ...
      }
  }
  ```

  - 이로부터 아래와 같은 사실을 알 수 있다.
    - 첫째로 여러 클래스가 동일한 타입을 구현할 수 있다는 것이다.
    - 따라서 **다른 클래스의 객체들이 동일한 타입을 가질 수 있다.**
    - `Player`와 `Monster` 클래스는 서로 다른 클래스지만 이 두 클래스의 인스턴스들은 `Collidable` 인터페이스를 구현하고 있기 때문에 동일한 메시지에 응답할 수 있다.
    - 따라서 서로 다른 클래스를 이용해서 구현됐지만 타입은 동일하다.
    - 두 번째로 하나의 클래스가 여러 타입을 구현할 수도 있다.
    - 따라서 **하나의 객체가 여러 타입을 가질 수 있다.**
    - `Explosion` 인스턴스는 `Displayable` 인터페이스와 동시에 `Effect` 인터페이스도 구현한다. 따라서 `Explosion`의 인스턴스는 `Displayable` 타입인 동시에 `Effect` 타입이기도 하다.



- 클래스와 타입을 구분하는 것은 매우 중요하다.
  - 객체의 클래스는 객체의 구현을 정의하고, 타입은 인터페이스를 정의한다.
    - 클래스는 객체의 내부 상태와 오퍼레이션 구현 방법을 정의하는 것이다.
    - **객체의 타입은 인터페이스만을 정의하는 것으로 객체가 반응할 수 있는 오퍼레이션의 집합을 의미한다.**
  - 클래스와 타입 간에는 밀접한 관련이 있다.
    -  클래스도 객체가 만족할 수 있는 오퍼레이션을 정의하고 있으므로 타입을 정의하는 것이기도 하다.
  - 둘을 구분하는 것은 설계 관점에서도 매우 중요하다.
    - 타입은 동일한 퍼블릭 인터페이스를 가진 객체들의 범주다.
    - 클래스는 타입에 속하는 객체들을 구현하기 위한 구현 메커니즘이다.
    - 객체지향에서 중요한 것은 협력 안에서 객체가 제공하는 행동이라는 사실을 생각해 본다면, 중요한 것은 클래스 자체가 아니라 타입이라는 것을 알 수 있다.
    - 타입이 식별된 후에 타입에 속하는 객체를 구현하기 위해 클래스를 사용하는 것이다.
  - **클래스가 아니라 타입에 집중해야 한다.**
    - **중요한 것은 객체가 외부에 제공하는 행동, 즉 타입을 중심으로 객체들의 계층을 설계하는 것이다.**
    - **타입이 아니라 클래스를 강조하면 객체의 퍼블릭 인터페이스가 아닌 세부 구현에 결합된 협력 관계를 낳게 된다.**



- 추상 클래스를 이용한 타입 계층 구현

  - 클래스 상속을 이용해 구현을 공유하면서도 결합도로 인한 부작용을 피하는 방법이다.
  - 영화 예매 정책에서는 할인 정책을 구현하기 위한 `DiscountPolicy`가 추상 클래스에 해당한다.

  ```python
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
  ```

  - 추상 클래스인 `DiscountPolicy`를 상속 받는 구체 클래스를 추가함으로써 타입 계층을 구현할 수 있다.

  ```python
  class AmountDiscountPolicy(DiscountPolicy):
  
      def __init__(self, discount_amount: Money, conditions: list[DiscountCondition]):
          super().__init__(conditions)
          self.discount_amount = discount_amount
  
      def get_discount_amount(self, screening: Screening) -> Money:
          return self.discount_amount
  ```

  - 구체 클래스로 타입을 정의해서 상속받는 방법과 추상 클래스로 타입을 정의해서 상속받는 방법 사이에는 두 가지 중요한 차이점이 있다.
    - 첫 번째로 **의존하는 대상의 추상화 정도가 다르다.**
    - 앞서 살펴본 `Phone`의 예시에서 자식 클래스인 `NightlyDiscountPhone`의 `calculate_fee` 메서드가 부모 클래스인 `Phone`의 `calcaulate_fee` 메서드의 구체적인 내부 구현에 강하게 결합된다.
    - 따라서 부모 클래스의 내부 구현이 변경될 경우 자식 클래스도 함께 변경될 가능성이 높다.
    - 이에 비해 추상클래스인 `DiscountPolicy`의 경우 자식 클래스인 `AmountDiscountPolicy`가 부모 클래스의 내부 구현이 아닌 추상 메서드의 시그니처에만 의존한다.
    - 이 경우 자식 클래스들은 부모 클래스가 어떤 식으로 구현되어 있는지 알 필요가 없으며, 단지 추상 메서드로 정의된 `get_discount_amount` 메서드를 오버라이딩하면 된다는 사실에만 의존해도 무방하다.
    - 두 번째로 **상속을 사용하는 의도가 다르다.**
    - `Phone`은 상속을 염두에 두고 설계된 것이 아니므로 미래의 확장을 위한 어떤 준비도 되어 있지 않다.
    - 그에 반해 `DiscountPolicy`는 처음부터 상속을 염두에 두고 설계된 클래스로, 추상클래스이기에 자신의 인스턴스를 직접 생성할 수 없다.
    - `DiscountPolicy`의 유일한 목적은 자식 클래스를 추가하는 것이며, 추상 메서드를 제공함으로써 상속 계층을 쉽게 확장할 수 있게 하고 결합도로 인한 부작용을 박징할 수 있는 안전망을 제공한다.



- 추상 클래스와 인터페이스 결합하기

  - 클래스만을 이용한 방법에는 한계가 있다.
    - 대부분의 객체지향 언어들은 단일 상속만 지원한다.
    - 이 경우 여러 타입으로 분류되는 타입이 문제가 될 수 있는데 오직 클래스만을 이용해 타입을 구현할 경우 다중 상속이 꼭 필요하기 때문이다.
    - 클래스와 단일 상속만으로는 이 문제를 해결할 수 없기 때문에 대부분의 경우에 해결 방법은 타입 계층을 오묘한 방식으로 비트는 것이다.
    - Java의 경우 인터페이스를 이용하면 다중 상속 문제를 해결할 수 있는데, 클래스가 구현할 수 있는 인터페이스의 수에는 제한이 없기 때문이다.
  - 인터페이스만을 이용한 방법에도 단점은 있다.
    - Java 8 이전에서 제공하는 인터페이스에는 구현 코드를 포함시킬 수 없기 때문에 인터페이스만으로는 중복 코드를 제거하기 어렵다는 접이다.
    - 따라서 **효과적인 접근 방법은 인터페이스를 이용해 타입을 정의하고 특정 상속 계층에 국한된 코드를 공유할 필요가 있을 경우 추상 클래스를 이용해 코드 중복을 방지하는 것이다.**
    - 이런 형태로 추상 클래스를 사용하는 방식을 **골격 구현 추상 클래스(skeletal implementation abstract class)**라고 부른다.
  - **인터페이스와 추상 클래스 결합**
    - `DiscountPolicy` 타입은 추상 클래스를 이용해서 구현했기 때문에 `DiscountPolicy` 타입에 속하는 모든 객체들은 하나의 상속 계층 안에 묶여야 하는 제약을 가진다.
    - 이제 상속 계층에 대한 제약을 완화시켜 `DiscountPolicy`타입으로 분류될 수 있는 객체들이 구현 시에 서로 다른 상속 계층에 속하도록 만들어 볼 것이다.
    - 이를 위한 가장 좋은 방법은 인터페이스와 추상 클래스를 결합하는 것이다.
    - `DiscountPolicy` 타입을 추상 클래스에서 인터페이스로 변경하고 공통 코드를 담을 골격 구현 추상 클래스인 `DefaultDiscountPolicy`를 추가함으로써 상속 계층이라는 굴레를 벗어날 수 있다.

  ```python
  class DiscountPolicy(ABC):
  	
      @abstractmethod
      def calculate_discount_amount(self, screening: Screening):
          ...
          
  class DefaultDiscountPolicy(DiscountPolicy):
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
  ```

  - 그 후 `AmountDiscountPolicy`의 부모 클래스를 `DefaultDiscountPolicy`로 변경한다.

  ```python
  class AmountDiscountPolicy(DefaultDiscountPolicy):
  
      def __init__(self, discount_amount: Money, conditions: list[DiscountCondition]):
          super().__init__(conditions)
          self.discount_amount = discount_amount
  
      def get_discount_amount(self, screening: Screening) -> Money:
          return self.discount_amount
  ```

  - 인터페이스와 추상 클래스를 함께 사용하는 방식은 추상 클래스만 사용하는 방법에 비해 두 가지 장점이 있다.
    - 다양한 구현이 필요할 경우 새로운 추상 클래스를 추가해서 쉽게 해결할 수 있다.
    - 이미 부모 클래스가 존재하는 클래스라고 하더라도 인터페이스를 추가함으로써 새로운 타입으로 쉽게 확장할 수 있다.
    - 만약 `DiscountPolicy` 타입이 인터페이스가 아닌 추상 클래스로 구현되어 있는 경우 이 문제를  해결할 수 있는 유일한 방법은 상속 계층을 다시 조정하는 것뿐이다.
  - 요약하면 아래와 같다.
    - **상속 계층에 얽매이지 않는 타입 계층을 요구한다면 인터페이스로 타입을 정의한 후 추상 클래스로 기본 구현을 제공해서 중복 코드를 제거하면 된다.**
    - 만약 이런 복잡성이 필요하지 않다면 타입을 정의하기 위해 인터페이스나 추상 클래스 둘 중 하나만 사용해야 한다.
    - **타입의 구현 방법이 단 한 가지거나 상속 계층만으로도 타입 계층을 구현하는 데 무리가 없다면 클래스나 추상 클래스를 이용해 타입을 정의하는 것이 더 좋다.**
    - **그 외의 상황이라면 인터페이스를 사용하는 것을 고려해야 한다.**



- 덕 타이핑 사용하기

  - 덕 타이핑은 주로 동적 언어에서 사용하는 방법으로 아래와 같은 덕 테스트(duck test)를 프로그래밍 언어에 적용한 것이다.

  > 어떤 새가 오리처럼 걷고, 오리처럼 헤엄치며, 오리처럼 꽥꽥 소리를 낸다면 나는 이 새를 오리라고 부를 것이다 - 제임스 윗콤 릴리

  - **덕 타이핑은 객체가 어떤 인터페이스에 정의된 행동을 수행할 수만 있다면 그 객체를 해당 타입으로 분류해도 된다는 것이다.**
    - **덕 타이핑은 특정 클래스에 종속되지 않은 퍼블릭 인터페이스다.**
    - 여러 클래스를 가로지르는 이런 인터페이스는 클래스에 대한 의존을 메시지에 대한 의존으로 대치시켜 애플리케이션을 굉장히 유연하게 만들어준다.
    - **덕 타이핑을 사용하면 메시지 수준으로 결합도를 낮출 수 있기 때문에 유연할 설계를 얻을 수 있다.**
    - 다만, **덕 타이핑을 사용하면 컴파일 시점에 발견할 수 있는 오류를 실행 시점으로 미루게 되기 때문에 코드의 안전성을 약화시킬 수 있다.**
  - 컨텍스트 독립성과 덕 타이핑
    - [의존성 관리하기] 장에서 유연한 설계의 한 가지 조건으로 컨텍스트 독립성을 살펴봤다.
    - 인터페이스가 클래스보다 더 유연한 설계를 가능하게 해주는 이유는 클래스가 정의하는 구현이라는 컨텍스트에 독립적인 코드를 작성할 수 있게 해주기 때문이다.
    - 덕 타이핑은 여기서 한 걸음 더 나아간다.
    - 단지 메서드의 시그니처만 동일하면 명시적인 타입 선언이라는 컨텍스트를 제거할 수 있다.
    - 덕 타이핑은 클래스나 인터페이스에 대한 의존성을 메시지에 대한 의존성으로 대체한다.
    - 결과적으로 낮은 결합도를 유지하고 변경에 유연하게 대응할 수 있다.





# 동적인 협력, 정적인 코드

- 객체는 동적이고, 프로그램은 정적이다.
  - 협력을 구성하기 위해서는 살아 움직이는 객체가 필요하다.
    - 객체는 동적이다.
    - 객체의 움직임과 변화를 표현하기 위해 객체지향 프로그래밍 언어를 사용한다.
  - 문제는 프로그래밍을 위해 사용하는 텍스트라는 표현 도구가 정적이라는 것이다.
    - 프로그램은 일단 작성되고 나면 프로그래머가 직접 손을 대기 전까지는 변하지 않는다.
  - 객체는 동적이고 프로그램은 정적이라는 사실은 프로그래머가 아래 두 가지 모델을 동시에 마음속에 그려야 한다는 것을 의미한다.
    - 동적 모델(dynamic model): 프로그램의 실행 구조를 표현하는 움직이는 모델.
    - 정적 모델(static model): 코드의 구조를 담는 고정된 모델.
  - 훌륭한 객체지향 프로그램을 작성하기 위해서는 두 모델을 조화롭게 버무릴 수 있는 능력이 필요하다.
    - 객체지향 세계에서 동적 모델은 객체와 협력으로 구성된다.
    - 객체지향 세계에서 정적 모델은 관계와 타입으로 구성된다.
    - 객체는 다른 객체와 협력하면서 애플리케이션의 기능을 수행한다.
    - 타입은 객체를 분류하기 위한 틀로서 동일한 타입에 속하는 객체들이 수행할 수 잇는 모든 행동들을 압축해서 표현한 것이다.
    - 클래스 기반의 객체지향 언어에서 타입을 구현하는 가장 대표적인 방법은 클래를 사용하는 것이므로 일반적으로 정적 모델이라고 하면 클래스로 구성된 모델을 의미한다.
  - **동적 모델이 정적 모델에 앞선다.**
    - 정적 모델은 동적 모델에 의해 주도돼야 하고 동적 모델이라는 토대 위에 세워져야 한다.
    - 프로그램 코드 안에 담아지는 정적 모델은 객체 사이의 협력에 기반해야 한다.
    - 동적 모델을 기반으로 정적 모델을 구상할 때 고려해야 하는 가장 중요한 요소는 변경이다.
    - 설계가 필요한 이유는 변경을 수용할 수 있는 코드를 만들기 위해서다.
  - 변경을 수용할 수 있는 코드란 단순하고 결합도가 낮으며, 중복 코드가 없는 코드를 의미한다.
    - 수정이 용이한 코드란 응집도가 높고, 결합도가 낮으며, 단순해서 쉽게 이해할 수 있는 코드다.
    - 유연한 코드란 동일한 코드를 이용해 다양한 컨텍스트에서 동작 가능한 협력을 만들 수 있는 코드다.
    - 수정이 용이한 코드와 유연한 코드를 작성하기 위해 중복 코드를 제거해야 한다.





## 동적 모델과 정적 모델

- **행동이 코드를 결정한다.**
  - 협력에 참여하는 객체의 행동이 객체의 정적 모델을 결정해야 한다.
  - 행동이 코드의 구조에 영향을 미치는 대표적인 예가 바로 상속 계층을 구성하는 방식이다.
    - [서브클래싱과 서브타이핑] 장에서 서브타이핑을 살펴볼 때 사용했던 `Bird`와 `Penguin`의 예시를 다시 살펴보자.
    - 만약 객체가 외부에 제공하는 행동을 제외한 채 개념 사이의 관계에 기반해 `Bird`와  `Penguin`의 정적 모델을 구상한다면 `Penguin`은 `Bird`의 자식 클래스가 될 것이다.
    - 하지만 객체가 외부에 `fly`라는 행동을 제공한다면 정적 모델의 구조는 `FlyingBird`를 추가하고, `FlyingBird`와 `Penguin`이 `Bird`를 상속받는 구성이 될 것이다.
  - 객체의 정적 모델은 동적 모델이라는 토대 없이는 완전해질 수 없다.
    - 위 예시는 객체가 외부에 제공하는 행동이 코드 구조에 어떤 영향을 미치는지를 잘 설명해준다.
    - 객체의 행동을 고려하지 않을 경우 날 수 있는 `Penguin`이 나타나거나 `Bird`의 인스턴스들이 예상과 다르게 행동하거나 OCP를 위반하는 코드가 양산될 수 밖에 없다.
    - 가장 중요한 것은 객체가 외부에 제공하는 행동이다.
    - **정적 모델을 설계하는 이유는 단지 행동과 변경을 적절하게 수용할 수 있는 코드 구조를 찾는 것이어야 한다.**
  - **정적 모델을 미리 결정하고 객체의 행동을 정적 모델에 맞춰서는 안 된다.**
    - 동적 모델이 정적 모델을 결정해야 한다.
    - 만약 정적 모델이 협력에 적합하지 않다면 정적 모델을 지속적으로 개선하라.
    - 그 결과로 `FlyingBird`와 같은 이상한 이름의 클래스를 추가해야 한다고 해도 말이다.



- 변경을 고려하라
  - 객체가 제공하는 행동의 측면에서 적절하게 정적 모델을 고려하더라도 변경을 고려하지 않으면 유지보수하기 어려운 코드가 만들어진다.
  - 동일한 행동을 제공하는 정적 모델이 있다면 항상 현재의 설계에서 요구되는 변경을 부드럽게 수용할 수 있는 설계를 선택해야한다.





## 도메인 모델과 구현

- 도메인 모델
  - 도메인 모델의 정의
    - 도메인이란 사용자가 프로그램을 사용하는 대상 영역을 가리킨다.
    - 모델이란 지식을 선택적으로 단순화하고 의식적으로 구조화한 형태다.
    - **도메인 모델이란 사용자가 프로그램을 사용하는 대상 영역에 대한 지식을 선택적으로 단순화하고 의식적으로 구조화한 형태다.**
  - 소프트웨어의 도메인에 대해 고민하고 도메인 모델을 기반으로 소프트웨어를 구축해야한다.
    - 이를 통해 개념과 소프트웨어 사이의 표현적 차이를 줄일 수 있기 때문에 이해하고 수정하기 쉬운 소프트웨어를 만들 수 있다.
  - 여기서 중요한 것은 **도메인 모델을 작성하는 것이 목표가 아니라 출발점**이라는 것이다.
    - 소프트웨어를 만들기 위해 수행하는 모든 활동의 궁극적인 목적은 동작하는 소프트웨어를 만드는 것이다.
    - 도메인 모델은 소프트웨어를 만드는 데 필요한 개념의 이름과 의미, 그리고 관계에 대한 힌트를 제공하는 것으로 끝나야 한다.
    - 도메인 모델에 지나치게 집착하거나 도메인 모델의 초기 구조를 맹목적으로 따를 경우 변경하기 어려운 소프트웨어가 만들어질 가능성이 높아진다.
  - **불행은 도메인 안의 개념이 제공하는 틀에 맞춰서 소프트웨어를 구축해야 한다고 생각할 때부터 시작된다.**
    - 또한 도메인 모델이 클래스 다이어그램과 같은 정적 모델에 기반해야 한다는 오해 역시 잘못된 코드 구조를 낳는 원인이 된다.
    - 도메인 모델은 도메인에 대한 지식을 표현하고 코드의 구조에 대한 힌트를 제공할 수 있다면 어떤 형태로 표현하더라도 상관이 없다.



- 몬스터 설계하기

  - 주인공 캐릭터를 공격하는 다양한 종류의 몬스터가 등장하는 게임을 설계해야 한다고 가정해보자.
    - 현재의 요구사항에 따르면 몬스터는 용과 트롤만이 존재하지만 앞으로 어떤 종류의 몬스터가 더 추가될지 모른다.
    - 즉 몬스터의 종류를 확장할 수 있어야 한다는 것이다.
    - 설계자들은 용과 트롤이 몬스터의 일종이기 때문에 아래와 같은 도메인 모델에서 출발하는 것이 적절하다고 생각했다.
    - 아래 도메인 모델은 코드를 작성할 수 있는 훌륭한 출발점을 제공한다.
    - 게다가 모든 몬스터가 공격할 수 있다는 요구사항을 수용할 수 있으며 계층에 속하는 모든 클래스들이 서브타입 관계를 만족하도록 구현할 수도 있다.
    - 결론적으로 아래 도메인 모델을 기반으로 코드를 작성하면 원하는 협력을 지원할 수 있기 때문에 훌륭한 출발점이 될 수 있다.

  ```|=|
  Monster
   ㄴ Dragon
   ㄴ Troll
   ㄴ ?
  ```

  - `Monster`와 그 자식 클래스 구현하기

  ```python
  from abc import ABC
  
  class Monster(ABC):
      def __init__(self, health: int):
          self._health = health
      
      def get_attack(self):
          ...
          
  class Dragon(Monster):
      def get_attack(self):
          return "불 뿜기"
      
  class Troll(Monster):
      def get_attack(self):
          return "곤봉 휘두르기"
  ```

  - 합성 사용하기

    - 추후에 새로운 몬스터를 추가해달라는 요청이 물밀듯이 들어오고, 그 때 마다 몬스터별로 하나의 클래스를 추가하고 `get_attack` 메서드를 오버라이딩한다.
    - 게임에 몬스터를 더 쉽게 추가할 수 있는 방법이 필요해졌다.
    - 현재의 설계를 변경하기 어려운 이유는 몬스터가 필요할 때마다 새로운 클래스를 추가해야 하기 때문이다.
    - 물론 현재의 설계는 기존 코드의 수정 없이 몬스터를 추가할 수 있기 때문에 OCP를 준수하지만, 더 좋은 방법은 새로운 클래스를 추가히지 않고도 새로운 몬스터를 추가할 수 있는 방법일 것이다.

    - 몬스터 종류별로 새로운 서브클래스를 추가하는 대신 몬스터가 품종을 가지도도록 설계를 개선한다.
    - 즉 하나의 `Monster` 클래스가 하나의 `Breed` 클래스를 합성 관계로 포함하는 설계로 개선할 수 있다.

  ```python
  class Breed:
      def __init__(self, name: str, health: int, attack: str):
          self._name = name
          self._health = health
          self._attack = attack
          
      @property
      def attack(self):
          return self._attack
          
  
  class Monster:
      def __init__(self, breed: Breed):
          self._bread = bread
          
      def get_attack(self):
          return breed.attack
  ```

  - 두 개의 클래스만으로 반복작업을 단순화시켰다.
    - 이제 몬스터의 종류를 추가하는 것은 새로운 클래스를 추가하는 것이 아니라 새로운 `Breed` 인스턴스를 생성하고 `Monster` 인스턴스에 연결하는 작업으로 바뀐다.

  ```python
  dragon = Monster(Breed("용", 1000, "불 뿜기"))
  ```

  - 도메인 모델도 이에 따라 단순해진다.

  ```
  Monster ◆─ Breed
  ```

  - TYPE OBJECT 패턴
    - 위와 같이 어떤 인스턴스가 다른 인스턴스의 타입을 표현하는 방법을 TYPE OBJECT 패턴이라고 부른다.
    - 앞에서 살펴본 게임 예제에서 `Breed`의 인스턴스가 바로 `Monster`의 타입을 구현하는 TYPE OBJECT에 해당한다.



- 행동과 변경을 고려한 도메인 모델
  - 일반적으로 도메인 모델은 아레와 같은 순서로 사용한다.
    - 도메인 모델 만든다. 
    - 만들어진 도메인 모델에 표현된 개념과 관계를 기반으로 협력에 필요한 객체의 후보를 도출한다.
    - 구현 클래스의 이름과 관계를 설계한다.
  - 도메인 모델을 그대로 복사해서는 안 된다.
    - 초기의 도메인 모델은 그저 작업을 시작하기 위한 거친 아이디어 덩어리일 뿐이다.
    - 더 많은 지식이 쌓이고 요구사항이 분명해지면 초기의 아이디어에 대한 미련을 버려야 한다.
    - 몬스터 설계할 때 처음 작성했던 도메인 모델을 도메은 실제 코드와는 멀어졌다.
    - 하지만 새로운 도메인 모델은 실제로 다양한 종류의 몬스터의 구조를 구현하기 위해 사용된 코드의 구조와 일치한다.
  - 핵심은 도메인 모델은 단순히 정적 모델의 형태를 띨 필요가 없으며 도메인 모델의 구조가 코드와 다를 필요가 없다는 것이다.
    - 도메인 모델은 코드를 위한 것이다.
    - 도메인 모델은 도메인 안에 존재하는 개념과 관계를 표현해야 하지만 최종 모습은 객체의 행동과 변경에 기반해야 하며 코드의 구조를 반영해야 한다.
    - 중요한 것은 도메인 모델을 봤을 때 도메인의 개념뿐만 아리나 코드도 함께 이해될 수 있는 구조를 찾는 것이다.
    - 즉 도메인 모델과 코드의 구조 사이의 차이는 작을수록 좋다.
    - 앞서 말했듯 형식은 어떤 형태라도 좋다.





# 핵심

- 타입과 클래스는 동일한 개념이 아니다. 타입은 개념의 분류를 의미하고 클래스는 타입을 구현하는 한 가지 방법일 뿐이다.



- 서브타이핑 관계가 보장되지 않는다면 타입 계층을 올바르게 구현했다고 할 수 없다.



- 객체의 타입은 인터페이스만을 정의하는 것으로 객체가 반응할 수 있는 오퍼레이션의 집합을 의미한다.



- 타입의 구현 방법이 단 한 가지거나 상속 계층만으로도 타입 계층을 구현하는 데 무리가 없다면 클래스나 추상 클래스를 이용해 타입을 정의하는 것이 더 좋다.



- 덕 타이핑을 사용하면 메시지 수준으로 결합도를 낮출 수 있기 때문에 유연할 설계를 얻을 수 있다.



- 정적 모델을 미리 결정하고 객체의 행동을 정적 모델에 맞춰서는 안 된다.
