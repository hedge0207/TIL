# 객체 지향의 사실과 오해

## 협력하는 객체들의 공동체

- 객체들은 역할과 책임을 수행하며 서로 협력한다.
  - 각 객체들은 맡은 역할과 그에 따르는 책임이 있으며, 여러 객체는 애플리케이션의 기능을 구현하기 위해 서로 협력한다.
    - 애플리케이션의 기능은 더 작은 책임으로 분할되고, 책임은 적절한 역할을 수행할 수 있는 객체에 의해 수행된다.
    - 객체는 자신의 책임을 수행하는 도중에 다른 객체에게 도움을 요청하기도 한다.
    - 결국 시스템은 역할과 책임을 수행하는 객체로 분할되고, 시스템의 기능은 객체 간의 연쇄적인 요청과 응답의 흐름으로 구성된 협력으로 구현된다.
    - 객체지향 설계는 적절한 객체에게 적절한 책임을 할당하는 것에서 시작하며, 책임은 객체 지향 설계의 품질을 결정하는 가장 중요한 요소다.
    - 역할은 관련성 높은 책임의 집합이다.
  - 각 객체가 역할과 책임을 가지며, 여러 객체가 협력한다는 사실은 아래와 같은 것들을 시사한다.
    - 여러 객체가 동일한 역할을 수행할 수 있다. 즉 각 객체는 협력 하는 객체가 맡은 책임만 충실히 이행하면 그 객체에 대해 상세히 알 필요가 없다.
    - 역할은 대체 가능하다.
    - 책임을 수행하는 방법은 자율적으로 선택할 수 있다. 따라서 객체마다 동일한 요청에 대해 서로 다른 방식으로 응답을 줄 수 있으며, 이를 다형성이라 한다.
    - 하나의 객체가 동시에 여러 역할을 수행할 수 있다.



- 객체는 협력 속에 존재한다.

  - 객체는 충분히 협력적이어야한다.
    - 객체는 다른 객체의 요청에 충실히 귀를 기울이고 다른 객체에게도 적극적으로 도움을 요청해야한다.
    - 어떤 요청도 받지 않고, 어떤 요청도 하지 않는 전지 전능한 객체(god object)는 내부적인 복잡도에 의해 자멸한다.
  - 객체는 충분히 자율적이어야한다.
    - 객체는 협력적이어야하지만, 요청을 어떻게 처리할지는 자율적으로 결정하고 판단할 수 있어야한다.
    - 객체의 자율성은 객체의 내부와 외부를 명확히 구분하는 것에서 나온다.
    - 객체의 사적인 부분은 객체 외부에서 간섭할 수 없도록 차단해야 하며, 객체 외부에서는 접근이 허락된 수단을 통해서만 객체와 의사소통해야한다.
    - 즉 객체는 다른 객체가 무엇을 수행하는지만 알 뿐, 어떻게 수행하는지는 알 수 없다.

  - 상태, 행동과 자율성
    - 객체를 상태와 행동을 함께 지닌 실체라고 정의한다.
    - 이는 객체가 협력에 참여하기 위해서는 특정 행동도 해야 하지만, 행동에 필요한 상태도 가지고 있어야 한다는 것을 의미한다.
    - 객체가 협력에 참여하는 과정에서 스스로 판단하고 스스로 자율적인 존재로 남기 위해서는 필요한 행동과 객체를 함께 지니고 있어야한다.

  - 협력과 메시지
    - 객체들 사이의 의사소통은 오직 메시지를 통해서만 이루어진다.
    - 객체는 협력을 위해 다른 객체에게 메시지를 전송하고, 다른 객체로부터 메시지를 수신한다.
    - 메시지를 송신하는 객체를 송신자, 수신하는 객체를 수신자라 부른다.
  - 메서드와 자율성
    - 메시지를 받은 수신자는 자신만의 정해진 방법에 따라 메시지를 처리하는데, 메시지를 처리하는 방법을 메서드라 부른다.
    - 메시지를 수신한 객체가 실행 시간에 해당 메시지를 처리하기 위해 어떤 메서드를 사용할지 선택할 수 있으며, 이는 객체지향 프로그래밍을 다른 프로그래밍 패러다임과 구분짓는 핵심적인 특징 중 하나이다.
    - 절차적 언어는 프로시저 호출에 대한 실행 코드를 실행 시간(run time)이 아닌 컴파일 시간(compile time)에 결정한다.
    - 메시지와 메서드의 분리는 협력에 참여하는 객체들 간의 자율성을 증진시킨다.
    - 즉, 메시지를 특정 메서드와 연결하지 않고 분리함으로써, 객체는 같은 메시지도 다른 메서드로 처리할 수 있게 된다.
    - 이는 캡슐화와도 깊게 관련되어 있다.



- 객체지향의 본질
  - 위의 내용을 종합하면 객체지향은 아래와 같이 정리할 수 있다.
    - 시스템을 상호작용하는 자율적인 객체들의 공동체로 바라보고 객체를 이용해 시스템을 분할하는 방법이다.
    - 자율적인 객체란 상태와 행위를 함께 지니며 스스로 자기 자신을 책임지는 객체를 의미한다.
    - 객체는 시스템의 행위를 구현하기 위해 다른 객체와 협력하며, 각 객체는 협력 내에서 정해진 역할을 수행하고 역할은 관련된 책임의 집합이다.
    - 객체는 다른 객체와 협력하기 위해 메시지를 전송하고, 메시지를 수신한 객체는 메시지를 처리하는 데 적합한 메서드를 자율적으로 선택한다.
  - 객체지향과 클래스
    - 초기 객체지향 프로그래밍 언어의 초점은 새로운 개념의 데이터 추상화를 제공하는 클래스에 맞춰져 있었다.
    - 이 과정에서 클래스의 중요성이 과하게 부풀려졌고, 그 결과 사람들은 객체지향의 중심에 있어야 할 객체로부터 멀어져 갔다.
    - 클래스가 객체지향 프로그래밍 언어의 관점에서 매우 중요한 구성요소인 것은 분명하지만, 객체지향의 핵심이라고 말하기에는 무리가 있다.
    - 클래스를 강조하는 프로그래밍 언어적인 관점은 객체의 캡슐화를 저해하고, 클래스를 서로 강하게 결합시킨다.
    - 애플리케이션을 협력하는 객체들의 공동체가 아닌 클래스로 구성된 설계도로 보는 관점은 유연하고 확장 가능한 애플리케이션의 구축을 방해한다.
    - 클래스는 객체들의 협력 관계를 코드로 옮기는 도구에 불과하다.
    - 즉 클래스는 객체를 만드는 데 필요한 구현 메커니즘일 뿐이다.
    - 따라서 클래스의 구조와 메서드가 아니라 역할, 책임, 협력에 집중해야한다.





##  상태, 행동

- 객체지향 패러다임은 인간이 인지할 수 있는 다양한 객체들이 모여 현실 세계를 이루는 것처럼 소프트웨어의 세계 역시 인간이 인지할 수 있는 다양한 소프트웨어 객체들이 모여 이뤄져 있다는 믿음에서 출발한다.
  - 그러나 현실 세계와 소프트웨어 세계의 유사성은 여기까지일 뿐이다.
  - 객체지향 패러다임의 목적은 현실 세계를 모방하는 것이 아니라 현실 세계를 기반으로 새로운 세계를 창조하는 것이다.
  - 따라서 소프트웨어 세계에서 살아가는 객체는 현실 세계에 존재하는 객체와는 전혀 다른 모습을 보이는 것이 일반적이다.



- 객체의 정의
  - 객체란 식별 가능한 개체 또는 사물이다.
    - 구체적인 사물일 수도 있고 추상적인 개념일 수도 있다.
    - 객체는 구별 가능한 식별자, 특징적인 행동, 변경 가능한 상태를 가진다.
    - 소프트웨어 안에서 객체는 저장된 상태와 실행 가능한 코드를 통해 구현된다.
  - 객체의 상태를 결정하는 것은 행동이지만 행동의 결과를 결정하는 것은 상태다.
    - 따라서 객체가 실행하는 행동의 결과는 객체의 상태에 의존적이다.
  - 객체의 행동의 성공 여부는 이전에 어떤 행동들이 발생했는지에도 영향을 받는다.
    - 따라서 행동간의 순서도 중요하다.
  - 행동에 의해 객체의 상태가 변경되더라도 객체는 유일하게 식별이 가능하다.



- 상태
  - 상태가 왜 필요한가
    - 객체가 주변 환경과의 상호작용에 어떻게 반응하는가는 그 시점까지 객체에 어떤 일이 발생했느냐에 좌우된다.
    - 어떤 행동의 결과는 과게에 어떤 행동들이 일어났느냐에 의존한다.
    - 따라서 행동의 결과를 이해하기 위해서는 과거에 일어난 행동의 이력을 알고 있어야한다.
    - 그러나 과거에 발생한 행동의 이력을 통해 현재 발생한 행동의 결과를 판단하는 방식은 복잡하고 번거로우며 이해하기 어렵다.
    - 따라서 이 행동의 과정과 결과를 단순하게 기술하기 위해 상태라는 개념이 등장했다.
    - 상태를 이용하면 과거의 모든 행동 이력을 설명하지 않고도 행동의 결과를 쉽게 예측하고 설명할 수 있다.
    - 예를 들어 통장의 잔액은 이전의 입금되고 출금된 모든 행동들의 결과로 만들어진 상태이다.
    - 통장의 잔액이라는 상태를 보고 어느 금액까지 출금이 가능한지, 출금이라는 행동의 결과를 예측하고 설명할 수 있게 해준다.
  - 상태와 프로퍼티(property)
    - 세상에 존재하는 모든 것이 객체인 것은 아니다.
    - 숫자, 문자열, 양, 속도, 시간, 날짜, 참/거짓과 같은 단순한 값들은 객체가 아니다.
    - 단순한 값들은 그 자체로 독립적인 의미를 가지기보다는 다른 객체의 특성을 표현하는 데 사용된다.
    - 즉 객체의 상태를 표현하기 위해 사용된다.
    - 객체 역시 다른 객체의 상태를 표현하기 위해 사용될 수 있다.
    - 결과적으로 모든 객체의 상태는 단순한 값과 객체의 조합으로 표현될 수 있다.
    - 이 때 객체의 상태를 구성하는 모든 특징을 통틀어 객체의 프로퍼티라 한다.
    - 일반적으로 프로퍼티는 변경되지 않고 고정되기 때문에 정적이다.
    - 그러나 프로퍼티 값(property value)은 시간이 흐름에 따라 변경되기 때문에 동적이다.
  - 링크(link)와 속성(attribute)
    - 객체가 다른 객체 사이의 의미 있는 연결을 링크라 한다.
    - 객체와 객체 사이에는 링크가 존재해야만 요청을 보내고 받을 수 있다.
    - 링크는 객체가 다른 객체를 참조할 수 있다는 것을 의미하며, 이는 일반적으로 한 객체가 다른 객체의 식별자를 알고 있는 것으로 표현된다.
    - 객체를 구성하는 단순한 값은 속성이라고 한다.
    - 객체의 프로퍼티는 단순한 값인 속성과 다른 객체를 가리키는 링크라는 두 가지 종류의 조합으로 표현할 수 있다.
  - 상태의 정의
    - 위에서 살펴본 내용을 기반으로 객체의 상태를 아래와 같이 정의할 수 있다.
    - 상태는 특정 시점에 객체가 가지고 있는 정보의 집합으로 객체의 구조적 특징을 표현한다.
    - 객체의 상태는 객체에 존재하는 정적인 프로퍼티와 동적인 프로퍼티 값으로 구성된다.
    - 객체의 프로퍼티는 단순한 값인 속성과 다른 객체를 참조하는 링크로 구분할 수 있다.



- 행동
  - 상태와 행동
    - 객체의 상태를 변경하는 것은 객체의 자발적인 행동뿐이다.
    - 객체가 취하는 행동은 객체 자신의 상태를 변경시키며, 이는 행동이 객체의 상태 변경이라는 부수 효과(side effect)를 초래한다는 것을 의미한다.
    - 객체의 행동은 상태를 변경시키지만, 행동의 결과는 객체의 상태에 의존적이다.
  - 협력과 행동
    - 어떤 객체도 섬이 아니다.
    - 객체는 자신에게 주어진 책임을 완수하기 위해 다른 객체를 이용하고 다른 객체에게 서비스를 제공한다.
    - 객체가 다른 객체와 협력하는 유일한 방법은 다른 객체에게 요청을 보내는 것이다.
    - 객체는 수신된 메시지에 따라 자율적으로 행동하면서 협력에 참여하고, 그 결과로 자신의 상태를 변경한다.
    - 객체는 협력에 참여하는 과정에서 자신의 상태뿐 아니라 다른 객체의 상태 변경을 유발할 수도 있다.
  - 행동의 정의
    - 객체의 행동은 아래와 같이 정의할 수 있다.
    - 행동이란 외부의 요청 또는 수신된 메시지에 응답하기 위해 동작하고 반응하는 활동이다.
    - 행동의 결과로 객체는 자신의 상태를 변경하거나 다른 객체에게 메시지를 전달할 수 있다.
    - 객체는 다른 행동을 통해 다른 객체와의 협력에 참여하므로 행동은 외부에 가시적이어야한다.
    - 이때 행동이 외부에 가시적이라는 말은 어떻게 행동하는 지를 알려야 한다는 것이 아니라, 어떤 행동을 할 수 있는지를 알려야 한다는 의미이다.



- 상태 캡슐화

  - 현실 세계의 객체와 객체지향 세계의 객체 사이에는 중요한 차이가 있다.
    - 현실의 객체는 능동적인 객체와 수동적인 객체가 있지만, 객체지향의 세계에는 능동적인 객체만 존재한다는 점이다.
    - 예를 들어 현실 세계의 사람이라는 객체는 능동적으로 음료수를 마실 수 있지만, 음료수라는 객체는 스스로는 아무것도 할 수 없는 수동적인 존재다.
    - 따라서 음료를 마셔서 음료의 양이 줄었다면, 그것은 음료수라는 객체가 한 행동의 결과가 아니라, 인간이 마신다는 행동을 한 결과이다.
    - 그러나 객체지향 세계에서는 음료수가 스스로의 양을 줄일 수 있다.

  - 객체는 다른 객체에게 특정한 행동을 해줄 것을 요청하며, 해당 요청을 어떻게 처리할지는 요청을 받은 객체에게 달려있다.

    - 요청을 보낸 객체는 요청을 받은 객체가 자신의 요청대로 행동을 해줄 것이라는 것을 믿고 전달할 뿐이다.

    - 송신자가 수신자의 상태 변경을 기대하더라도, 수신자가 자신의 상태를 변경하지 않는다면 송신자가 간섭할 수 있는 어떤 여지도 없다.

    - 이것이 캡슐화의 의미로, 캡슐화는 이처럼 상태를 캡슐 안에 감춰둔 채 외부로 노출하지 않는다.

    - 객체가 외부에게 노출하는 것은 어떤 행동을 할 수 있는가 뿐이다.



- 식별자
  - 식별자란
    - 객체란 식별 가능한 경계를 가진 모든 사물을 의미한다.
    - 객체가 식별 가능하다는 것은 객체를 서로 구별할 수 있는 특정한 프로퍼티가 객체 안에 존재한다는 것을 의미한다.
    - 식별자란 어떤 객체를 다른 객체와 구분하는 데 사용하는 객체의 프로퍼티다.
  - 객체가 아닌 값은 식별자를 가지지 않는다.
    - 모든 객체가 식별자를 가진다는 것은 반대로 객체가 아닌 단순한 값은 식별자를 가지지 않는다는 것을 의미한다.
    - 객체가 가지는 프로퍼티의 타입 중 값과 객체의 가장 큰 차이점은 값은 식별자를 가지지 않는다는 점이다.
    - 그리고 시스템을 설계할 때 단순한 값과 객체의 차이점을 명확하게 구분하고 명시적으로 표현하는 것이 매우 중요하다.
  - 값(value)
    - 값은 숫자, 문자열, 날짜, 시간 등 변하지 않는 양을 모델링한다.
    - 흔히 값의 상태는 변하지 않기 때문에 불변 상태를 가진다고 말한다.
    - 값의 경우 두 인스턴스의 상태가 같다면 두 인스턴스를 같은 것으로 판단한다.
  - 값의 동등성(equality)
    - 값이 같은지 여부는 상태가 같은지를 이용해 판단한다.
    - 예를 들어 1이라는 숫자(값)는 모든 1이 동일한 상태를 가지며, 어떤 1도 다른 1과 다르지 않다.
    - 값의 상태가 같으면 두 인스턴스는 동일한 것으로 판단하고 다르면 두 인스턴스는 다른 것으로 판단한다.
    - 이처럼 상태를 이용해 두 값이 같은지 판단할 수 있는 성질을 동등성이라 한다.
    - 값은 오직 상태만을 이용해 동등성을 판단하기 때문에 인스턴스를 구별하기 위한 별도의 식별자를 필요로 하지 않는다.
  - 값의 불변성(immutability)
    - 상태를 이용해 두 값이 같은지를 판단할 수 있는 이유는 값의 상태가 변하지 않기 때문이다.
    - 값의 상태는 결코 변하지 않기 때문에 어떤 시점에 동일한 타입의 두 값이 같다면 언제까지라도 두 값은 동등한 상태를 유지할 것이다.
  - 객체는 가변 상태를 가진다.
    - 객체는 시간에 따라 변경되는 상태를 포함하며, 행동을 통해 다른 상태를 변경한다.
    - 따라서 객체는 가변 상태를 가진다고 말한다.
    - 타입이 같은 두 객체의 상태가 완전히 똑같더라도 두 객체는 독립적인 별개의 객체로 다뤄야 한다.
  - 객체의 동일성(identical)
    - 객체는 상태와 무관하게 두 객체를 동일하거나 다르다고 판단할 수 있는 프로퍼티를 가진다.
    - 두 객체의 상태가 다르더라도 식별자가 같다면 두 객체를 같은 객체로 판단할 수 있다.
    - 이처럼 식별자를 기반으로 객체가 같은지를 판단할 수 있는 성질을 동일성이라고 한다.
  - 식별자가 필요한 이유
    - 객체의 상태는 시간이 흐름에 따라 변화한다.
    - 따라서 가변적인 상태를 가지는 객체를 식별하기 위해서는 상태 변경에 독립적인 별도의 식별자를 이용할 수 밖에 없다.
    - 한 객체는 시간의 흐름에 따라 상태가 변화하더라도 객체의 상태가 변화한 것이지 다른 객체가 된 것은 아니며, 어느 시점에 서로 다른 두 객체의 상태가 동일하더라도 두 객체가 동일한 객체인 것은 아니다.
  - 값과 객체의 차이에 혼동이 생기는 이유
    - 대부분의 객체지향 프로그래밍 언어에서 값과 객체 모두 클래스를 이용해 구현되기 때문이다.
    - 객체 지향 프로그래밍 언어를 사용하면, 숫자는 Int라는 클래스로, 사람은 Person이라는 클래스로 정의할 수 밖에 없다.
    - 따라서 프로그래밍 언어의 관점에서 숫자는 Int 클래스로 부터 생성된 객체이며, 사람은 Person 클래스로부터 생성된 객체이다.
    - 객체지향 언어의 관점에서 값과 객체 모두 클래스로부터 생성된 객체이기 때문에 문맥에 따라 그 의미가 혼란스러워질 수 있다.
  - 값과 객체 사이의 혼동을 줄이기 위해 여기서는 객체와 값을 지칭하는 별도의 용어를 사용할 것이다.
    - 참조 객체(refrerence object) 또는 엔티티(entity)는 식별자를 지닌 전통적인 의미의 객체를 가리키는 용어이다.
    - 값 객체(value object)는 식별자를 가지지 않는 값을 가리키는 용어이다.



- 행동이 상태를 결정한다.
  - 객체 지향에 갓 입문한 사람들이 가장 쉽게 빠지는 함정은 상태를 중심으로 객체를 바라보는 것이다.
    - 초보자들은 먼저 객체에 필요한 상태가 무엇인지를 결정하고 그 상태에 필요한 행동을 결정한다.
    - 그러나 상태를 먼저 결정하고 행동을 나중에 결정하는 방법은 설계에 나쁜 영향을 미친다.
  - 행동보다 상태를 먼저 결정할 경우의 문제점
    - 상태가 객체 내부로 깔끔하게 캡슐화되지 못하고 공용 인터페이스에 그대로 노출되버릴 확률이 높아져 캡슐화를 저해한다.
    - 상태를 먼저 고려할 경우, 객체간의 협력이라는 맥락에서 멀리 벗어난 객체를 설계하게 되어 자연스럽게 협력에 적합하지 못한 객체를 생성하게 된다.
    - 상태의 초점을 맞춘 객체는 다양한 협력에 참여하기 어렵기 때문에 재사용성이 저하된다.
  - 협력에 참여하기 위한 객체를 생성하기 위해서는 상태 보다는 행동에 초점을 맞춰야한다.
    - 객체는 다른 객체와 협력하기 위해 존재하고, 객체의 행동은 객체가 협력에 참여하는 유일한 방법이다.
    - 따라서 객체가 적합한지를 결정하는 것은 그 객체의 행동이 아니라 행동이다.
    - 애플리케이션에 필요한 협력을 생각하고, 협력에 참여하는 데 필요한 상태를 생각한 후 행동에 필요한 상태가 무엇인지를 생각해야한다.
    - 결국 행동이 상태를 결정한다.





## 은유와 객체

- 객체지향이란 현실 세계의 모방인가?

  - 흔히 객체지향을 현실 세계의 모방이라고 표현한다.
    - 이러한 관점에서 객체지향 설계란 현실 세계에 존재하는 다양한 객체를 모방한 후 필요한 부분만 취해 소프트웨어 객체로 구현하는 과정이라고 설명한다.
    - 객체지향을 현실 세계의 추상화라고도 하는데, 그 안에는 현실 세계를 모방에서 단순화한다는 의미가 숨어 있따.
  - 그러나 객체지향 세계는 현실 세계의 단순한 모방이 아니다.
    - 소프트웨어 안에 구현된 상품 객체는 실제 세계의 상품과는 전혀 다른 양상을 띤다.
    - 소프트웨어 세계의 음료수는 스스로의 양을 줄일 수 있다.
    - 이것은 소프트웨어 상품이 실제 세계의 상품을 추상화한 것이 아니라 특성이 전혀 다른 어떤 것임을 의미한다.

  - 의인화(anthropomorphism)
    - 현실 세계의 객체와 달리 객체지향 세계의 모든 객체는 능동적으로 행동할 수 있다.
    - 레베카 워프스브록은 현실의 객체보다 더 많은 일을 할 수 있는 소프트웨어 객체의 특징을 의인화라고 부른다.
    - 객체지향 세계의 객체는 현실 속의 객체보다 더 많은 특징과 능력을 보유하고 있다.



- 은유
  - 객체지향의 세계와 현실 세계 사이에 전혀 상관이 없는 것은 아니다.
    - 모방이나 추상화의 수준이 아닌 다른 관점에서 유사성을 지니고 있다.
    - 현실 세계와 객체지향 세계 사이의 관계를 좀 더 정확하게 설명할 수 있는 단어는 은유이다.
    - 은유의 본질은 한 종류의 사물을 다른 종류의 사물 관점에서 이해하고 경험하는 데 있다.
  - 현실 속의 객체의 의미 일부가 소프트웨어 객체로 전달되기에 프로그램 내의 객체는 현실 속의 객체에 대한 은유다.
    - 현실 속의 전화기는 스스로 전화를 걸 수 없다고 하다. 
    - 그러나, 우리가 익히 알고 있는 현실의 전화기라는 개념을 이용해 소프트웨어 객체를 묘사하면 그 객체가 전화를 걸 수 있다는 사실을 쉽게 이해하고 기억할 수 있게 된다.
  - 은유관계에 있는 실제 객체의 이름을 소프트웨어 객체의 이름으로 사용하면 표현적 차이를 줄여 소프트웨어의 구조를 쉽게 예측할 수 있다.
    - 이를 통해 이해하기 쉽고 유지보수가 용이한 소프트웨어를 만들 수 있다.
    - 이것이 많은 객체지향 지침서들이 현실 세계의 도메인에서 사용되는 이름을 객체에게 부여하라고 가이드하는 이유이다.





## 타입과 추상화

- 추상화를 통한 복잡성 극복
  - 추상화란
    - 어떤 양상, 세부 사항, 구조를 좀 더 명확히 이해하기 위해 특정 절차나 물체를 의도적으로 생략하거나 감추는 방법이다.
    - 추상화의 첫 번째 차원은 구체적인 사물들 간의 공통점은 취하고 차이점은 버리는 일반화다.
    - 추상화의 두 번째 차원은 불필요한 세부 사항을 제거하는 것이다.
  - 추상화의 목적
    - 현실에 존재하는 다양한 현상 및 사물과 상호작용하기 위해서는 우선 현실을 이해해야한다.
    - 그러나 복잡한 현실 세계를 이해하는 것이 쉽지 않으므로 추상화를 통해 현실 세계를 단순화할 필요가 있다.
    - 객체지향에서 추상화의 목적도 이와 마찬가지로, 다양한 객체들을 추상화하여 객체들을 단순화 하는 것이 목적이다.
  - 훌륭한 추상화의 기준
    - 현실에서 출발하되 불필요한 부분을 도려내어 사물의 본질을 드러나게 해야 한다.
    - 추상화의 목적에 부합해야한다.



- 객체지향과 추상화
  - 그룹으로 나누어 단순화하기
    - 공통적인 특성을 지닌 객체들을 하나의 그룹으로 묶어 단순화할 수 있다.
    - 즉 객체를 여러 그룹으로 분류(classification)할 수 있다.
    - 객체지향 언어에서는 이 분류를 class로 표현한다.
  - 개념
    - 공통점을 기반으로 객체를 묶기 위한 그릇을 개념(concept)이라 한다.
    - 개념이란 일반적으로 우리가 인식하고 있는 다양한 사물이나 객체에 적용할 수 있는 아이디어나 관념을 뜻한다.
    - 각 객체는 특정한 개념을 표현하는 그룹의 일원으로 포함된다.
    - 객체에 어떤 개념을 적용하는 것이 가능해서 개념 그룹의 일원이 될 때 객체를 그 개념의 인스턴스라고 한다.
  - 개념의 세 가지 관점
    - 개념은 특정한 객체가 어떤 그룹에 속할 것인지를 결정한다.
    - 즉 어떤 객체에 어떤 개념이 적용됐다고 할 때는 그 개념이 부가하는 의미를 만족시킴으로써 다른 객체와 함께 해당 개념의 일원이 됐다는 것을 의미한다.
    - 일반적으로 객체의 분류장치로서의 개념을 이야기할 때는 아래의 세 가지 관점을 함께 언급한다.
    - 심볼(symbol): 개념을 가리키는 간략한 이름이나 명칭
    - 내연(intension): 개념의 완전한 정의를 나타내며 내연의 의미를 이용해 객체가 개념에 속하는지 여부를 확인할 수 있다.
    - 외연(extension): 개념에 속하는 모든 객체의 집합
  - 분류
    - 분류란 객체에 특정한 개념을 적용하는 작업이다.
    - 따라서 개념은 객체를 분류하기 위한 도구라고 불 수 있다.
    - 객체에 특정한 개념을 적용하기로 결심했을 때 우리는 그 객체를 특정한 집합의 멤버로 분류하고 있는 것이다.
    - 분류는 객체지향의 가장 중요한 개념 중 하나이며, 어떤 객체를 어떤 개념으로 분류할지가 객체지향의 품질을 결정한다.
    - 객체를 적절한 개념에 따라 분류하지 못한 애플리케이션은 유지보수가 어렵고 변화에 쉽게 대응하지 못한다.



- 타입

  - 타입은 개념이다.
    - 위에서 개념은 분류를 위해 사용되는 도구라고 했다.
    - 타입은 개념과 동일하다.
    - 따라서 타입이란 다양한 사물이나 객체에 적용할 수 있는 아이디어나 관념을 의미한다.
    - 어떤 객체에 어떤 타입을 적용할 수 있을 때 그 객체를 타입의 인스턴스라고 한다.
    - 타입의 인스턴스는 타입을 구성하는 외연인 객체 집합의 일원이 된다.

  - 전통적인 데이터 타입
    - 메모리의 세계에는 타입이 존재하지 않으며, 모든 데이터는 일련의 비트열로 구성된다.
    - 타입이 존재하지 않아 발생할 수 있는 혼동에 대처하기 위해 타입이 만들어졌다.
    - 타입에 따라 수행 가능한 작업과 불가능한 작업을 구분함으로써 데이터가 잘못 사용되는 것을 방지한다.
    - 결과적으로 타입 시스템의 목적은 데이터가 잘못 사용되지 않도록 제약사항을 부과하는 것이다.
    - 결국 타입은 데이터가 어떻게 사용되느냐에 관한 것이다.
    - 또한 타입에 속한 데이터를 메모리에 어떻게 표현하는지는 외부로부터 철저하게 감춰진다.
    - 결국 데이터 타입은 메모리 안에 저장된 데이터의 종류를 분류하는 데 사용하는 메모리 집합에 관한 메타데이터라 할 수 있으며, 이 메타데이터를 통해 암시적으로 어떤 종류의 연산이 해당 데이터에 수행될 수 있는지를 결정한다.
  - 객체와 타입
    - 전통적인 데이터 타입과 객체지향의 타입 사이에는 연관성이 존재한다.
    - 객체지향 프로그램을 작성할 때 객체를 일종의 데이터처럼 사용하게 되므로, 객체를 타입에 따라 분류하고 그 타입에 이름을 붙이는 것은 결국 프로그램에서 사용할 새로운 데이터 타입을 선언하는 것과 같다.
    - 객체가 수행하는 행동에 따라 어떤 객체가 어떤 타입에 속하는지가 결정된다.
    - 따라서 어떤 객체들이 동일한 행동을 수행할 수 있다면 그 객체들은 동일한 타입으로 분류될 수 있다.
    - 객체의 타입은 객체의 내부 표현과는 아무런 상관이 없다.
    - 따라서 객체의 행동을 가장 효과적으로 수행할 수만 있다면 객체 내부의 상태를 어떤 방식으로 표현하더라도 무방하다.
  - 행동이 우선이다.
    - 어떤 행동을 하느냐에 따라 객체의 타입이 결정되고, 객체의 타입은 객체 내부의 표현과는 아무런 상관이 없으므로 객체의 내부 표현 방식이 다르더라도 어떤 객체들이 동일하게 행동한다면 그 객체들은 동일한 타입에 속한다고 할 수 있다.
    - 결과적으로 동일한 책임을 수행하는 객체는 동일한 타입에 속한다고 할 수 있다.
    - 두 객체가 동일한 상태를 가지고 있다고 하더라도 다른 행동을 한다면 서로 다른 타입에 속한다고 할 수 있다.
    - 따라서 객체의 타입을 결정하는 것은 객체의 행동뿐이다.
    - 결국 같은 타입에 속한 객체는 행동만 동일하다면 서로 다른 데이터를 가질 수 있다.
    - 여기서 동일한 행동이란 동일한 책임을 의미하고, 동일한 책임은 동일한 메시지 수신을 의미한다.
    - 따라서 동일한 타입에 속한 객체는 내부의 데이터 표현 방식이 다르더라도 동일한 메시지를 수신하고 이를 처리할 수 있다.
    - 다만 내부의 표현 방식이 다르기 때문에 동일한 메시지를 처리하는 방식은 서로 다를 수 밖에 없으며, 이는 다형성에 의미를 부여한다.
    - 결론적으로 다형적인 객체들은 동일한 타입(혹은 타입 계층)에 속하게 된다.
  - 결국 타입은 앞에서 살펴본 추상화의 첫 번째 차원인 공통점은 취하고 차이점은 버리는 일반화의 산물이라고 할 수 있다.
    - 행동이라는 기준으로 공통적인 행동을 하는 객체들을 하나의 타입으로 일반화하는 것이다.



- 타입의 계층
  - 타입에는 계층이 존재한다.
    - 하나의 타입이 다른 타입이 할 수 있는 행동을 모두 할 수 있고, 거기에 추가적인 행동도 할 수 있을 때 두 타입 사이에 계층이 존재한다고 할 수 있다.
    - 집합의 관점에서 본다면, 추가적인 행동을 할 수 있는 타입이 다른 타입의 부분집합이라고 할 수 있다.
    - 계층을 나누는 기준도 행동이라는 것을 유념해야한다.
  - 일반화와 특수화
    - 타입과 타입 사이에는 일반화/특수화 관계가 존재할 수 있다.
    - 일반적이라는 말은 더 포괄적이라는 의미를 내포하고, 특수하다는 말은 일반적인 개념보다 범위가 더 좁다는 것을 의미한다.
    - 일반적인 타입이란 특수한 타입이 가진 모든 행동들 중에서 일부 행동만을 가지는 타입을 가리킨다.
    - 특수한 타입이란 일반적인 타입이 가진 모든 행동을 포함하지만 거기에 더해 자신만의 행동이 추가된 타입을 가리킨다.
    - 일반화/특수화 관계는 결정하는 것은 객체의 상태가 아닌 객체의 행동이라는 것이 중요하다.
    - 두 타입 간에 일반화/특수화 관계가 성립하려면 한 타입이 다른 타입보다 다른 타입보다 더 특수하게 행동해야하고, 반대로 한 타입은 다른 타입보다 더 일반적으로 행동해야한다.
  - 슈퍼타입과 서브타입
    - 일반화/특수화 관계는 좀 더 일반적인 한 타입과 좀 더 특수한 한 타입 간의 관계다.
    - 이 때 좀 더 일반적인 타입을 슈퍼타입이라 하고, 좀 더 특수한 타입을 서브타입이라고한다.
    - 일반적으로 서브타입은 슈퍼타입의 행위와 호환되기 때문에 서브타입은 슈퍼타입을 대체할 수 있어야한다.
  - 결국 타입의 계층은 앞에서 살펴본 추상화의 두 번째 차원인 중요한 부분을 강조하기 위해 불필요한 세부 사항을 단순화한 결과이다.
    - 일반화/특수화 계층은 객체지향에서 추상화의 두 번째 차원을 적절하게 사용하는 대표적인 예이다. 



- 정적 모델
  - 타입의 목적
    - 타입을 사용하는 이유는 시간에 따라 능동적으로 변하는 객체의 복잡성을 극복하기 위함이다.
    - 객체를 추상화하여 공통적인 객체를 묶어 단순화하기 위함이다.
    - 타입은 시간에 따라 동적으로 변하는 객체의 상태를 시간과 무관한 정적인 모습으로 다룰 수 있게 해준다.
  - 타입은 추상화다.
    - 타입을 이용하면 객체의 동적인 특성을 추상화할 수 있다.
    - 결국 타입은 시간에 따른 객체의 상태 변경이라는 복잡성을 단순화할 수 있는 효과적인 방법인 것이다.
  - 동적 모델과 정적 모델
    - 객체가 특정 시점에 구체적으로 가지는 상태를 스냅샷이라 한다.
    - 스냅샷처럼 실제로 객체가 살아 움직이는 동안 상태가 어떻게 변하고 행동하는지를 포착하는 것을 동적 모델이라 한다.
    - 반면에 타입 모델이란 객체가 가질 수 있는 모든 상태와 행동을 시간에 독립적으로 표현하는 것을 의미한다.
    - 타입 모델은 동적으로 변하는 객체의 상태가 아니라 객체가 속한 타입의 정적인 모습을 표현하기 때문에 정적 모델이라고도 한다.
  - 객체지향 애플리케이션을 설계하고 구현하기 위해서는 객체 관점의 동적 모델과 객체를 추상화한 타입 관점의 정적 모델을 적절히 혼용해야한다.
    - 동적 모델과 정적 모델의 구분은 실제로 프로그래밍이라는 행위와도 관련이 깊다.
    - 객체지향 프로그래밍 언어에서 클래스를 작성하는 시점에는 시스템을 정적인 관점에서 접근하는 것이다.
    - 그러나 실제로 애플리케이션을 실행해 객체의 상태 변경을 추적하고 디버깅하는 동안에는 객체의 동적인 모델을 탐험하고 있는 것이다.
  - 클래스
    - 객체지향 프로그래밍 언어에서 정적인 모델은 클래스를 이용해 구현된다.
    - 따라서 타입을 구현하는 가정 보편적인 방법은 클래스를 이용하는 것이다.
    - 그러나 클래스는 타입과 동일한 것이 아니다.
    - 타입은 객체를 분류하기 위해 사용하는 개념인 반면, 클래스는 단지 타입을 구현할 수 있는 여러 구현 메커니즘 중 하나일 뿐이다.
    - 그럼에도 객체지향 패러다임을 주도하는 대부분의 프로그래밍 언어는 클래스를 기반으로 하기 때문에 대부분의 사람들은 클래스와 타입을 동일한 개념이라고 생각한다.
    - 클래스와 타입을 구분하는 것은 설계를 유연하게 유지하기 위한 바탕이 된다.
    - 클래스는 타입의 구현 외에도 코드를 재사용하는 용도로도 사용되기 때문에 클래스와 타입을 동일시하는 것은 오해와 혼란을 불러일이킨다.





## 역할, 책임, 협력

- 협력
  - 협력은 한 객체가 다른 객체에 요청을 보내면서 시작된다.
  - 요청을 받은 객체가 해당 요청을 처리하기 위해 다른 객체에게 다시 요청을 보낼 수 있으며, 이런 식으로 하나의 요청에 여러 객체가 함께 협력할 수도 있다.
  - 요청을 받는 객체는 해당 요청을 처리할 수 있는 능력이 있기에 요청을 받는 것이다.



- 책임
  - 책임이란
    - 어떤 객체가 어떤 요청에 대해 대답해 줄 수 있거나, 적절한 행동을 할 의무가 있는 경우 해당 객체가 책임을 가진다고 말한다.
    - 결국 어떤 대상에 대한 요청은 그 대상이 요청을 처리할 책임이 있음을 암시한다.
  - 책임의 분류
    - 책임은 객체에 의해 정의되는 응집도 있는 행위의 집합으로, 객체가 알아야 하는 정보와 객체가 수행할 수 있는 행위에 대해 개략적으로 서술한 문장이다.
    - 즉 객체의 책임은 아래와 같이 두 가지로 분류할 수 있다. 
    - 객체가 무엇을 알고 있는가: 객체 자신에 대한 정보, 관련된 객체에 대한 정보, 자신이 계산한 것에 대한 정보 등
    - 무엇을 할 수 있는가: 객체를 생성하거나 계산하는 것, 다른 객체의 행동을 시작시키는 것, 다른 객체의 활동을 요청을 통해 제어하는 것 등
  - 책임은 객체 지향 설계의 품질을 결정하는 가장 중요한 요소다.
    - 객체지향 설계에서 가장 중요한 것은 적절한 객체에게 적절한 책임을 할당하는 것이다.
    - 책임이 불분명한 객체들은 불분명한 애플리케이션을 만든다.
  - 책임은 공용 인터페이스를 구성한다.
    - 객체의 책임을 이야기할 때는 일반적으로 외부에서 접근 가능한 공용 서비스의 관점에서 이야기한다.
    - 즉, 책임은 객체의 외부에 제공해 줄 수 있는 정보(객체가 아는 것)와 외부에 제공해 줄 수 있는 서비스(객체가 할 수 있는 것)의 목록이다.
    - 따라서 책임은 공용 인터페이스를 구성한다.
  - 책임과 메시지
    - 협력 안에서 객체는 다른 객체로부터 요청이 전송됐을 경우에만 자신에게 주어진 책임을 수행한다.
    - 결국 한 객체가 다른 객체에게 전송한 요청은 그 요청을 수신한 객체의 책임이 수행되게 한다.
    - 객체가 다른 객체에게 주어진 책임을 수행하도록 요청을 보내는 것을 메시지 전송이라 하며, **메시지는 협력을 위해 한 객체가 다른 객체로 접근할 수 있는 유일한 방법**이다.
    - 책임이 메시지 수신자의 관점에서 무엇을 할 수 있는지를 나열하는 것이라면, 메시지는 메시지를 주고 받은 두 객체 사이의 관계를 강조한 것이다.
    - 책임을 결정한 후 실제로 협력을 정제하면서 이를 메시지로 변환할 때는 하나의 책임이 여러 메시지로 분할되는 것이 일반적이다.



- 역할
  - 책임과 해당 책임을 수행하는 역할의 구분
    - 책임과 해당 책임을 수행하는 역할을 구분함으로써 재사용 가능하고 유연한 객체지향 설계가 가능해진다.
    - 예를 들어 식당에서 주문을 하는 상황을 가정해보자.
    - A, B, C라는 사람이 종업원으로 있는 식당에 E, F, G라는 손님이 들어왔다.
    - 식당에서 일하는 사람은 손님에게 주문을 받아야 다는 책임이 있다.
    - 식당에서 식사를 하는 사람은 종업원에게 음식을 요청해야 한다는 책임이 있다.
    - 따라서 아래와 같은 협력이 가능할 것이다.
    - E는 A에게 음식을 요청하고, A는 E에게 주문을 받았다는 응답을 보낸다.
    - F는 B에게 음식을 요청하고, B는 F에게 주문을 받았다는 응답을 보낸다.
    - G는 C에게 음식을 요청하고, C는 G에게 주문을 받았다는 응답을 보낸다.
    - 위와 같은 식으로 종업원 A, B, C와 E, F, G의 조합으로 여러 개의 상황이 생길 수 있다.
    - 예를 들어 F가 B, C에게 주문을 할 수 도 있고, G가 A, B에게 주문을 할 수도 있다.
    - 위와 동일한 상황을 A, B, C, D, E, F 라는 이름이 아니라 역할로 바꾸면 한 문장으로 표현이 가능하다.
    - "손님"은 "종업원"에게 음식을 요청하고, "종업원"은 "손님"에게 주문을 받았다는 응답을 보낸다.
  - 역할은 협력 내에서 다른 객체로 대체할 수 있음을 나타내는 일종의 표식이다.
    - 그러나 역할을 다른 객체로 대체하기 위해서는 각 역할이 수신할 수 있는 메시지를 동일한 방식으로 이해해야한다.
    - 역할을 대체할 수 있는 객체는 동일한 메시지를 이해할 수 있는 객체로 한정된다.
    - 메시지를 수신 받았다는 것은 해당 메시지를 처리해야 한다는 책임을 의미하므로 결국 동일한 역할을 수행할 수 있다는 것은 해당 객체들이 협력 내에서 동일한 책임의 집합을 수행할 수 있다는 것을 의미한다.
    - 동일한 역할을 수행하는 객체들이 동일한 메시지를 수신할 수 있기 때문에 동일한 책임을 수행할 수 있다는 것은 매우 중요한 개념이다.
    - 역할을 사용하여 유사한 협력을 추상화할 수 있고, 여러 객체가 협력에 참여할 수 있기에 협력이 좀 더 유연해지며, 재사용성이 높아진다.
    - 역할은 객체지향 설계의 단순성, 유연성, 재사용성을 뒷받침하는 핵심 개념이다.
  - 협력의 추상화
    - 역할의 가장 큰 가치는 협력 안에 여러 종류의 객체가 참여할 수 있게 함으로써 협력을 추상화할 수 있다는 것이다.
    - 구체적인 객체로 추상적인 역할을 대체해서 동일한 구조의 협력을 다양한 문맥에서 재사용할 수 있는 능력은 객체지향의 힘이다.
  - 역할의 대체 가능성
    - 역할은 협력 안에서 구체적인 객체로 대체될 수 있는 추상적인 협력자다.
    - 객체가 역할을 대체하기 위해서는 행동이 호환되어야 한다는 점을 기억해야한다.
    - 객체가 역할을 대체 가능하기 위해서는 협력 안에서 역할이 수행하는 모든 책임을 동일하게 수행할 수 있어야한다.
  - 역할과 객체의 타입
    - 객체는 역할에 주어진 책임 외에 다른 책임을 수행할 수도 있다는 사실도 기억해야한다.
    - 결국 객체는 역할이 암시하는 책임보다 더 많은 책임을 가질 수 있다.
    - 따라서 대부분의 경우에 객체의 타입과 역할 사이에는 일반화/특수화 관계가 성립한다.
    - 좀 더 일반적인 개념을 의미하는 역할은 일반화이며, 좀 더 구체적인 개념을 의미하는 객체의 타입은 특수화다.
    - 역할이 협력을 추상적으로 만들 수 있는 이유는 역할 자체가 객체의 추상화이기 때문이다.



- 객체 지향에 관한 흔한 오류들
  - 시스템에 필요한 데이터를 저장하기 위해 객체가 존재한다
    - 객체가 상태의 일부로 데이터를 포함하는 것은 사실이지만 데이터는 객체가 행위를 수행하는 데 필요한 재료일 뿐이다.
    - 객체가 존재하는 이유는 행위를 수행하며 협력에 참여하기 위해서로, 실제로 중요한 것은 객체의 행동, 즉 책임이다.
  - 객체지향은 클래스와 클래스 간의 관계를 표현하는 것이다.
    - 이는 시스템의 정적인 측면에 중점을 두는 것으로, 중요한 것은 정적인 클래스가 아니라 협력에 참여하는 동적인 객체이다.
    - 클래스는 단지 시스템에 필요한 객체를 표현하고 생성하기 위해 프로그래밍 언어가 제공하는 구현 메커니즘일 뿐이다.
    - 객체지향의 핵심은 클래스를 어떻게 구현할 것인가가 아니라 객체가 협력 안에서 어떤 책임과 역할을 수행할 것인지를 결정하는 것이다.
  - 객체지향 입문자들이 위와 같은 오류를 범하는 이유는 협력이라는 맥락을 고려하지 않고 각 객체를 독립적으로 바라보기 때문이다.
    - 예를 들어 자동차의 인스턴스를 모델링할 경우 대부분이 사람들은 자동차의 모양, 바퀴, 문과 같은 것들을 떠올릴 것이다.
    - 그리고 이 이미지를 기반으로 클래스를 구현하기 시작할 것이다.
    - 실제로 동작하는 애플리케이션을 구축하기 위해서는 자동차가 참여하는 협력을 우선적으로 고려해야한다.



- 객체의 모양을 결정하는 협력
  - 협력을 따라 흐르는 객체의 책임
    - 올바른 객체를 설계하기 위해서는 올바른 협력을 설계해야한다.
    - 협력을 설계한다는 것은 설계에 참여하는 객체들이 주고 받을 요청과 응답의 흐름을 결정한다는 것을 의미한다.
    - 이렇게 결정된 요청과 응답의 흐름은 객체가 역할에 참여하기 위해 수행할 책임이 된다.
    - 객체에게 책임을 할당하고 나면 책임은 객체가 외부에 제공하게 될 행동이 되며, 이를 결정한 후에 책임을 수행하는 데 필요한 데이터를 고민해야한다.
    - 여기까지 마친 후에야 클래스의 구현 방법을 결정해야한다.
  - 객체의 행위에 초점을 맞추기 위해서는 협력이라는 실행 문맥 안에서 책임을 분배해야한다.
    - 각 객체가 가져야 하는 상태와 행위에 대해 고민하기 전에 그 객체가 참여할 문맥인 협력을 정의하라.



- 책임 주도 설계(Responsibility-Driven Design)
  - 협력에 필요한 책임들을 식별하고 적합한 객체에게 책임을 할당하는 방식으로 애플리케이션을 설계한다.
    - 가장 널리 받아들여지는 객체지향 설계 방법론 중 하나이다.
    - 레베카 워프스브록이 고안했다.
  - 목적
    - 책임 주도 설계는 개별적인 객체의 상태가 아니라 객체의 책임과 상호작용에 집중한다.
    - 결과적으로 시스템은 스스로 자신을 책임질 수 있을 정도로 충분히 자율적인 동시에 다른 객체와 우호적으로 협력할 수 있을 정도로 충분히 협조적인 객체들로 이루어진 생태계를 구성하게 된다.
  - 설계 원리
    - 시스템의 기능을 더 작은 규모의 책임으로 분할하고 각 책임을 책임을 수행할 적절한 객체에게 할당하는 방식으로 애플리케이션을 설계한다.
    - 객체가 책임을 수행하는 도중에 스스로 처리할 수 없는 정보나 기능이 필요한 경우 적절한 객체를 찾아 필요한 작업을 요청한다.
    - 이 경우 요청된 작업을 수행하는 일은 작업을 위임받은 객체의 책임으로 변환된다.
    - 객체가 다른 객체에게 작업을 요청하는 행위를 통해 결과적으로 객체들 간의 협력 관계가 만들어진다.
    - 책임을 여러 종류의 객체가 수행할 수 있다면 협력자는 객체가 아니라 추상적인 역할로 대체된다.
  - 설계 방식
    - 시스템이 사용자에게 제공해야하는 기능인 시스템 책임을 파악한다.
    - 시스템 책임을 더 작은 책임으로 분할한다.
    - 분할된 책임을 수행할 수 있는 적절한 객체 또는 역할을 찾아 책임을  할당한다.
    - 객체가 책임을 수행하는 중에 다른 객체의 도움이 필요한 경우 이를 책임질 적절한 객체 또는 역할을 찾는다.
    - 해당 객체 또는 역할에게 책임을 할당함으로써 두 객체가 협력하게 한다.



- 테스트 주도 개발(Test-Driven Development)
  - 테스트 주도 개발은 테스트를 작성하는 것이 아니다.
    - 책임을 수행할 객체 또는 클라이언트가 기대하는 객체의 역할이 메시지를 수신할 때 어떤 결과를 반환하고 그 과정에서 어떤 객체와 협력할 것인지에 대한 기대를 코드의 형태로 작성하는 것이다.
    - 따라서 테스트 주도 개발은 객체지향에 대한 깊이 있는 지식을 요구한다.
    - 테스트를 작성하기 위해 객체의 메서드를 호출하고 반환값을 검증하는 것은 객체가 수행해야 하는 책임을 검증하는 것이다.
    - 테스트에 필요한 간접 입력 값을 제공하기 위해 스텁을 추가하거나 간접 출력 값을 검증하기 위해 목 객체를 사용하는 것은 객체와 협력해야 하는 협력자에 관해 관한 고민이 필요하다.
  - 테스트 주도 개발은 책임 주도 설계의 기본 개념을 따른다.
    - 테스트 주도 개발은 책임 주도 설계를 통해 도달하고자 하는 목적지에 테스트라는 안전장치를 통해 좀 더 빠르고 견고한 방법으로 도달할 수 있도록 해준다.
    - 따라서 책임 주도 설계에 대한 이해 없이는 테스트 주도 개발의 온전한 이점을 누리기 힘들다.





## 책임과 메시지

- 자율적인 책임
  - 객체지향 공동체를 구성하는 기본 단위는 '자율적'인 객체다.
    - 자율적인 객체란 스스로 정한 원칙에 따라 판단하고 스스로 의지를 기반으로 행동하는 객체를 말한다.
    - 객체가 아떤 행동을 하는 유일한 이유는 다른 객체로부터 요청을 받았기 때문이다.
    - 요청을 처리하기 위해 객체가 수행하는 행동을 책임이라 한다.
    - 따라서 자율적인 객체란 스스로의 의지와 판단에 따라 각자 맡은 책임을 수행하는 객체를 의미한다.
  - 자율적인 책임
    - 객체가 책임을 자율적으로 수행하기 위해서는 객체에게 할당되는 책임이 자율적이어야한다.
    - 책임이 구체적일수록 책임을 수행해야하는 객체의 자율성은 떨어진다.
  - 지나치게 추상적인 책임
    - 그렇다고 포괄적이고 추상적인 책임이 무조건 좋은 것도 아니다.
    - 책임이 수행 방법을 제한할 정도로 너무 구체적인 것도 문제지만 협력의 의도를 명확하게 표현하지 못할 정도로 추상적인 것 역시 문제다.
    - 추상적이고 포괄적인 책임은 유연함을 가져다주지만 협력에 참여할 수 있는 의도를 명확히 설명할 수 있는 수준 안에서 추상적이어야한다.



- 메시지와 메서드
  - 메시지 이름과 인자
    - 하나의 객체는 메시지를 전송함으로써 다른 객체에 접근하며, 메시지는 객체가 다른 객체에게 접근할 수 있는 유일한 방법이다.
    - 메시지는 이름을 가지고 있으며, 메시지를 처리하는 데 필요한 부가 정보인 인자(argument)를 가지고 있을 수 있다.
  - 결국 메시지 전송에서 가장 중요한 것은 메시지의 수신자, 메시지 이름, 메시지의 인자이다.
    - 예를 들어 손님 객체는 종업원 객체에게 다음과 같이 메시지 이름과 메시지의 인자를 사용하여 요청을 보낼 수 있다
    - `주문(메뉴, 개수)`
    - 또한 메시지는 누가 메시지를 받을 지도 중요하므로 아래와 같이 표현할 수도 있다.
    - `종업원.주문(메뉴, 개수)`
  - 메시지와 책임
    - 메시지를 수신받은 객체는 자신이 해당 메시지를 처리할 수 있는지를 확인한다.
    - 메시지를 처리할 수 있다는 이야기는 객체가 해당 메시지에 해당하는 행동을 수행해야 할 책임이 있다는 것을 의미한다.
    - 따라서 메시지는 책임과 연결된다.
  - 메서드
    - 객체가 메시지를 처리하기 위해 내부적으로 선택하는 방법을 메서드라한다.
    - 객체는 자신이 처리할 수 있는 메시지를 수신할 경우 주어진 책임을 다하기 위해 메시지를 처리할 방법, 즉 메서드를 정하게 된다.
    - 메시지는 어떻게 수행될 것인지는 명시하지 않으며, 단지 무엇이 실행되기를 바라는지만 명시한다.
    - 따라서 메시지를 처리하기 위해 어떤 메서드를 실행할 것인지는 전적으로 수신자의 결정에 좌우된다.
    - 수신자가 실행 시간에 메서드를 선택할 수 있다는 사실은 다른 프로그래밍 언어와 객체지향 프로그래밍 언어를 구분 짓는 핵심적인 특징 중 하나이다.
  - 다형성
    - 다형성이란 서로 다른 유형의 객체가 동일한 메시지에 대해 서로 다르게 반응하는 것을 의미한다.
    - 보다 구체적으로는 서로 다른 타입에 속하는 객체들이 동일한 메시지를 수신할 경우 서로 다른 메서드를 이용해 메시지를 처리할 수 있는 메커니즘을 가리킨다.
    - 서로 다른 객체들이 다형성을 만족시킨다는 것은 객체들이 동일한 책임을 공유한다는 것을 의미한다.
    - 다형성에서 중요한 것은 메시지 송신자의 관점이다.
    - 메시지 수신자들이 동일한 요청을 서로 다른 방식으로 처리하더라도 메시지 송신자의 관점에서 이 객체들은 동일한 책임을 수행하는 것이다.
    - 즉 송신자는 수신자들을 구별할 필요가 없다.
    - 다형성은 메시지 송신자의 관점에서 동일한 역할을 수행하는 다양한 타입의 객체와 협력할 수 있게 한다.
    - 기본적으로 다형성은 동일한 역할을 수행할 수 있는 객체들 사이의 대체 가능성을 의미한다.
    - 다형성은 객체들의 대체 가능성을 이용해 설계를 유연하고 재사용 가능하게 만든다.
    - 다형성을 사용하면 송신자가 수신자의 종류를 모르더라도 메시지를 전송할 수 있으며, 이는 수신자의 종류를 캡슐화한다.
  - 송신자는 수신자가 메시지를 처리할 수 있다는 사실만 알고 있는 상태에서 협력에 참여한다.
    - 이로 인해 아래와 같은 이점이 생긴다.
    - 수신자를 다른 타입의 객체로 대체해도 되기 때문에 송신자에 대한 파급 효과 없이 수신자를 유연하게 변경이 가능하다.
    - 송신자에 대한 파급 효과 없이 수신자를 변경할 수 있기에 세부적인 책임의 수행 방식을 쉽게 수정할 수 있다.
    - 수신자를 변경할 수 있기에 다양한 맥락에서 협력이 수행되는 방식을 재사용할 수 있다.



- 메시지를 따라라
  - 메시지는 객체 지향의 핵심이다.
    - 객체지향 애플리케이션의 중심 사상은 연쇄적으로 메시지를 전송하고 수신하는 객체들 사이의 협력 관계를 기반으로 사용자에게 유용한 기능을 제공하는 것이다.
    - 객체지향 패러다임으로의 전환은 시스템을 정적인 클래스들의 집합이 아니라 메시지를 주고 받는 동적인 객체들의 집합으로 바라보는 것에서 시작된다.
    - 훌륭한 객체지향 설계는 어떤 객체가 어떤 메시지를 이해할 수 있는가를 중심으로 객체 사이의 협력 관계를 구성하는 것이다.
  - 메시지가 아니라 데이터를 중심으로 객체를 설계하는 방식은 객체 내부 구조를 객체 정의의 일부로 만들기 때문에 객체의 자율성을 저해한다.
    - 객체 내부의 구조는 감춰져야한다.
    - 외부의 객체가 객체의 내부를 마음대로 변경할 수 있다면 객체가 자신의 의지에 따라 판단하고 행동할 수 있는 자율성이 저해된다.
    - 결국 객체 외부에서는 몰라도 되는 객체 내부 구조의 변경이 외부의 협력자에게까지 파급될 것이다.
  - 독립된 객체의 상태와 행위에 대해 고민하지 말고 시스템의 기능을 구현하기 위해 객체가 다른 객체에게 제공해야하는 메시지에 대해 고민하라.
    - 결국 객체를 이용하는 중요한 이유는 객체가 다른 객체가 필요로 하는 행위를 제공하기 때문이다.
    - 협력 관계 속에서 다른 객체에게 무엇을 제공해야 하고 다른 객체로부터 무엇을 얻어야 하는가라는 관점으로 접근해야만 객체의 책임을 확정할 수 있다.
    - 객체가 메시지를 선택하는 것이 아니라 메시지가 객체를 선택해야한다.
    - 메시지가 객체를 선택하게 하려면 메시지를 중심으로 협력을 설계해야한다.



- 책임-주도 설계 다시 살펴보기
  - 책임-주도 설계와 메시지
    - 객체는 책임을 완수하기 위해 다른 객체의 도움이 필요하다고 판단되면 도움을 요청하기 위해 어떤 메시지가 필요한지 결정한다.
    - 메시지를 결정한 후에는 메시지를 수신하기에 적합한 객체를 선택한다.
    - 수신자는 송신자가 기대한 대로 메시지를 처리할 책임이 있다.
    - 결과적으로 메시지가 수신자의 책임을 결정한다.
  - What/Who 사이클
    - 책임-주도 설계의 핵심은 어떤 행위가 필요한지를 먼저 결정한 후에 이 행위를 수행할 객체를 결정하는 것이다.
    - 이 과정을 흔히 What/Who 사이클이라 한다.
    - 여기서 어떤 행위가 바로 메시지다.
    - 결국 어떤 메시지가 필요한지를 먼저 결정한 후에 메시지를 처리할 수 있는 객체를 결정하는 것이다.
    - 객체의 행위를 결정하는 것은 객체 자체의 속성이 아니라는 점이 중요하다.
    - 책임-주도 설계의 관점에서는 어떤 객체가 어떤 특징을 가지고 있다고 해서 반드시 그와 관련된 행위를 수행할 것이라고 가정하지 않는다.
    - 반대로 행위를 먼저 식별한 후에 행위를 수행할 적절한 객체를 찾는다.
  - 협력이라는 문맥 안에서 객체의 책임을 결정하는 것은 메시지다.
    - 책임이 먼저 오고 객체가 책임을 따른다.
    - 결국 어떤 메시지를 수신하고 처리할 수 있느냐가 객체의 책임을 결정한다.



- 묻지 말고 시켜라(Tell, Don't Ask)
  - 묻지 말고 시켜라 혹은 데메테르 법칙(Law of Demeter)은 아래와 같은 협력 패턴을 의미한다.
    - 송신자는 수신자가 누구인지 모르기에 수신자에 대해 캐물을 수 없으며 캐물어서도 안 된다.
    - 단지 송신자는 수신자가 어떤 객체인지는 모르지만 자신이 전송한 메시지를 잘 처리할 것이라는 것을 믿고 메시지를 전송할 수 밖에 없다.
  - 묻지 말고 시켜라 스타일은 객체지향 애플리케이션이 자율적인 객체들의 공동체라는 사실을 강조한다.
    - 객체는 다른 객체의 결정에 간섭하지 말아야한다.
    - 모든 객체는 자신의 상태를 기반으로 스스로 결정을 내려야한다.
    - 객체가 아니라 메시지에 초점을 맞추는 것은 묻지 말고 시켜라 스타일의 설계를 증진시켜 객체의 자율성을 보장한다.



- 객체 인터페이스
  - 인터페이스
    - 일반적으로 인터페이스란 두 사물이 마주치는 경계 지점에서 서로 상호작용할 수 있게 이어주는 방법이나 장치를 의미한다.
    - 일반적으로 인터페이스는 아래와 같은 세 가지 특징을 가진다.
    - 인터페이스의 사용법을 익히기만 하면 내부 구조나 동작 방식을 몰라도 쉽게 대상을 조작할 수 있다.
    - 인터페이스 자체는 변경하지 않고 단순히 내부 구성이나 작동 방식만을 변경하는 것은 사용자에게 어떤 영향도 미치지 않는다.
    - 대상이 변경되더라도 동일한 인터페이스를 제공하기만 하면 아무런 문제 없이 상호작용 할 수 있다.
  - 협력에 참여하는 객체는 인터페이스를 통해 다른 객체와 상호작용한다.
  - 메시지가 인터페이스를 결정한다.
    - 객체가 다른 객체와 상호작용할 수 있는 유일한 방법은 메시지 전송이다.
    - 객체의 인터페이스는 객체가 수신할 수 있는 메시지의 목록으로 구성된다.
    - 객체가 어떤 메시지를 수신할 수 있는지가 객체가 제공하는 인터페이스의 모양을 빚는다.
  - 공용 인터페이스
    - 인터페이스는 외부에서 접근 가능한 공용 인터페이스와 내부에서만 접근 가능한 인터페이스로 구분된다.
    - 어떤 인터페이스건 메시지 전송을 통해서만 접근할 수 있다는 점은 동일하다.
    - 다만 송신자가 다른 객체인지, 객체 자신인지만 다를 뿐이다.



- 인터페이스와 구현의 분리

  - 객체 관점에서 생각하는 방법
    - 맷 와이스펠드는 객체지향적인 사고 방식을 이해하기 위해서는 아래 세 가지 원칙을 지켜야 한다고 주장했다.
    - 보다 추상적인 인터페이스: 추상적일수록 객체의 자율성이 높아진다.
    - 최소한의 인터페이스: 외부에서 사용할 필요가 없는 인터페이스는 외부로 노출하지 않음으로써 객체의 내부를 수정하더라도 외부에 미치는 영향을 최소화 할 수 있다.
    - 인터페이스와 구현 간에 차이가 있다는 점을 인식.

  - 구현
    - 객체지향에서 내부 구조와 동작 방식을 가리키는 고유의 용어는 구현이다.
    - 객체를 구성하지만 공용 인터페이스에 포함되지 않는 모든 것이 구현에 포함된다.
    - 객체는 상태를 가지며, 상태는 외부에 노출되지 않으므로 객체의 상태를 어떻게 표현할 것인가는 객체의 구현에 해당한다.
    - 객체는 행동을 가지며, 행동은 메시지를 수신했을 때만 실행되는 일종의 메시지 처리 방법으로 이를 메서드라 한다.
    - 메서드를 구성하는 코드 자체는 객체 외부에 노출되는 공용 인터페이스는 아니기에 객체의 구현 부분에 포함된다.
    - 객체의 외부와 내부을 분리하라는 것은 결국 객체의 공용 인터페이스와 구현을 명확하게 분리하라는 말과 동일하다.



- 인터페이스와 구현의 분리 원칙
  - 객체를 설계할 때 객체 외부에 노출되는 인터페이스와 객체 내부에 숨겨지는 구현을 명확하게 분리해서 고려해야 한다는 것을 의미한다.
    - 객체 설계의 핵심 원칙이다.
  - 인터페이스와 구현을 분리해야 하는 이유
    - 소프트웨어는 항상 변경되기 때문이다.
    - 수 많은 객체들이 물고 물리며 돌아가는 객체지향에서 어떤 객체를 수정했을 때 어떤 객체가 영향을 받는지 판단한는 것은 거의 불가능에 가깝다.
    - 객체의 모든 것이 외부에 공개돼 있다면 아무리 작은 부분을 수정하더라도 변경에 의한 파급효과가 애플리케이션의 구석구석까지 파고들 것이다.
    - 따라서 변경해도 무방한 부분과 변경했을 경우 파급 효과가 클 수 있는 부분을 분리해야한다.
    - 여기서 변경해도 무방한 부분이 구현이고, 파급 효과가 클 수 있는 부분이 공용 인터페이스이다.
    - 즉 둘을 분리함으로써 수신자 내부의 수정이 송신자에게까지 영향을 미치는 일을 방지하여 수신자와 송신자가 느슨한 인터페이스로만 결합되도록 해준다.



- 캡슐화

  - 객체의 자율성을 보존하기 위해 구현을 외부로부터 감추는 것을 의미한다.
    - 객체는 상태와 행위를 함께 캡슐화하여 충분히 협력적이고 만족스러울 정도로 자율적인 존재가 될 수 있다.
    - 캡슐화를 정보 은닉(information hiding)이라고 부르기도 한다.
    - 캡슐화는 상태와 행위의 캡슐화와 사적인 비밀의 캡슐화라는 두 가지 관점에서 사용된다.
  - 상태와 행위의 캡슐화(데이터 캡슐화)
    - 객체는 상태와 행위의 조합이다.
    - 객체는 자신의 상태를 관리하며 상태를 변경하고 외부에 응답할 수 있는 행동을 내부에 함께 보관한다.
    - 객체는 상태와 행동을 묶은 후 외부에서 반드시 접근해야만 하는 행위만 골라 공용 인터페이스를 통해 노출한다.
    - 따라서 데이터 캡슐화는 인터페이스와 구현을 분리하기 위한 전제 조건이다.
    - 객체가 자율적이기 위해서는 자기 자신의 상태를 스스로 관리할 수 있어야 하기 때문에 데이터 캡슐화는 자율적인 객체를 만들기 위한 전제 조건이기도 하다.

  - 사적인 비밀의 캡슐화
    - 외부의 객체가 자신의 내부 상태를 직접 관찰하거나 제어할 수 없도록 막기 위해 캡슐화를 한다는 관점이다.
    - 외부에 제공해야할 필요가 있는 것들만 공용 인터페이스에 포함시키고 개인적인 비밀은 공용 인터페이스의 뒤에 감춤으로써 외부의 불필요한 공격과 간섭으로부터 내부 상태를 격리한다.
    - 따라서 객체는 공용 인터페이스를 경계로 최대한의 자율성을 보장받을 수 있다.



- 책임의 자율성이 협력의 품질을 결정한다.
  - 자율적인 책임은 협력을 단순하게 만든다.
    - 자율적인 책임은 요청의 의도를 명확하게 표현함으로써 협력을 단순하고 이해하기 쉽게 만든다.
    - 자율적인 책임은 세부적인 사항들을 무시하고 의도를 드러내는 하나의 문장으로 표현함으로써 협력을 단순하게 만든다.
    - 예를 들어 손님 객체로 부터 주문을 받은 종업원 객체를 생각해보자.
    - 손님 객체로부터 "주문을 받는다"라는 단순한 요청을 받은 경우와 "테이블에서 세 걸음 떨어져서 손님의 눈을 똑바로 보고 웃으면서 주문지에 펜으로 적어가며 손님의 주문을 받는다"와 같은 상대적으로 구체적인 요청이 있을 때 전자는 주문을 받는다는 의도가 보다 명확히 드러나 협력을 단순하게 하지만 후자는 세부사항들 때문에 의도를 명확히 드러내기 힘들어 협력을 어렵게 만든다.
    - 즉 추상화가 쉬워진다.
  - 자율적인 책임은 객체의 외부와 내부를 명확하게 분리한다.
    - 책임이 자율적일수록 수신자가 메시지를 처리할 수 있을지를 판단하기 위해 알야 하는 것이 적어진다.
    - 따라서 외부에 노출할 인터페이스를 보다 명확하게 만들어준다.
    - 또한 외부에 노출해야 하는 공용 인터페이스를 최소화한다.
  - 자율적인 책임은 책임을 수행하는 내부적인 방법을 변경하더라도 외부에 영향을 미치지 않는다.
    - 책임이 자율적일수록 외부에 미치는 영향이 줄어든다.
    - 예를 들어 위 예시에서 주문지에 펜으로 적지 않고 테블릿에 적도록 종업원 객체의 구현이 변경된다면, 이는 외부 객체에도 영향을 미치게 된다.
    - 즉 결합도가 낮아진다.
  - 자율적인 책임은 협력 대상을 다양하게 선택할 수 있는 유연성을 제공한다.
    - 위 예시에서 "주문을 받는다"는 주문을 받을 수 있는 어떤 종업원이던 요청을 받을 수 있다.
    - 반면에 후자의 경우 손님에게 세 걸음 떨어질 수 있고, 눈을 똑바도 볼 수 있으며, 웃을 수 있고, 주문지와 펜이 있으며, 글을 쓸 수 있는 종업원만 요청을 받을 수 있다.
  - 객체가 수행하는 역할이 자율적일수록 객체의 존재 이유를 명확하게 표현할 수 있다.
    - 객체는 역할을 수행하기 위한 강하게 연관된 책임으로 구성되기 때문이다.
    - 즉 응집도가 높아진다.
