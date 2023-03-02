# First-Class Continuation

- First-class continuation
  - 이전 장에서는 FAE의 small-step semantic을 정의하고 CPS로 FAE의 interpreter를 구현했다.
    - 개념적으로, continuation은 FAE program이 평가되는 중에 존재한다.
    - 그러나, programmer에게 노출되지는 않으므로, programmer는 FAE로 program을 작성할 때 continuation을 직접 활용할 수는 없다.
  - First-class entity
    - First-class entitiy는 value로 취급된다.
    - Value로 취급되기에, 변수가 가리키는 value가 될 수 있고, 함수 호출시에 인수가 될 수 있으며, 함수의 반환 값이 될 수 있다.
  - First-class continuation
    - First-class continuation은 value로 사용되는 continuation이다.
    - 만약 어떤 언어가 first-class continuation을 지원한다면, continuation은 변수의 값이 될 수 있고, 함수 호출시에 인수가 될 수 있으며, 함수의 반환값이 될 수 있다.
  - 함수와 continuation의 차이
    - Continuation은 value를 받고 연산을 수행하기에, 함수라고 생각할 수 있다.
    - Programmer는 함수를 호출하는 것과 같이 continuation을 호출할 수 있다.
    - 그러나 continuation은 함수와는 다르다.
    - 함수 호출은 value를 반환하고, 반환과 동시에 함수를 호출한 곳으로 돌아가 실행이 계속된다.
    - 반면에, continuation 호출은 호출한 곳으로 돌아가지 않는다.
    - Continuation이 호출되고, 평가되면, 실행은 종료된다(continuation은 남은 계산 전부를 의미하므로 continuation을 호출하여 모두 계산하고 나면 당연하게도 프로그램이 종료된다).
    - Continuation을 호출하는 것은 현재의 continuation을 호출된 continuation으로 변경시키는 것이다.
    - 이는 실행의 제어 흐름을 변경시킨다.
    - First-class continuation은 programmer가 복잡한 제어 흐름을 가진 연산을 간결하게 표현할 수 있게 해준다.
  - 이번 장에서 할 것
    - FAE에 first-class continuation을 추가한 KFAE를 정의한다.
    - KFAE의 small-step semantic을 정의하고, CPS로 KFAE의 인터프리터를 구현한다.



- Syntax

  - KFAE의 syntax는 아래와 같다.
    - $\cdots$는 FAE의 기존 syntax를 의미한다.

  $$
  e::=\cdots|\ vcc\ \ x\ in\ e
  $$

  - $vcc\ x\ in\ e$라는 표현식은 현재 continuation을 x의 값으로 하고, e를 계산하는 식이다.
    - vcc의 cc는 current continuation을 뜻한다.
    - cc는 $vcc\ x\ in\ e$ 전체가 환원 가능식일 때의 계속이다.
    - 즉, $vcc\ x\ in\ e$를 계산할 때의 계쏙이다.
    - x의 scope는 e전체이다.
    - Continuation이 호출되면, 현재 continuation이 호출 시점의 continuation을 대체한다.



- Semantics

