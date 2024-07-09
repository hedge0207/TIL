# 계약에 의한 설계

- 계약에 의한 설계가 필요한 이유
  - 인터페이스만으로는 객체의 행동에 관한 다양한 관점을 전달하기 어렵다
    - [메시지와 인터페이스]에서 살펴본 원칙에 따라 의도를 드러내도록 인터페이스를 다듬고 명령과 쿼리를 분리했다고 해도 명령으로 인해 발생하는 부수효과를 명확하게 표현하는 데는 한계가 있다.
    - 메서드의 내부 구현이 단순하다면 내부를 살펴보는 것만으로도 부수효과를 쉽게 이해할 수 있을 것이다.
    - 하지만 구현이 복잡하고 부수효과를 가진 다수의 메서드들을 연이어 호출하는 코드를 분석하는 경우에는 실행 결과를 예츧하기 어려울 수밖에 없다.
    - 물론 주석으로 해결할 수 있겠지만, 주석으로 설명하는 것은 한계가 있을 뿐더러, 주석이 시간이 지남에 따라 코드를 반영하지 못 하게 되는 경우도 많아지기 때문에 이는 좋은 방법이 아니다.
  - **계약에 의한 설계를 사용하면 다양한 제약과 부수효과를 정의하고 문서화할 수 있다.**
    - 클라이언트 개발자는 오퍼레이션의 구현을 살펴보지 않더라도 객체의 사용법을 쉽게 이해할 수 있다.
    - 계약은 실행 가능하기 때문에 구현에 동기화돼 있는지 여부를 런타임에 검증할 수 있다.
    - 따라서 주석과 다르게 시간의 흐름에 뒤쳐질 걱정을 할 필요가 없다.
    - 계약에 의한 설계는 클래스의 부수효과를 명시적으로 문서화하고 명시적으로 커뮤니케이션할 수 있을뿐만 아니라 실행 가능한 검증 도구로써 사용할 수 있다.



- C#에는 계약에 의한 설계 라이브러리인 Code Contracts가 있다.
  - 아래 예시에서는 이 라이브러리를 사용할 것이다.





## 협력과 계약

- 부수효과를 명시적으로

  - 객체지향의 핵심은 협력 안에서 객체들이 수행하는 행동이다.
    - **프로그래밍 언어로 작성된 인터페이스는 객체가 수신할 수 있는 메시지는 정의할 수 있지만 객체 사이의 의사소통 방식은 명확하게 정의할 수 없다.**
    - 메시지의 이름과 파라미터 목록은 시그니처를 통해 전달할 수 있지만 **협력을 위해 필요한 약속과 제약은 인터페이스를 통해 전달할 수 없기 떄문에 협력과 관련된 상당한 내용이 암시적인 상태로 남게 된다.**
  - [메시지와 인터페이스] 장에서 명령-쿼리 분리 원칙을 살펴보기 위해 소개했던 일정 관리 프로그램의 C# 버전을 이용해 계약에 의한 설계를 살펴볼 것이다.
    - 명령과 쿼리를 분리했기에 `Event` 클래스의 클라이언트는 먼저 `IsSatisfied` 메서드를 호출해서 `RecurringSchedule`의 조건을 만족시키는지 여부를 확인한 후에 `Reschedule` 메서드를 호출해야 한다.
    - 인터페이스만으로는 메서드의 순서와 관련된 제약을 설명하기 쉽지 않다.
    - 그러나 계약에 의한 설계 라이브러리인 Code Contracts를 사용하면 `IsSatisfied` 메서드의 실행 결과가 true일 때만 `Reschedule` 메서드를 호출할 수 있다는 사실을 명확하게 표현할 수 있다.

  ```c#
  class Event
  {
      public bool IsSatisfied(RecurringSchedule schedule) {...}
      
      public void Reschedule(RecurringSchedule schedule)
      {
          Contract.Requires(IsSatisfied(schedule));
      }
  }
  ```

  - 계약을 통한 설계의 장점
    - 위 코드가 if문을 사용한 일반적인 파라미터 체크 방식과 크게 다르지 않다고 생각할 수도 있지만 그렇지 않다.
    - 대표적인 차이점으로 문서화를 들 수 있다.
    - 일반적인 정합성 체크 로직은 코드의 구현이 내부에 숨겨져있어 실제로 코드를 분석하지 않는 한 정확하게 파악하기가 쉽지 않다.
    - 게다가 일반 로직과 조건을 기술한 로직을 구분하기도 쉽지 않다.
    - 하지만 계약에 의한 설계를 지원하는 라이브러리나 언어들은 일반 로직과 구분할 수 있도록 계약 조건을 명시적으로 표현하는 것이 가능하다.
    - 위 코드에서 `Contract.Requires`는 메서드를 호출하기 전에 true여야 하는 조건을 표현하기 위해 Code Contracts에서 제공하는 API로 `IsSatified` 메서드의 반환값이 ture일 경우에만 `Reschedule` 메서드를 호출할 수 있다는 사실을 명확하게 표현한다.
    - 이렇게 작성된 계약은 문서화로 끝나는 것이 아니라 제약 조건의 만족 여부를 실행 중에 체크할 수 있다.
    - 또한 이 계약들을 코드로부터 추출해서 문서를 만들어주는 자동화 도구도 제공한다.
    - 따라서 계약에 의한 설계를 사용하면 계약 조건을 명시적으로 표현하고 자동으로 문서화할 수 있을뿐만 아니라 실행을 통해 검증할 수 있다.



- 계약
  - 계약은 한쪽의 의무가 반대쪽의 권리가 된다.
    - 예를 들어 리모델링 계약을 채결하는 상황을 가정해보자.
    - 리모델링을 위탁하는 입장에서는 인테리어 업자에게 대금을 지급할 의무가 있고, 원하는 품질로 집을 리모델링 받을 권리가 있다.
    - 반대로 인테리어 입자 입장에서는 고객이 원하는 품질로 집을 리모델링할 의무가 있고, 대금을 받을 권리가 있다.
  - 두 계약 당사자 중 어느 한쪽이라도 계약의 내용을 위반한다면 계약은 정상적으로 완료되지 않는다.
  - 계약은 협력을 명확하게 정의하고 커뮤니케이션할 수 있는 범용적인 아이디어다.
    - 그리고 사람들이 협력을 위해 사용하는 계약이라는 아이디어를 객체들이 협력하는 방식에도 적용하는 것이 계약에 의한 설계이다.





## 계약에 의한 설계

- 버트란드 마이어는 프로그래밍 언어인 Eiffel을 만들면서 사람들 사이의 계약에 착안해 계약에 의한 설계 기법을 고안했다.

  - 버트란드 마이어가 제시한 계약의 개념은 사람들 사이의 계약과 유사하다.
  - 계약은 협력에 참여하는 두 객체 사이의 의무와 이익을 문서화한 것이다.
    - 협력에 참여하는 각 객체는 계약으로부터 이익을 기대하고 이익을 얻기 위해 의무를 수행한다.
    - 협력에 참여하는 각 객체의 이익과 의무는 객체의 인터페이스상에 문서화된다.
  - **계약에 의한 설계 개념은 인터페이스에 대해 프로그래밍하라는 원칙을 확장한 것이다.**
    - 계약에 의한 설계를 이용하면 오퍼레이션의 시그니처를 구성하는 다양한 요소들을 이용해 협력에 참여하는 객체들이 지켜야 하는 제약 조건을 명시할 수 있다.
    - 이 제약 조건을 인터페이스의 일부로 만듦으로써 코드를 분석하지 않고도 인터페이스의 사용법을 이해할 수 있다.
  - 계약에 의한 설계와 의도를 드러내는 인터페이스
    - 메서드의 이름과 매개변수의 이름을 통해 오퍼레이션이 클라이언트에게 어떤 것을 제공하려고 하는지를 설명할 수 있다.
    - 즉 **의도를 드러내는 인터페이스를 만들면 오퍼레이선의 시그니처만으로도 어느 정도까지는 클라이언트와 서버가 협력을 위해 수행해야 하는 제약조건을 명시할 수 있다.**
    - 계약은 여기서 한 걸음 더 나아간다.
    - 메서드를 호출할 때 클라이언트 개발자는 매개변수에 전달할 수 있는 값을 가정해야하지만, 그 가정은 틀릴 수 있다.
    - **계약에 의한 설계는 잘못된 가정으로는 다른 객체와 협력할 수 없게 한다.**

  - 계약에 의한 설계를 구성하는 세 가지 요소

    - **사전조건(precondition)**: **메서드가 호출되기 위해 만족돼야 하는 조건**으로, 메서드의 요구 사항을 명시한다. 사전조건이 만족되지 않을 경우 메서드가 실행되어서는 안 되며, **사전조건을 만족시키는 것은 메서드를 실행하는 클라이언트의 의무**다.

    - **사후조건(postcondition)**: **메서드가 실행된 후에 클라이언트에게 보장해야 하는 조건**으로, 클라이언트가 사전조건을 만족시켰다면 메서드는 사후조건에 명시된 조건을 만족시켜야 한다. 만약 클라이언트가 사전조건을 만족시켰는데도 사후조건을 만족시키지 못한 경우에는 클라이언트에게 예외를 던져야 하며, **사후조건을 만족시키는 것은 서버의 의무**다.
    - **불변식(invariant)**: **항상 참이라고 보장되는 서버의 조건**으로, **메서드가 실행되는 도중에는 불변식을 만족시키지 못할 수도 있지만** 메서드를 실행하기 전이나 종료된 후에 불변식은 항상 참이어야 한다.

  - 위 세 가지 요소를 기술할 때는 실행 절차를 기술할 필요 없이 상태 변경만을 명시하기 때문에 코드를 이해하고 분석하기 쉬워진다.

    - 클라이언트 개발자는 사전조건에 명시된 조건을 만족시키지 않으면 메서드가 실행되지 않을 것이라는 사실을 잘 알고 있다.
    - 불변식을 사용하면 클래스의 의미를 쉽게 설명할 수 있고 클라이언트 개발자가 객체를 더욱 쉽게 예측할 수 있다.
    - 사후조건을 믿는다면 객체가 내부적으로 어떤 방식으로 동작하는지 걱정할 필요가 없다.
    - **세 요소에는 클라이언트 개발자가 알아야 하는 모든 것이 포함되어 있을 것이다.**



- 사전조건

  - 사전조건이란 메서드가 정상적으로 실행되기 위해 만족해야 하는 조건이다.
    - **사전조건을 만족시키는 것은 메서드를 실행하는 클라이언트의 의무다.**
    - 따라서 사전조건을 만족시키지 못해서 메서드가 실행되지 않을 경우 클라이언트에 버그가 있다는 것을 의미한다.
    - **사전조건이 만족되지 않을 경우 서버는 메서드를 실행할 의무가 없다.**
  - **일반적으로 사전조건은 메서드에 전달된 인자의 정합성을 체크하기 위해 사용된다.**
    - 예를 들어 특정 인자는 null이어서는 안 되고, 특정 인자는 1 이상의 값이어야 한다는 것 등이 있을 수 있다.
    - 이러한 조건들을 메서드의 사전조건으로 정의함으로써 메서드가 잘못된 값을 기반으로 실행되는 것을 방지할 수 있다.
  - Code Contracts는 사전조건을 정의하기 위한 `Contract.Requires` 메서드를 제공한다.
  
  ```c#
  public Reservation Reserve(Customer customer, int audienceCount)
  {
      Contract.Requires(customer != null);
      Contract.Requires(audienceCount >= 1);
      return new Reservation(customer, this, calculateFee(audienceCount), audienceCount);
  }
  ```
  
  - 위 예시에서 사전조건을 만족시킬 책임은 Reserve메서드를 호출하는 클라이언트에게 있다는 것을 기억해야한다.
    - 클라이언트가 사전조건을 만족시키지 못할 경우 `Reserve` 메서드는 최대한 빨리 실패해서 클라이언트에게 버그가 있다는 사실을 알린다.
    - `Contract.Requires` 메서드는 클라이언트가 계약에 명시된 조건을 만족시키지 못할 경우 `ContractException`을 발생시킨다.
  - 계약에 의한 설계를 사용하면 계약만을 위해 준비된 전용 표기법을 사용해 계약을 명확하게 표현할 수 있다.
    - 또한 계약을 일반 로직과 분리해서 서술함으로써 계약을 좀 더 두드러지게 강조할 수 있다.
    - 또한 계약이 메서드의 일부로 실행되도록 함으로써 계약을 강조할 수 있다.



- 사후조건

  - 사후조건은 메서드의 실행 결과가 올바른지 검사하고 실행 후에 객체가 유효한 상태로 남아 있는지를 검증한다.
    - 즉 사후조건을 통해 메서드를 호출한 후에 어떤 일이 일어났는지를 설명할 수 있다.
    - 클라이언트가 사전조건을 만족시켰는데도 서버가 사후조건을 만족시키지 못하면 서버에 버그가 있음을 의미한다.
  - **일반적으로 사후조건은 아래와 같은 세 가지 용도로 사용된다.**
    - 인스턴스 변수의 상태가 올바른지를 서술하기 위해
    - 메서드에 전달된 파라미터의 값이 올바르게 변경됐는지를 서술하기 위해
    - 반환값이 올바른지를 서술하기 위해
  - 다음과 같은 두 가지 이유로 사후조건을 정의하는 것이 사전조건을 정의하는 것 보다 어려울 수 있다.
    - 한 메서드 안에서 return문이 여러 번 나올 경우, return문마다 결과값이 올바른지 검증하는 코드를 추가해야 한다.
    - 실행 전과 실행 후의 값을 비교해야 하는 경우 실행 전의 값이 메서드 실행으로 인해 다른 값으로 변경됐을 수 있기 때문에 두 값을 비교하기 어려울 수 있다.
  - Code Contracts는 사후조건을 정의하기 위한 `Contract.Ensures` 메서드를 제공한다.
    - `Reserve` 메서드의 사후조건은 반환값인 `Reservation` 인스턴스가 null이어서는 안 된다는 것이다.
    - `Contract.Result<T>` 메서드가 `Reserve` 메서드의 실행 결과에 접근할 수 있게 해주는 메서드다.
    - 이 메서드는 제너릭 타입으로 메서드의 반환 타입에 대한 정보를 명시할 것을 요구한다.

  ```c#
  public Reservation Reserve(Customer customer, int audienceCount)
  {
      Contract.Requires(customer != null);
      Contract.Requires(audienceCount >= 1);
      Contract.Ensures(Contract.Result<Rservation>() != null);
      return new Reservation(customer, this, calculateFee(audienceCount), audienceCount);
  }
  ```



- 불변식

  - 불변식은 인스턴스 생명주기 전반에 걸쳐 지켜져야 하는 규칙을 명세한다.
    - **일반적으로 불변식은 객체 내부 상태와 관련이 있다.**
  - 불변식은 아래와 같은 두 가지 특성을 가진다.
    - 불변식은 클래스의 모든 인스턴스가 생성된 후에 만족돼야 한다. 즉 클래스에 정의된 모든 생성자는 불변식을 준수해야 한다는 것을 의미한다.
    - 불변식은 클라이언트에 의해 호출 가능한 모든 메서드에 의해 준수돼야 한다. 즉 메서드가 실행되는 중에는 객체의 상태가 불안정한 상태로 빠질 수 있기 때문에 불변식을 만족시킬 필요는 없지만 메서드 실행 전과 메서드 종료 후에는 항상 불변식을 만족하는 상태가 유지돼야 한다.
  - 불변식은 클래스의 모든 메서드의 사전조건과 사후조건에 추가되는 공통의 조건으로 생각할 수 있다.
    - 불변식은 메서드가 실행되기 전에 사전조건과 함께 실행되며, 메서드가 실행된 후에 사후조건과 함께 실행된다.
  - Code Contracts에서는 `Contract.Invariant` 메서드를 이용해 불변식을 정의할 수 있다.
    - 불변식은 생성자 실행 후, 메서드 실행 전, 메서드 실행 후에 호출되어야 한다.

  ```c#
  public class Screening
  {
      private Movie movie;
      private int sequence;
      private DateTime whenScreened;
      
      [ContractInvariationMethod]
      private void Invariant() {
          Contract.Invariant(movie != null);
          Contract.Invariant(sequence >= 1);
          Contract.Invariant(whenScreened > DateTime.Now);
          
      }
  }
  ```





## 계약에 의한 설계와 서브타이핑

- 계약에 의한 설계와 리스코프 치환 원칙

  - **계약에 의한 설계의 핵심은 클라이언트와 서버 사이의 견고한 협력을 위해 준수해야 하는 규약을 정의하는 것이다.**
    - 계약에 의한 설계는 클라이언트가 만족시켜야 하는 사전조건과 클라이언트의 관점에서 서버가 만족시켜야 하는 사후조건을 기술한다.
    - 계약에 의한 설계와 리스코프 치환 원칙이 만나는 지점이 바로 이곳이다.
    - 리스코프 치환 원칙은 슈퍼타입의 인스턴스와 협력하는 클라이언트의 관점에서 서브타입의 인스턴스가 슈퍼타입을 대체하더라도 협력에 지장이 없어야 한다는 것을 의미한다.
    - 따라서 서브타입이 리스코프 치환 원칙을 만족시키기 위해서는 클라이언트와 슈퍼타입 간에 체결된 계약을 준수해야한다.

  - 리스코프 치환 원칙의 규칙을 두 가지 종류로 세분화 할 수 있다.
    - 계약 규칙: 협력에 참여하는 객체에 대한 기대를 표현하는 규칙
    - 가변성 규칙: 교체 가능한 타입과 관련된 규칙

  - **계약 규칙은 슈퍼타입과 서브타입 사이의 사전조건, 사후조건, 불변식에 대해 서술할 수 있는 제약에 관한 규칙이다.**
    - **서브타입에 대한 더 강력한 사전조건을 정의할 수 없다.**
    - **서브타입에 대한 더 완화된 사후조건을 정의할 수 없다.**
    - **슈퍼타입의 불변식은 서브타입에서도 반드시 유지돼야 한다.**
  - **가변성 규칙은 파라미터와 리턴 타입의 변형과 관련된 규칙이다.**
    - **서브타입의 메서드 파라미터는 반공변성을 가져야 한다.**
    - **서브타입의 리턴 타입은 공변성을 가져야 한다.**
    - **서브타입은 슈퍼타입이 발생시키는 예외와 다른 타입의 예외를 발생시켜서는 안 된다.**





### 계약 규칙(Contract Rules)

- 계약 규칙

  - [합성과 유연한 설계]에서 살펴본 핸드폰 과금 시스템의 합성 시스템을 예시로 살펴본다.
    - 핸드폰 과금 시스템에서 `RatePolicy`는 기본 정책과 부가 정책을 구현하는 모든 객체들이 실체화해야 하는 인터페이스다.
    - 기본 정책과 부가 정책을 구현하는 모든 객체들(`RatePolicy`를 실체화한 객체들)이 정말로 `RatePolicy`의 서브타입인지(즉 리스코프 치환 원칙을 준수하는지) 확인하려면, 이들이 `RatePolicy`가 클라이언트와 체결한 계약을 준수하는지를 확인해야 한다.

  ```python
  class RatePolicy(ABC):
  
      @abstractmethod
      def calculate_fee(self, phone: Phone):
          ...
  ```

  - `RatePolicy`의 클라이언트인 `Phone` 클래스에 `publish_bill` 메서드를 추가한다.

  ```python
  class Phone(ABC):
  
      def __init__(self, rate_policy: RatePolicy):
          self._calls: List[Call] = []
          self._rate_policy = rate_policy
      
      def publish_bill(self):
          return Bill(self, self._rate_policy.calculate_fee(self._calls))
      
      # ...
  ```

  - `Phone.publish_bill` 메서드가 반환하는 `Bill` 클래스를 구현한다.

  ```python
  class Bill:
      
      def __init__(self, phone: Phone, fee: Money):
          if phone is None:
              raise ValueError
          
          if fee.is_lt(Money.wons(0)):
              raise ValueError
          
          self._phone = phone
          self._fee = fee
  ```

  - 사전조건과 사후조건
    - `Phone.publish_bill` 메서드에서 `RatePolicy.calculate_fee()`의 반환값을 `Bill`의 생성자에 전달하는 부분에 주목해야 한다.
    - 청구서의 요금은 최소한 0원보다 크거나 같아야하므로 `RatePolicy.calculate_fee()`의 반환값인 0보다 커야 한다.
    - 이것이 요금을 계산하는 `RatePolicy.calculate_fee()`의 사후조건이 된다.
    - 다음으로 `RatePolicy.calculate_fee`를 호출할 떄 클라이언트인 `Phone` 보장해야 하는 사전조건은 파라미터인 `calls`가 None이 아니어야 한다는 것이다.
    - `RatePolicy` 인터페이스를 구현하는 클래스가 `RatePolicy`의 서브타입이 되기 위해서는 위에서 정의한 사전조건과 사후조건을 만족해야 한다.

  - 먼저 기본 정책을 구현하는 추상 클래스인 `BasicRatePolicy`에 사전조건과 사후조건을 추가한다.

  ```python
  class BasicRatePolicy(RatePolicy):
  
      def calculate_fee(self, phone: Phone):
          # 사전조건
          assert phone.calls is not None
  
          result = Money.wons(0)
  
          for call in phone.calls:
              result = result.plus(self._calculate_call_fee(call))
              
          # 사후조건
          assert result.is_gte(Money.wons(0))
          
          return result
  ```

  - 부가정책을 구현하는 추상 클래스인 `AdditionalRatePolicy`에도 사전조건과 사후조건을 추가한다.

  ```python
  class AdditionalRatePolicy(RatePolicy):
  
      def calculate_fee(self, phone: Phone):
          # 사전조건
          assert phone.calls is not None
  
          fee = self._next.calculate_fee(phone)
          result = self._after_calculated(fee)
  
          # 사후조건
          assert result.is_gte(Money.wons(0))
          
          return result
  ```



- 서브타입에 더 강력한 사전조건을 정의할 수 없다.

  - 한 번도 통화가 발생하지 않은 `Phone`에 대한 청구서를 발행하는 시나리오를 생각해보자.

  ```python
  phone = Phone(RegularPolicy(Money(10), 10))
  bill = phone.publish_bill()
  ```

  - `Phone`의 코드를 보면 내부적으로 통화 목록을 유지하는 인스턴스 변수인 `_calls`를 선언하면서 동시에 빈 리스트로 초기화 한다.
    - 따라서 위 코드처럼 한 번도 `Phone.call` 메서드가 호출되지 않은 경우 `RatePolicy.calculate_fee` 메서드 인자로 빈 리스트가 전달될 것이다.
    - `calculate_fee`의 사전 조건에서는 인자가 None인 경우를 제외하고는 모든 값을 허용하기 때문에 위 코드는 사전조건을 위반하지 않는다.
  - `RatePolicy` 클래스의 부모 클래스인 `BasicRatePolicy`에 `calls`가 빈 리스트여서는 안 된다는 사전조건을 추가한다.
    - 이 경우, 위 에서 작성한 코드는 사전조건을 만족하지 않기 때문(`Phone.call`을 호출하지 않아 `_call`이 빈 배열이기 때문)에 정상적으로 실행되지 않을 것이다.

  ```python
  class BasicRatePolicy(RatePolicy):
  
      def calculate_fee(self, phone: Phone):
          # 사전조건
          assert phone.calls is not None
          assert len(phone) != 0
  
          result = Money.wons(0)
  
          for call in phone.calls:
              result = result.plus(self._calculate_call_fee(call))
              
          # 사후조건
          assert result.is_gte(Money.wons(0))
  
          return result
  ```

  - 위와 같이 변경하면 `BasicRatePolicy`는 `Phone`과 `RatePolicy` 사이에 맺은 계약을 위반하게 된다.

    - 클라이언트인 `Phone`은 오직 `RatePolicy` 인터페이스만 알고 있기 때문에 `RatePolicy`가 None을 제외한 어떤 `calls`라도 받아들인다고 가정한다.
    - 따라서 빈 리스트를 전달하더라도 문제가 발생하지 않는다고 예상할 것이다.
    - 하지만 `BasicRatePolicy`는 사전조건에 새로운 조건을 추가함으로써 `Phone`과 `RatePolicy` 사이에 맺은 계약을 위반한다.

    - `Phone`의 입장에서 더 이상 `RatePolicy`와 `BasicRatePolicy`는 동일하지 않다.
    - 하나는 원래의 약속을 지키는 신뢰할 수 있는 협력자이지만, 다른 하나는 그렇지 않다.
    - 클라이언트의 관점에서 `BasicRatePolicy`는 `RatePolicy`를 대체할 수 없기 때문에 리스코프 치환 원칙을 위반한다.
    - `BasicRateolicy`는 `RatePolicy`의 서브타입이 아닌 것이다.

  - **사전조건 강화는 리스코프 치환 원칙 위반이다.**
    - 위 예에서 알 수 있는 것 처럼 **서브타입이 슈퍼타입에 정의된 사전조건을 강화하면 기존에 체결된 계약을 위반하게 된다.**
    - 계약서에 명시된 의무보다 더 많은 의무를 짊어져야 한다는 사실을 순순히 납득하는 클라이언트는 없을 것이다.
    - 결국 **사전조건을 강화한 서브타입은 클라이언트의 입장에서 수용이 불가능하기 때문에 슈퍼타입을 대체할 수 없게 된다.**
  - 사전조건을 완화하는 것은 리스코프 치환 원칙을 위반하지 않는다.
    - 아래와 같이 `calls`에 `None`을 전달해도 예외가 발생하지 않게 수정해도 문제는 없다.
    - 사전조건을 보장해야 하는 책임은 클라이언트에게 있는데, 이미 클라이언트인 `Phone`은 `RatePolicy.calculate_fee` 메서드를 호출할 때 (`RatePolicy`와 맺은 계약 대로 ) 인자가 None이 아닌 값을 전달하도록 보장하고 있을 것이다.
    - 따라서 항상 인자는 None이 아닐 것이고 None 여부를 체크하는 조건문은 무시되기 때문에 수정된 사전조건은 협력에 영향을 미치지 않게 된다.

  ```python
  class BasicRatePolicy(RatePolicy):
  
      def calculate_fee(self, phone: Phone):
          # 사전조건
          if phone.calls is None:
              return Money.wons(0)
  ```




- 서브타입에 더 완화된 사후조건을 정의할 수 없다.

  - 사후조건은 `RatePolicy.calculate_fee` 메서드의 반환값이 0보다 커야 한다는 것이었다.
  - 아래는 10초당 100원을 부과하는 `RegularPolicy`에 1000원을 할인해주는 기본 요금 할인 정책(`RateDiscountPolicy`)를 적용하는 시나리오를 구현한 것이다.
    - 가입자의 통화 목록에는 단 한 번의 통화 내역만 존재하고 통화 시간은 1분이다.
    - 이 사용자는 통화시간 10초당 100원을 부과하는 요금제에 가입되어 있기 때문에 통화 요금은 600원일 것이다.
    - 문제는 사용자의 요금제에 1000원의 기본 할인 정책이 추가되어 있다는 것이다.
    - 따라서 최종 청구 금액은 -400원이 된다.

  ```python
  phone = Phone(RateDiscountPolicy(Money.wons(1000), RegularPolicy(Money(100), 10)))
  phone.call(Call(datetime(2024, 11, 11, 22, 30, 0), datetime(2024, 11, 11, 22, 31, 0)))
  bill = phone.publish_bill()
  ```

  - 사후조건을 만족시킬 책임은 서버에 있다.
    - 클라이언트인 `Phone`은 반환된 요금이 0보다 큰지를 확인할 의무가 없으며 사후조건을 위반한 책임은 전적으로 서버인 `RateDiscountablePolicy`가 져야한다.
    - `RateDiscountablePolicy`는 계약을 만족시킬 수 없다는 사실을 안 즉시 예외를 발생시키기 때문에 `calcaulte_fee` 오퍼레이션은 정상적으로 실행되지 않고 종료된다.
  - `calcaulte_fee` 오퍼레이션이 정상적으로 실행되도록 `RateDiscountablePolicy`의 부모 클래스인 `AdditionalRatePolicy`에서 사후조건을 완화시킨다.
    - 아래와 같이 사후조건을 주석으로 처리해서 마이너스 요금이 반환되더라도 예외가 발생하지 않도록 수정한다.
    - 이제 `AdditionalRatePolicy`는 마이너스 금액도 반환할 수 있기 때문에 `Phone`과의 협력을 문제없이 처리할 수 있다.

  ```python
  class AdditionalRatePolicy(RatePolicy):
  
      def calculate_fee(self, phone: Phone):
          # 사전조건
          assert phone.calls is not None
  
          fee = self._next.calculate_fee(phone)
          result = self._after_calculated(fee)
  
          # 사후조건을 주석처리
          # assert result.is_gte(Money.wons(0))
  
          return result
  ```

  - 그러나 `AdditionalRatePolicy`의 클라이언트가 아닌 `Bill`에서 예외가 발생한다.
    - `Bill`의 생성자에서는 인자로 전달된 `fee`가 마이너스 금액일 경우 예외를 던지도록 구현되어 있기 때문이다.

  ```python
  class Bill:
      
      def __init__(self, phone: Phone, fee: Money):
          if phone is None:
              raise ValueError
          
          if fee.is_lt(Money.wons(0)):
              raise ValueError
          
          # ...
  ```

  - 문제는 `AdditionalRatePolicy`가 마이너스 금액을 반환했다는 것이다.
    - 예외는 `Bill`에서 발생했지만, 이는 `Bill`의 문제가 아니다.
    - `Bill`의 입장에서 요금이 0원보다 크거나 같다고 가정하는 것은 자연스럽다.
    - 문제는 `AdditionalRatePolicy`가 사후조건을 완화함으로써 기존에 `Phone`과 `RatePolicy` 사이에 체결된 계약을 위반했기 때문에 발생한 것이다.
  - 사후조건을 완화한다는 것은 서버가 클라이언트에게 제공하겠다고 보장한 계약을 충족시켜주지 못한다는 것을 의미한다.
    - 서버는 계약을 위반했기 때문에 이제 계약은 더 이상 유효하지 않다.
    - 클라이언트인 `Phone` 입장에서 `AdditionalRatePolicy`는 더 이상 `RatePolicy`가 아니다.
    - 다시 말해 `AdditionalRatePolicy`는 더 이상 `RatePolicy`의 서브타입이 아니다.
  - **사후조건 완화는 리스코프 치환 원칙 위반이다.**
    - 계약서에 명시된 이익보다 더 적은 이익을 받게 된다는 사실을 납득할 수 있는 클라이언트는 없다.
    - 결국 **사후조건을 완화시키는 서버는 클라이언트의 관점에서 수용할 수 없기 때문에 슈퍼타입을 대체할 수 없다.**
  - 사후조건을 강화하는 경우에는 리스코프 치환 원칙을 위반하지 않는다.
    - `calculate_fee`가 100원보다 크거나 같은 금액을 반환하도록 사후조건을 강화한다.
    - `Phone`은 반환된 요금이 0보다 크기만 하다면 아무런 불만도 가지지 않기 때문에 이 변경은 클라이언트에게 아무런 영향도 미치지 않는다.

  ```python
  class AdditionalRatePolicy(RatePolicy):
  
      def calculate_fee(self, phone: Phone):
          # 사전조건
          assert phone.calls is not None
  
          fee = self._next.calculate_fee(phone)
          result = self._after_calculated(fee)
  
          # 사후조건 강화
          assert result.is_gte(Money.wons(100))
  
          return result
  ```





- **일찍 실패하기(Fail Fast)**
  - **문제의 원인을 파악할 수 있는 가장 빠른 방법은 문제가 발생하자마자 프로그램이 일찍 실패하게 만드는 것이다.**
    - 일반적으로 죽은 프로그램이 입히는 피해는 절름발이 프로그램이 끼치는 것보다 훨씬 덜한 법이다(*Hunt*)
  - 마이너스 금액을 그대로 사용하는 것 보다 처리를 종료하는 것이 올바른 선택이다.
    - 사후조건은 서버가 보장해야 한다는 것을 기억해야한다.
    - 클라이언트인 `Phone`은 서버인 `RatePolicy`가 계약에 명시된 사후조건을 만족시킬 것이라고 가정하기 때문에 반환값을 체크할 필요가 없다.
    - 따라서 `Phone`은 `RatePolicy`가 항상 플러스 금액을 반환할 것이라고 가정하고 별도의 확인 없이 반환값을 그대로 `Bill`의 생성자에게 전달한다.
    - 그리고 그 결과 원인에서 멀리 떨어진 곳에서 예외가 발생하게 된다.

  - `Phone`과 `RatePolicy` 사이의 협력을 종료시키지 않고 마이너스 금액을 그대로 사용하게 하면 반환된 값을 이용하는 어딘가에서는 문제가 발생할 것이다.
    - 게다가 문제가 발생한 `Bill`의 생성자는 마이너스 금액을 계산한 로직이 위치한 곳이 아니다.
    - 문제의 원인을 제공한 위치로부터 너무나도 멀리 떨어져 있다.
    - `RatePolicy`와 `Phone` 사이에서 예외를 발생시키면 이 문제를 해결할 수 있다.
    - 예외가 발생한 그 지점이 바로 문제가 발생한 바로 그곳이다.



- **슈퍼타입의 불변식은 서브타입에서도 반드시 유지돼야 한다.**

  - 불변식은 메서드가 실행되기 전과 후에 반드시 만족시켜야 하는 조건이다.
    - 모든 객체는 객체가 생성된 직후부터 소멸될 때까지 불변식을 만족시켜야 한다.
    - 하지만 메서드를 실행하는 도중에는 만족시키지 않아도 무방하다.
    - 생성자의 경우 시작 지점에는 불변식을 만족시키지 않겠지만 생성자가 종료되는 시점에는 불변식을 만족시켜야 한다.
  - `AdditionalRatePolicy`의 불변식
    - `AdditionalRatePolicy`에서 다음 요금제를 가리키는 `_next`는 None이어서는 안된다.
    - 따라서 `AdditionalRatePolicy`의 모든 메서드 실행 전과 후, 그리고 생성자의 마지막 지점에서 `_next`가 None이어서는 안 된다는 불변식을 만족시켜야 한다.

  ```python
  class AdditionalRatePolicy(RatePolicy):
  
      def __init__(self, next_: RatePolicy):
          self._next = next_
          # 불변식
          assert self._next is not None
  
      def calculate_fee(self, phone: Phone):
          # 불변식
          assert self._next is not None
  
          # 사전조건
          assert phone.calls is not None
  
          fee = self._next.calculate_fee(phone)
          result = self._after_calculated(fee)
  
          # 사후조건 강화
          assert result.is_gte(Money.wons(100))
  
          # 불변식
          assert self._next is not None
          
          return result
  ```

  - 그러나 위 코드에는 불변식을 위반할 수 있는 취약점이 존재한다.
    - 인스턴스 변수인 `_next`를 자식 클래스가 수정할 수 있다는 것이다.
    - 예를 들어 아래와 같이 `AdditionalRatePolicy`의 자식 클래스인 `RateDiscountPolicy`에 `change_next` 메서드가 추가됐다고 가정해보자.
    - `change_next`를 통해 `_next`의 값을 None으로 변경하는 것이 가능해졌고, 그렇게 할 경우 불변식이 유지되지 않는다.

  ```python
  class RateDiscountPolicy(AdditionalRatePolicy):
      
      def change_next(self, next_: RatePolicy):
          self._next = next_
  ```

  - 이 예는 계약의 관점에서 캡슐화의 중요성을 잘 보여준다.
    - 자식 클래스가 계약을 위반할 수 있는 코드를 작성하는 것을 막을 수 있는 유일한 방법은 인스턴스 변수의 가시성을 protected가 아니라 private로 만드는 것 뿐이다.
    - protected 인스턴스 변수를 가진 부모 클래스의 불변성은 자식클래스에 의해 언제라도 쉽게 무너질 수 있다.
    - 모든 인스턴스 변수의 가시성은 private으로 제한돼야 한다.
  - 만약 자식 클래스에서 인스턴스 변수의 상태를 변경하고 싶다면, 부모 클래스에 protected 메서드를 제공하고 이 메서드를 통해 불변식을 체크하게 해야 한다.

  ```python
  class AdditionalRatePolicy(RatePolicy):
  
      def __init__(self, next_: RatePolicy):
          self._next = None
          self._change_next(next_)
  
      def _change_next(self, next_: RatePolicy):
          self._next = next_
          # 불변식
          assert self._next is not None
  ```





### 가변성 규칙

- **서브타입은 슈퍼타입이 발생시키는 예외와 다른 타입의 예외를 발생시켜서는 안 된다.**

  > 부득이 Java로 작성한다.

  - `RatePolicy`의 `calculateFee` 오퍼레이션이 인자로 빈 리스트를 전달받았을 때 예외를 발생시키도록 계약을 수정한다.

  ```java
  public class EmptyCallException extends Exception { ... }
  
  public interface RatePolicy {
      Money calculateFee(List<Call> class) throws EmptyCallException;
  }
  ```

  - 이제 `BasicRatePolicy`는 슈퍼타입의 계약을 준수하기위해 아래와 같이 구현될 것이다.

  ```java
  public abstract class BasicRatePolicy implements RatePolicy {
      @Override
      public Money calculateFee(List<Call> calls) {
          if (calls == null || calls.isEmpty()) {
              throw new EmptyCallException();
          }
      }
  }
  ```

  - `RatePolicy`와 협력하는 메서드가 있다고 하자.
    - 이 메서드는 `EmptyCallException` 예외가 던져질 경우 이를 캐치한 후 0원을 반환한다.

  ```java
  public void calculate(RatePolicy policy, List<Call> calls) {
      try {
          return policy.calculateFee(calls);
      } catch(EmptyCallException ex) {
          return Money.ZERO;
      }
  } 
  ```

  - 하지만 `RatePolicy`를 구현하는 클래스가 `EmptyCallException` 예외가 아닌 다른 예외를 던질 경우 문제가 생긴다.
    - 예를 들어 아래와 같이 `AdditionalRatePolicy` 클래스가 `NoneElementException`을 던진다고 가정해보자.

  ```java
  public abstract class AdditionalRatePolicy implements RatePolicy {
      @Override
      public Money calculateFee(List<Call> calls) {
          if (calls == null || calls.isEmpty()) {
              throw new NoneElementException();
          }
      }
  }
  ```

  - 일반적으로 부모 클래스가 던지는 예외가 속한 상속 계층이 아닌 다른 상속 계층에 속하는 예외를 던질 경우 자식 클래스는 부모 클래스를 대체할 수 없다.

    - 이 경우 `AdditionalRatePolicy`는 `RatePolicy`를 대체할 수 없다.
    - 만약 `NoneElementException` 클래스가 `EmptyCallException` 클래스의 자식 클래스라면 `AdditionalRatePolicy`는 `RatePolicy`를 대체할 수 있을 것이다.
    - 그러나 상속 계층이 다르다면 하나의 catch문으로 두 예외를 모두 처리할 수 없기 때문에 `NoneElementException`은 예외 처리에서 잡히지 않게 된다.
    - 결과적으로 클라이언트 입장에서 협력의 결과가 예상을 벗어났기 때문에 `AdditionalRatePolicy`는 `RatePolicy`를 대체할 수 없다.

    - 따라서 서브타입이 아니다.

  - 자식 클래스에서 부모 클래스에서 정의하지 않은 예외를 발생시키는 경우에도 자식 클래스는 부모 클래스를 대체할 수 없다.

    - [서브클래싱과 서브타이핑]장에서 소개한 `Bird`를 상속받는 `Penguin`의 예가 이 경우에 해당한다.
    - `Bird`의 자식 클래스인 `Penguin`은 `fly` 메서드 안에서 `UnsupportedOperationException`을 던진다.
    - 개발자는 코드를 재사용하기 위해 `Bird`를 상속받았지만 `Penguin`은 날 수 없다는 제약조건을 만족시켜야 했기 때문에 `fly` 메서드의 실행을 막아야 했던 것이다.
    - 예외를 던짐으로써 날 수 있는 행동을 정상적으로 동작하지 않도록 만들었기 때문에 `Penguin`의 입장에서는 원하는 결과를 얻은 것이라고 생각할 수도 있다.
    - 하지만 클라이언트는 협력하는 모든 `Bird`가 날 수 있다고 생각할 것이다.
    - 클라이언트는 `Bird`의 인스턴스에게 `fly` 메서드를 전송했을 때 `UnsupportedOperationException` 예외가 던져지리가고 기대하지 않았을 것이다.
    - 따라서 클라이언트의 관점에서 `Penguin`은 `Bird`를 대체할 수 없다.

  - 계약을 위반하는 또 다른 예는 자식 클래스에서 메서드의 기능을 퇴화시키는 경우다.

    - 예를 들어 `Penguin`의 `fly` 메서드가 호출될 때 아무것도 하지 않는 경우가 있을 수 있다.
    - 이렇게 하면 `fly` 메시지에는 응답할 수 있지만 나는 기능 자체는 제거할 수 있으므로 좋은 선택이라고 생각할 수 있다.
    - 그러나 이 경우도 모든 `Bird`가 날 수 있다는 클라이언트의 관점에서는 올바르지 않다.



- 공변성
  - S가 T의 서브타입이라고 할 때, 프로그램의 어떤 위치에서 두 타입 사이의 치환 가능성을 다음과 같이 나눌 수 있다.
    - 공변성(covariance): S와 T 사이의 서브타입 관계가 그대로 유지된다. 이 경우 해당 위치에서 S가 T 대신 사용될 수 있다.
    - 반공변성(contravariance): S와 T 사이의 서브타입 관계가 역전된다. 이 경우 해당 위치에서 T가 S 대신 사용될 수 있다.
    - 무공변성(invariance): S와 T 사이에 아무런 관계도 존재하지 않는다. 따라서 S대신 T를 사용하거나 T 대신 S를 사용할 수 없다.
  - 주의할 점은 공변성과 반공변성의 지원 여부는 언어에 따라 다르다는 것이다.
    - 따라서 사용하는 언어가 공변성과 반공변성을 어느 정도로 지원하는지를 정확하게 이해한 후 사용해야 한다.

    - 예를 들어 Java는 아래에서 살펴볼 리턴 타입 공변성을 지원하지만, C#은 지원하지 않는다.

    - 또한 대부분의 객체지향 언어는 파라미터 반공변성을 지원하지 않는다.



- 서브타입의 리턴 타입은 공변성을 가져야한다.

  - 예를 들어 아래와 같은 관계를 가진 클래스들이 있다고 가정해보자.
    - `IndependentPublisher`는 `Publisher`의 자식클래스이다.
    - `Megazine`은 `Book`의 자식클래스이다.
    - `MegazineStore`는 `BookStall`의 자식클래스이다.
    - `BookStall`은 `IndependentPublisher`가 출간한 `Book`만 판매할 수 있으며. `MegazineStore` 역시 `IndependentPublisher`가 출간한 `Megazine`만 판매할 수 있다.

  ```python
  class Publisher:
      ...
  
  class IndependentPublisher(Publisher):
      ...
  
  class Book:
      def __init__(self, publisher: Publisher):
          self._publisher = publisher
      
  class Megazine(Book):
      def __init__(self, publisher: Publisher):
          self._publisher = publisher
  
  class BookStall:
      def sell(self, independent_publisher: IndependentPublisher):
          return Book(independent_publisher)
      
  class MegazineStore(BookStall):
      def sell(self, independent_publisher: IndependentPublisher):
          return Megazine(independent_publisher)
  ```

  - 책을 구매하는 `Customer` 클래스는 아래와 같다.
    - `BookStall`에게 `sell` 메시지를 전송해 책을 구매한다.

  ```python
  class Customer(BookStall):
  
      def __init__(self):
          self._book: Book = None
  
      def order(self, book_stall: BookStall):
          self._book = book_stall.sell(IndependentPublisher())
  ```

  - 공변성과 반공변성의 영역에서는 메서드의 리턴 타입과 파라미터 타입에 초점을 맞춰야한다.

    - 지금까지 살펴본 서브타이핑은 단순히 서브타입이 슈퍼타입의 모든 위치에서 대체 가능하다는 것이다.
    - 하지만 공변성과 반공변성의 영역에서는 타입의 관계가 아니라 메서드의 리턴 타입과 파라미터 타입에 초점을 맞춰야한다.

  - 리턴 타입 공변성(return type covariance)

    - `BookStall`의 `sell` 메서드는 `Book`의 인스턴스를 반환하고, `MegazineStore`의 `sell` 메서드는 `Megazine`의 인스턴스를 반환한다.
    - 여기서 주목해야 할 점은 슈퍼타입인 `BookStall`이 슈퍼타입인 `Book`을 반환하고, 서브타입인 `MegazineStore`가 서브타입인 `Megazine`를 반환한다는 점이다.

    - 리스코프 치환 원칙이 클라이언트 관점에서의 치환 가능성이므로 `BookStall`의 클라이언트 관점에서 리턴타입 공변성의 개념을 살펴볼 필요가 있다.
    - `Customer` 클래스의 `order` 메서드를 살펴보면 `BookStall`에게 `sell` 메시지를 전송하는 것을 알 수 있다.
    - `Customer`의 `order` 메서드는 `BookStall`에게 `sell` 메시지를 전송한 후 `Book` 타입의 인스턴스 변수에 대한 반환 값을 저장한다.
    - `BookStall`의 `sell` 메서드의 반환 타입이 `Book` 타입으로 선언돼 있기 때문에 이 코드는 직관적이다.
    - `MegazineStore`는 `BookStall`의 서브타입이므로 `BookStall`을 대신해서 협력할 수 있다.
    - 따라서 `Customer`는 자연스럽게  `MegazineStore`에서도 책을 구매할 수 있다.
    - `MegazineStore`의 `sell` 메서드는 `Megazine`의 인스턴스를 반환한다.
    - 그리고 `Customer`의 `order` 메서드는 반환된 `Megazine`을 `Book` 타입의 인스턴스 변수에 대입한다.
    - 업캐스팅에 의해 `Megzine` 역시 `Book`이기 때문에 `Customer`의 입장에서는 둘 사이의 차이를 알지 못할 것이다.
    - `Megazine`의 인스턴스가 반환되더라도 `Customer`의 입장에서는 `Megazine` 역시 `Book`의 일종이기 때문에 `MegazineStore`로 `BookStall`을 치환하더라도 문제가 없는 것이다.
    - `MegazineStall.sell`은 비록 반환 타입은 다르지만 정확하게 `BookStall.sell` 메서드를 대체할 수 있다.
    - 이처럼 부모 클래스에서 구현된 메서드를 자식 클래스에서 오버라이딩할 때 부모 클래스에서 선언한 반환타입의 서브타입으로 반환타입을 지정할 수 있는 특성을 리턴 타입 공변성이라고 부른다.
    - 간단히 말해 메서드를 구현한 클래스의 타입 계층 방향과 리턴 타입의 타입 계층 방향이 동일한 경우를 말한다.

  ```
  메서드 정의				파라미터 타입			
  BookStall		-		Publisher
  	↑						↑
  MegzineStore	-   IndependentPublisher
  ```

  - **슈퍼타입 대신 서브타입을 반환하는 것은 더 강력한 사후조건을 정의하는 것과 같다.**
    - 앞서 리스코프 치환 원칙과 관련된 계약 규칙을 설명할 때 서브타입에서 메서드의 사후조건이 강화되더라도 클라이언트 입장에서는 영향이 없었다.
    - 이와 마찬가지로 리턴타입 공변성은 계약에 의한 설계 관점에서 계약을 위반하지 않는다.
    - 앞의 예에서 메서드를 구현한 슈퍼타입(`BookStall`)이 리턴값으로 슈퍼타입(`Book`)을 반환할 경우 메서드를 오버라이딩하는 서브타입(`MegazineStore`)이 슈퍼타입에서 사용한 리턴 타입(`Book`)의 서브타입(`Megazine`)을 리턴 타입으로 사용하더라도 클라이언트(`Customer`)의 입장에서는 대체 가능한 것이다.



- 서브타입의 메서드 파리미터는 반공변성을 가져야 한다.

  - 책 판매 프로그램의 파라미터들
    - `Customer`는 `BookStall`의 `sell` 메서드를 호출할 때 파라미터로 `IndependentPublisher` 인스턴스를 전달한다.
    - 그리고 `BookStall`의 서브타입인 `MeazineStore`의 `sell` 메서드 역시 `IndependentPublisher` 타입의 인스턴스를 전달받도록 정의돼 있다.
    - 여기서 `IndependentPublisher`가 `Publisher`의 서브타입이라는 사실을 기억해야 한다.
    - 메서드의 파리머터가 `Publisher` 타입으로 정의돼 있더라도, 그 서브타입인 `IndependentPublisher`의 인스턴스를 전달하더라도 이전에 살펴본 업캐스팅을 통해 메서드가 정상적으로 동작한다.
  - `BookStall`의 자식 클래스인 `MegazineStore`에서 `sell` 메서드의 파라미터를 아래와 같이 `IndependentPublisher`의 슈퍼타입인 `Publisher`로 변경한다고 가정해보자.
    - 부모 클래스인 `BookStall`은 여전히 `IndependentPublisher`를 파라미터로 받는다.
    - `Customer.order` 메서드는 `BookStall.sell` 메서드에 `IndependentPublisher` 인스턴스를 전달한다.
    - `Bookstall` 대신 `MegazineStore` 인스턴스와 협력한다면 `IndependentPublisher` 인스턴스가 `MegazineStore.sell` 메서드의 파라미터로 전달될 것이다.
    - 이 때 파라미터 타입이 슈퍼타입인 `Publisher` 타입으로 선언되어 있기 때문에 `IndependentPublisher` 인스턴스가 전달되더라도 문제가 없다.

  ```python
  class BookStall:
      def sell(self, independent_publisher: IndependentPublisher):
          return Book(independent_publisher)
      
  class MegazineStore(BookStall):
      def sell(self, publisher: Publisher):
          return Megazine(publisher=publisher)
  ```

  - 파라미터 타입 반공변성(parameter type contravariance)
    - 이처럼 부모 클래스에서 구현된 메서드를 자식 클래스에서 오버라이딩할 때 파라미터 타입을 부모 클래스에서 사용한 파라미터 타입의 슈퍼타입을 지정할 수 있는 특성을 파라미터 반공변성이라고 부른다.
    - 간단히 말해서 메서드를 정의한 클래스의 타입 계층(`BookStall-MegazineStore`)과 파라미터의 타입 계층(`Publisher`-`IndependentPublisher`)의 방향이 반대인 경우 서브타입 관계를 만족한다는 것을 의미한다.

  ```
  메서드 정의				파라미터 타입			
  BookStall		-	IndependentPublisher
  	↑						↓
  MegzineStore	-		Publisher
  ```

  - **서브타입 대신 슈퍼타입을 파라미터로 받는 것은 더 약한 사전조건을 정의하는 것과 같다.**
    - 리스코프 치환 원칙과 관련된 계약 규칙을 설명할 때 서브타입에서 메서드의 사전조건이 약회되더라도 클라이언트 입장에서는 영향이 없었다.
    - 파리머타 타입 반공변성은 계약에 의한 설계 관점에서 계약을 위반하지 않는다.
    - 앞의 예에서 메서드를 구현한 슈퍼타입(`BookStall`)이 어떤 서브타입(`IndependentPublisher`)을 파라미터로 받을 경우 메서드를 오버라이딩하는 서브타입(`MegazineStore`)이 슈퍼타입에서 사용한 파라미터 타입의 슈퍼타입을 파리머타 타입으로 사용하더라도 클라이언트(`Customer`) 입장에서는 대체 가능한 것이다.



- 리턴 타입 공변성과 파라미터 타입 공변성을 사전조건과 사후조건의 관점에서 설명할 수도 있다.
  - 리턴 타입은 사후조건과 관련이 있으며 서브타입은 슈퍼타입에서 정의된 사후조건을 완화시킬 수는 없지만 강화할 수는 있다.
    - 따라서 슈퍼타입에서 정의한 리턴 타입보다 더 강화된 서브타입 인스턴스를 반환하는 것이 가능하다.
  - 서브타입은 슈퍼타입에서 정의한 것보다 더 강력한 사전조건을 정의할 수는 없지만 사전조건을 완화할 수는 있다.
    - 사전조건은 파리미터에 대한 제약조건이므로 이것은 슈퍼타입에서 정의한 파라미터 타입에 대한 제약을 좀 더 완화할 수 있다는 것을 의미한다.
    - 따라서 좀 더 완화된 파라미터에 해당하는 슈퍼타입을 파라미터로 받을 수 있는 것이다.



- 함수 타입과 서브타이핑

  - 익명 함수(anonymous function), 함수 리터럴(function literal), 람다 표현식(lambda expression)
    - 이들은 모두 이름 없는 메서드를 지칭하는 표현들이다.
    - 최근의 객체지향 언어들은 이름 없는 메서드를 정의할 수 있게 허용한다.

  ```scala
  // 파라미터 타입이 IndependentPublisher이고 반환 타입이 Book인 메서드
  def sell(publisher: IndependentPublisher): Book = new Book(publisher)
  
  // 위 메서드를 함수 리터럴로 표현하면 아래와 같다.
  (publisher: IndependentPublisher) => new Book(publisher)
  ```

  - 이름 없이 메서드를 정의하는 것을 허용하는 언어들은 객체의 타입뿐만 아니라 메서드의 타입을 정의할 수 있게 허용한다.
    - 그리고 타입에서 정의한 시그니처를 준수하는 메서드들을 이 타입의 인스턴스로 간주한다.
    - 위 예시의 경우 파라미터 타입과 반환 타입이 동일하기 때문에 모두 같은 타입의 인스턴스다.
    - 스칼라의 경우 아래와 같이 파라미터 타입과 반환 타입을 이용해 함수 타입을 정의할 수 있다.

  ```scala
  IndependentPublisher => Book
  ```

  - 함수에 대한 타입을 정의할 수 있을 뿐만 아니라 함수 타입의 서브타입도 정의할 수 있다.
    - 또한 객체의 서브타입이 슈퍼타입을 대체할 수 있는 것 처럼 서브타입 메서드가 슈퍼타입 메서드를 대체하는 것 역시 가능하다.





# 핵심

- 프로그래밍 언어로 작성된 인터페이스는 객체가 수신할 수 있는 메시지는 정의할 수 있지만 객체 사이의 의사소통 방식은 명확하게 정의할 수 없다.



- 계약에 의한 설계 개념은 인터페이스에 대해 프로그래밍하라는 원칙을 확장한 것이다.



- 계약에 의한 설계는 잘못된 가정으로는 다른 객체와 협력할 수 없게 한다.



- 계약에 의한 설계의 핵심은 클라이언트와 서버 사이의 견고한 협력을 위해 준수해야 하는 규약을 정의하는 것이다.



- 사전조건을 강화한 서브타입은 클라이언트의 입장에서 수용이 불가능하기 때문에 슈퍼타입을 대체할 수 없게 된다.



- 사후조건을 완화시키는 서버는 클라이언트의 관점에서 수용할 수 없기 때문에 슈퍼타입을 대체할 수 없다.



- 슈퍼타입의 불변식은 서브타입에서도 반드시 유지돼야 한다.



- 서브타입은 슈퍼타입이 발생시키는 예외와 다른 타입의 예외를 발생시켜서는 안 된다.
