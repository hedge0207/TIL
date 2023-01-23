# Boxes

- Mutation
  - Mutation은 여러 language에서 널리 사용되는 중요한 개념이다.
  - 특히 명령형 programming에서 더욱 그렇지만, functional language도 mutation을 지원한다.
    - 그러나, Haskell이나 Coq 같은 소수의 순수 functional language에서는 어떠한 mutation도 허용하지 않는다.
  - 때때로 mutation은 프로그램의 실행을 예측하기 힘들게 만들고, 보다 error가 쉽게 발생할 수 있게 만들기도 한다.
    - 따라서 mutation을 사용할 때는 극도의 집중력을 발휘해야한다.
  - 이번 장에서는 FAE에 box를 추가한 BFAE를 만들어 볼 것이다.



- Box

  - Box란 memory 내에서 단일 값을 가지고 있는 cell을 말한다.
  - Box에 담긴 값은 box의 생성 이후에도 어느때나 수정 할 수 있다.
  - 실제 language에서는 찾기 힘든 개념이다.
    - 그럼에도 다루는 이유는 mutable object와 data structure 등의 mutation의 mechanisms에 대한 보다 나은 설명이 가능하기 때문이다.
    - Mutable object와 data structure의 경우 많은 language에서 찾울 수 있다.
  - Scala로 정의하기
    - Scala에서 mutable object는 일반화한 box로 볼 수 있다.
    - 아래 `Box` class에서 `value`는 mutable하게 선언했으므로 수정이 가능하다.

  ```scala
  // Box class는 value라는 하나의 field를 가진다.
  case class Box(var value: Any)
  val b = Box(3)
  b.value = 5
  println(b.value)	// 5
  ```



## Syntax 정의하기

- 위에서 살펴본 Scala code는 box와 관련된 세 가지 expression을 보여준다.
  - 새로운 box 생성
    - Box를 생성하기위해서 box의 초기값을 결정하기 위핸 expression이 있어야한다.
  - Box의 값 읽기
    - Box의 값을 읽기 위해서, box를 결정하기 위한 expression이 있어야한다.
  - Box의 값 변경하기
    - Box의 값을 변경하기 위해서, box를 결정하고, box의 새로운 값을 결정하기 위한 expression이 있어야한다.



- sequencing expression
  - 위의 expression들 외에 암시적으로 사용되는 또 다른 종류의 expression이 있어야한다.
    - 일반적으로 box를 수정하는 expression은 그 자체로는 쓸모가 없다.
    - 변경을 관찰하고, 변경 사항에 기반해서 추가적인 작업을 하는 다른 expression이 있어야 한다.
    - 이를 위해서 여러 개의 expression 들을 하나의 expression으로 묶을 필요가 있다.
  - expression을 sequencing expression이라 부른다.
  - 많은 실제 language들에서 허용되는 개념이다.



- BFAE의 syntax는 아래와 같이 정의할 수 있다.

  - FAE에서 정의한 syntax는 생략한다.

  $$
  e::=\cdots\ |\ box\ e\ |\ !e\ |\ e:=e\ |\ e;e
  $$

  - `box e`는 새로운 box를 생성하는 syntax이다.
    - `e`는 box의 초기값을 설정한다.
    - `e`의 계산 결과를 box에 넣는다.
    - 전체 expression의 결과는 새로 만들어진 box이다.
  - `!e`는 box의 값을 읽는 syntax이다.
    - `e`는 어떤 박스에서 읽을지를 결정한다.
  - `e_1 := e_2`는 box의 값을 변경하는 syntax이다.
    - `e_1`은 어떤 box의 값이 변경될지를 결정하고, `e_2`는 어떤 값으로 변경할지를 결정한다.
  - `e_1;e_2`는 sequencing expression으로, `e_1`은 평가되는 첫 번째 expression이고, `e_2`는 평가되는 두 번째 expression이다.
    - 단순화를 위해서 BFAE는 오직 두 expression의 연속만 허용한다(실제 language들에서는 이보다 더 많이 허용한다).
    - 여러 expression의 sequencing은 중첩된 sequencing으로 쉽게 표한할 수 있다.
    - 예를 들어 `e_1;e_2;e_3`는 `(e_1;e_2);e_3`로 표현할 수 있다.



## Semantic 정의하기

- Mutable memory 정의하기

  - Mutable memory를 정의하는 것은 BFAE의 semantic을 정의하는데 매우 중요하다.

  - Program의 memory를 store라 부른다.

    - Store는 box의 값을 기록한다.

  - 각각의 box는 address로 다른 box들과 구분된다.

    - 즉 각 box는 자신만의 고유한 address를 가지고 있다.
    - `Addr`이 전체 address의 집합이라 할 때, metavariable `a`는 `Addr`의 원소이다(`a ∈ Addr`).

  - Store는 `Addr`의 원소 중 유한한 일부만이 value를 가리키는 유한 부분 함수이다. 

    - Store가 address인 `a`와 `value`인 `v`를 mapping한다면, address가 `a`인 box의 값은 `v`일 것이다.
    - `Sto`가 모든 store의 집합이라 할 때, metavariable `M`은 `Sto`의 원소이다(`M ∈ Sto`).

    $$
    Sto = Addr \overset{\text{fin}} \nrightarrow V
    $$



- Box의 semantic 정의하기

  - BFAE의 value의 semantic 수정하기

    - Semantic을 정의할 때, box의 개념에 대한 깊이 있는 이해가 필요하지는 않다.
    - Box가 address에 의해 고유하게 식별되므로, semantic은 각 box에 대한 address라고도 볼 수 있다.
    - 그러므로, box를 가리키는 새로운 semantic element를 추가하는 대신, address를 BFAE의 value로 취급할 것이다.
    - 예를 들어, box를 생성하는 expression은 address로 평가된다.

  - 기존 value의 semantic에 address를 추가한다.
    $$
    v ::= \cdots |\ a
    $$

  - 앞으로의 설명에서 box와 address는 동의어로 사용할 것이다.



- Environment의 변경과 store의 변경의 차이
  - Environment의 변경
    - Environment에서의 변경사항은 변경을 발생시킨 expression의 subexpression들에게 전파된다.
    - 예를 들어 `val x e_1 in e_2`는 `x`를 추가하여 environment를 확장시키지만, `x`의 scope는 `e_2`이기 때문에, 이 확장은 `e_2`에게만 영향을 미친다.
    - 즉, 변수의 선언은 오직 그것의 subexpression에만 영향을 미친다.
    - 예를 들어 `(val x=e_1 in e_2)+e_3`에서 `e_3`는 `x`의 scope에 속해있지 않기때문에, 확장된 environment는 오직 `e_2`에서만 사용된다.
    - 이러한 이유로, binding과 environment는 local하고 modular하다고 할 수 있다.
  - store의 변경
    - Store의 경우 environment와는 다르게 store의 변경을 발생시킨 expression의 subexpression을 계산하는 데는 수정된 store가 필요하지 않지만, program의 다른 부분에서 필요하다.
    - 그러므로, expression으로 인해 store가 어떻게 변경되었는지가 중요하다.
    - `(x:=2);!x`가 있다고 가정해보자.
    - `x`가 box를 가리킨다면, `!x`은 `x:=2`로인해 box의 값이 2로 변경되었다는 사실을 알아야한다.
    - 그렇지 않다면, `x!`은 변경되기 전의 값을 가져와 잘못 된 결과를 산출할 것이기 때문이다.
    - `!x`는 `x:=2`의 subexpression이 아니라는 점을 주지해야한다(즉, subexpression이 아닌 program의 다른 부분이다).
    - 그러나,`x:=2`에서,  `x:=2`의 subexpression인 `2` 자체에 대한 평가의 경우에는,  `2`의 평가 뒤에 변경이 발생하기 때문에, box 값의 변경에 영향을 받아선 안된다.
    - 즉 store의 변경을 발생시킨 expression의 subexpression을 계산하는 데는 수정된 store가 필요하지 않지않다.
    - 만약 expression이 두 개의 subexpression을 포함하고 있다면, 첫 번째 expression을 평가하여 얻어진 store는 두 번째 subexpression의 평가에 사용되어야한다(`(x:=2);!x`라는 전체 expression의 첫 번째 subexpression인 `x:=2`로 인해 수정된 store가 두 번째 subexpression인 `!x`의 평가에 사용되는 것 처럼).
    - Store는 environment와 달리,  store의 변경이 남아 있는 전체 연산에 영향을 준다.
    - 이러한 이유로, store는 global하지만 modular하지 않다고 할 수 있다.



- Store의 semantic 정의하기

  - Box를 읽는 semantic 정의하기

    - `e!`을 평가하기 위해서는, environment뿐 아니라 store도 고려해야한다.
    - `e`가 box를 가리킨다면, store에는 box의 값이 저장되어 있을 것이며, 이 값이 `e!`의 결과값이다.
    - Store가 없다면, box의 값을 찾고 결과를 반환할 방법이 없다.

  - Box의 값을 생성/수정하는 semantic 정의하기

    - `box e`는 box의 값을 생성하고, `e_1=e_2`는 box의 값을 변경한다.
    - 둘 모두 store를 수정하는데, 이는, 위에서 살펴봤듯이, 새로운 identifier를 추가하여 environment를 확장하는 것과는 다르다.

    - 따라서 expression의 평가에는 environment뿐 아니라 store도 필요하며, expression은 output으로 결과 값과 함께 새로운 store도 반환해야한다.

  - 결국 `Env`, `Sto`, `E`, `V`, `Sto` 사이의 관계로 정의할 수 있다.

    - 앞쪽의 `Sto`는 input이고, 뒤쪽의 `Sto`는 output이다.

    $$
    ⇒⊆Env×Sto×E×V×Sto
    $$

    - `σ, M_1 ├ e ⇒ v, M2`는 오직 `σ`하에서  `e`가 `v`로 평가되고, `M_1`이 `M_2`로 변경될 때만 참이다.
    - 이렇게 semantic을 정의하는 것을 store-passing style이라 부른다.



- Subexpression들이 store를 변경할 수 있다면, subexpression들 사이의 평가 순서가 중요하다.
  - `x`가 box를 가리키고, 그 box가 1을 담고 있다고 가정해보자.
    - `(x:=2)+!x`에서 만약 덧셈의 왼쪽 피연산자가 오른쪽 피연산자보다 먼저 평가된다면, `!x`는 2로 평가될 것이다.
    - 따라서 semantic에 평가 순서에 대한 정보도 넣어줘야한다.
  - 이는 store를 넘김으로서 자연스럽게 해결된다.
    - 우리가 semantic을 정의할 때, 왼쪽 피연산자의 평가 결과로 나온 store를 오른쪽 피연산자의 평가시에 input으로 사용하면 된다.
    - 이렇게하면 왼쪽 피연산자가 먼저 평가되도록 순서를 정할 수 있다.



- 기존 expression들의 semantic 재정의하기

  - 값의 semantic 정의하기

    - `σ`하에서 `n`이 `n`으로 평가되고, `M`에서 `M`으로 store를 변경한다.

    $$
    σ, M ├ n ⇒n,M
    $$

  - Identifier의 semantic 정의하기

    - `x`가 `σ`의 domain이면, `σ`하에서 `x`가 `σ(x)`로 평가되고, `M`에서 `M`으로 store를 변경한다.

    $$
    x ∈ Domain(σ)\over σ, M├x⇒σ(x), M
    $$

  - Function의 semantic 정의하기

    - `σ`하에서 `λx.e`가 `<λx.e, σ>`로 평가되고, `M`에서 `M`으로 store를 변경한다.

    $$
    σ, M├λx.e⇒\left\langle λx.e, σ \right\rangle, M
    $$

  - Sequencing expression의 semantic 정의하기

    - 만약 `σ`하에서 `e_1`이 ` v_1`으로 평가되고, store가 `M`에서 `M_1`로 변경되며, `σ`하에서 `e_2`가 `v_2`로 평가되고, store가 `M_1`에서 `M_2`로 변경되면, `σ`하에서 `e_1:e_2`는 `v2`로 평가되고, store는 `M`에서 `M_2`로 변경된다.

    $$
    σ,M├e_1⇒v_1,M_1\ \ \ \ \ \ \ σ,M_1├e_2⇒v_2,M_2\over σ, M├ e_1;e_2⇒v_2, M_2
    $$

    - Sequencing expression 그 자체로는 store를 변경할 수 없으나, sequencing expression의 subexpression들은 가능하다.
    - 따라서 평가 순서에 대해서 고려해야한다.
    - `e_1`은 `e_2` 전에 평가된다.
    - `e_2`의 평가는 `e_1`에 의한 store의 모든 변경사항이 적용되어야한다.
    - 이를 위해서, `e_1`을 평가함으로써 얻어진 `M_1`을 `e_2`를 평가할 때 사용한다.
    - `e_1`의 결과는 버려지며, 최종 결과는 `e_2` 의 결과가 된다.

  - 덧셈의 semantic 정의하기

    - 만약 `σ`하에서 `e_1`이 ` n_1`으로 평가되고, store가 `M`에서 `M_1`로 변경되며, `σ`하에서 `e_2`가 `n_2`로 평가되고, store가 `M_1`에서 `M_2`로 변경되면, `σ`하에서 `e_1+e_2`는 `n_1+n_2`로 평가되고, store는 `M`에서 `M_2`로 변경된다.

    $$
    σ,M├e_1⇒n_1,M_1\ \ \ \ \ \ \ σ,M_1├e_2⇒n_2,M_2\over σ, M├ e_1+e_2⇒n_1+n_2, M_2
    $$

    - Sequencing expression과 마찬가지로 덧셈 자체는 store를 변경할 수 없으나, 덧셈의 subexpression들은 가능하다.
    - 따라서 sequencing expression과 마찬가지로 `M_1`을 `e_2`를 평가할 때 사용한다.

  - 뺄셈의 semantic 정의하기

    - 만약 `σ`하에서 `e_1`이 ` n_1`으로 평가되고, store가 `M`에서 `M_1`로 변경되며, `σ`하에서 `e_2`가 `n_2`로 평가되고, store가 `M_1`에서 `M_2`로 변경되면, `σ`하에서 `e_1-e_2`는 `n_1-n_2`로 평가되고, store는 `M`에서 `M_2`로 변경된다.

    $$
    σ,M├e_1⇒n_1,M_1\ \ \ \ \ \ \ σ,M_1├e_2⇒n_2,M_2\over σ, M├ e_1-e_2⇒n_1-n_2, M_2
    $$

    - 역시 마찬가지로 뺄셈 자체는 store를 변경할 수 없으나, 뺄셈의 subexpression들은 가능하다.
    - 따라서 sequencing expression과 마찬가지로 `M_1`을 `e_2`를 평가할 때 사용한다.

  - Function application(function call)의 semantic 정의하기

    - 만약 `e_1`이 `σ`하에서 `<λx.e, σ'>`로 평가되고 store가 `M`에서 `M_1`로 변경되며, `e_2`가 `σ`하에서 `v'`로 평가되고 store가 `M_1`에서 `M_2`로 변경되며, `e`가 `σ'[x↦v']`하에서 `v`로 평가되고 `M_2`에서 `M_3`로 변경되면, `e1 e2`는 `σ`하에서 v로 평가되고, store를 `M`에서 `M_3`로 변경한다.

    $$
    σ,M├ e_1⇒\left\langle λx.e, σ' \right\rangle, M_1\ \ \ \ \ σ, M_1├ e_2⇒v',M_2\ \ \ \ \ σ'[x↦v'], M_2⇒v,M_3\over σ,M├ e_1\ e_2⇒v, M_3
    $$

    - Closure의 body(`λx.e`에서 `e`)의 평가도 store의 상태를 변경시킬 수 있다.



- Box와 관련된 semantic 정의하기

  - `box e`의 semantic 정의하기

    - `e`의 결과는 box의 초기값이 되며, `box e`의 결과는 새로운 box이다.
    - `σ`하에서 `e`가 `v`로 평가되고, store를 `M`에서 `M_1`으로 변경시키며, `a`가 `M_1`의 domain이 아니면, `box e`는 `σ`하에서 `a`로 평가되고, store를 `M`에서 `M_1[a↦v]`로 변경시킨다.

    $$
    σ,M├e⇒v,M_1\ \ \ \ \ a\notin Domain(M_1)\over σ,M├box\ e⇒a,M_1[a↦v]
    $$

    - 초기값을 얻기 위해서 `e`가 먼저 평가된다.
    - 새로운 box의 address는 `M_1`에 속해선 안되며, store는 `e`를 평가하여 얻을 수 있다.
    - `M_1`에 속해선 안된다는 것 외에 address가 충족시켜야 하는 추가적인 조건은 없으므로, `M_1`에 속하지 않는 아무 주소나 선택하면 된다.

  - `e!`의 semantic 정의하기

    - `e`는 box로 평가되며, 어떤 box를 읽을지를 결정한다. 
    - 만일 `e`가 box로 평가되지 않는다면 run-time error가 발생한다.
    - `σ`하에서 `e`가 `a`로 평가되고, store가  `M`에서 `M_1`으로 변경되며, `a`가 `M_1`의 domain이면, `!e`는 `σ`하에서 `M_1(a)`로 평가되고, store는 `M`에서 `M_1` 으로 변경된다.

    $$
    σ,M├e⇒a,M_1\ \ \ \ \ a \in Domain(M_1)\over σ,M├!e⇒M_1(a),M_1
    $$

    - Box를 얻기 위해서는 `e`를 평가해야한다.
    - `e`의 결과는 `M_1`에 속한 address이다.
    - Box의 값을 찾기 위해 `M`이 아닌 `M_1`을 사용하는데. 이는 `e`가 새로운 box를 생성할 수도 있고 box를 결과값으로 반환할수도 있기 때문이다.
    - 예를 들어 `!(box 1)`과 같은 expression이 있을 때, 이 expression은 1로 평가된다.
    - Store의 최초 상태(`M`)는 비어 있는 상태지만, `box 1`을 평가하면서 새로운 Store(`M_1`)에 box의 address가 담기게 된다.
    - 만일 box를 `M`에서 찾는다면, `M`에는 아무 것도 저장되어 있지 않으므로 `box 1`을 통해 추가된 box를 찾을 수 없을 것이다.
    - 따라서 `M`이 아닌 `M_1`에서 `Box`의 값을 찾야한다.

  - `e_1:=e_2`의 semantic 정의하기

    - `e1`은 수정할 box를 결정하고, `e2`는 box의 새로운 값을 결정한다.
    - `e1`은 `!e`의 `e`와 마찬가지로 box로 평가되어야하며, 그렇지 않다면 run-time error가 발생한다.
    - `σ`하에서 `e_1`이 `a`로 평가되고, store를 `M`에서 `M_1`으로 변경하며, `σ`하에서 `e_2`가 `v`로 평가되고, store를 `M_1`에서 `M_2`로 변경되면, `σ`하에서 `e_1:=e_2`는 `v`로 평가되고, store는 `M`에서 `M_2[a↦v]`로 변경된다.

    $$
    σ,M├e_1⇒a,M_1\ \ \ \ \ σ,M_1├e_2⇒v,M_2\over σ, M├e_1:=e_2⇒v,M_2[a↦v]
    $$

    - `e1`이 address `a`로 평가된다면, store 내의 `a`와 관련 있는 값은 `e2`가 가리키는 값으로 변경된다.
    - 또한 변경된 값이 전체 표현식의 결과가 된다.



- Interpreter 수정하기

  - FAE의 기존 syntax에 box와 관련된 Syntax를 추가한다.

  ```scala
  sealed trait Expr
  ...
  case class NewBox(e: Expr) extends Expr
  case class OpenBox(b: Expr) extends Expr
  case class SetBox(b: Expr, e: Expr) extends Expr
  case class Seqn(l: Expr, r: Expr) extends Expr
  ```

  - Address를 정의한다.
    - Address의 type은 integer로 설정한다.

  ```scala
  type Addr = Int
  ```

  - Box를 표현하기 위해 `Value`의 새로운 변형인 `BoxV`를 정의한다.

  ```scala
  sealed trait Value
  ...
  case class BoxV(a: Addr) extends Value
  ```

  - Store를 정의한다.
    - Store의 type은 `Map[Addr, Value]`이다.

  ```scala
  type Sto = Map[Addr, Value]
  ```

  - `interp` 함수를 수정한다.
    - 기존에 parameter로 받던 expression, environment에 추가적으로 store를 받는다.

  ```scala
  def interp(e: Expr, env: Env, sto: Sto): (Value, Sto) =
      e match {
      ...
      }
  ```

  - 기존 case들이 store를 받도록 수정하고, Sequence case를 추가한다.
    - Seqn, Add, Sub, App case의 경우, store를 직접 수정하거나 읽어오지는 않는다.
    - 그러나 재귀 호출에서 반환된 store를 다음 재귀호출에 넘기거나 store를 결과로 사용한다.

  ```scala
  case Num(n) => (NumV(n), sto)
  case Id(x) => (env(x), sto)
  case Fun(x, b) => (CloV(x, b, env), sto)
  case Seqn(l, r) =>
      val (_, ls) = interp(l, env, sto)
      interp(r, env, ls)
  case Add(l, r) =>
  	// NumV(n)에는 l을 평가한 값이, ls에는 l을 평가한 결과를 저장한 store 값이 할당된다,
      val (NumV(n), ls) = interp(l, env, sto)
  	// l을 평가한 결과를 저장한 store인 ls를 rs의 평가에 store 값으로 넘긴다.
      val (NumV(m), rs) = interp(r, env, ls)
  	// 전체 반환값은 l을 평가한 값과 r을 평가한 값을 더한 값과, l과 r을 평가한 결과를 저장한 store를 넘긴다.
      (NumV(n + m), rs)
  case Sub(l, r) =>
      val (NumV(n), ls) = interp(l, env, sto)
      val (NumV(m), rs) = interp(r, env, ls)
      (NumV(n - m), rs)
  case App(f, a) =>
      val (CloV(x, b, fEnv), ls) = interp(f, env, sto)
      val (v, rs) = interp(a, env, ls)
      interp(b, fEnv + (x -> v), rs)
  ```
  
  - Box를 생성하는 case 추가하기
    - 먼저 box의 초기값을 계산한다.
    - 그 후, store에서 사용하지 않는 address를 계산하며, 이를 위해서 `maxOption` 메서드를 사용한다.
    - 만약 collection이 비어있다면, `maxOption`은 None을 반환한다.
    - 그렇지 않다면, `Some(n)`을 반환하며, 이 때 `n`은 collection 내의 가장 큰 값이다.
    - `getOrElse(0)`를 통해서 `Some(n)`에서 n을 가져오고, None에서 0을 가져온다.
    - `s.keys.maxOption.getOrElse(0)`는 store가 비어있으면 0을, 비어있지 않다면 store에서 가장 큰 key를 가져온다.
    - `a`는 `s.keys.maxOption.getOrElse(0)`가 반환한 값 보다 큰 값이며, 따라서 store에 속하지 않은 값이다.
    - 그러므로 `a`를 box에 address 값으로 사용할 수 있다.
    - 함수 전체의 반환값은 address와 확장된 store이다.
  
  ```scala
  case NewBox(e) =>
      val (v, s) = interp(e, env, sto)
      val a = s.keys.maxOption.getOrElse(0) + 1
      (BoxV(a), s + (a -> v))
  ```
  
  - Box를 읽어오는 case 추가하기
    - Address를 얻기 위해 subexpression을 평가한다.
    - 만약 결과값이 box가 아니라면, pattern matching이 실패하고 exception이 발생한다.
    - 함수 전체의 반환값은 box의 값과 subexpression을 평가하여 얻은 store이다.
  
  ```scala
  case OpenBox(e) =>
      val (BoxV(a), s) = interp(e, env, sto)
      (s(a), s)
  ```

  - Box의 값을 변경하는 case 추가하기
    - 두 개의 subexpression을 모두 평가하고, store를 변경한다.
  
  ```scala
  case SetBox(b, e) =>
      val (BoxV(a), bs) = interp(b, env, sto)
      val (v, es) = interp(e, env, bs)
      (v, es + (a -> v))
  ```







# Mutable Variables

- 앞서 정의한 BFAE는 box 기능을 제공한다.
  - Box는 mutable object와 data structure에 대한 좋은 추상이지만, mutable variable을 잘 설멍혀자는 못한다.
  - Box, mutable object, mutable data structure는 모두 어떤 값이지만, mutable variable은 이름이다.
    - Mutable variable은 이름(mutable variable)과 관련된 값 들(box, mutable object, mutable data structure)을 변경할 수 있도록 해준다.
    - 즉 mutable variable은 개념이며, box, mutable object, mutable data structure 등은 해당 개념에 속하는 실제 값들이다.
  - 많은 실제 language에서 mutable variable의 개념을 발견할 수 있다.
    - 단, OCaml이나 Haskell 같은 소수의 pure functional language에는 존재하지 않는다.



- Mutable variable의 semantic은 단순하다.

  - Mutable variable의 semantic은 단순히 "mutable variable은 value를 변경할 수 있다."는 것이다.
  - 그러나, mutable variable을 closure와 함께 사용한다면, 흥미로운 많은 것들을 할 수 있다.
    - 예를 들어 아래 code에 mutable variable인 `x`를 가지고 는 `makeCounter` 함수를 정의했다.
    - `makeCounter` 함수는 `counter` 함수를 정의하고 반환한다.
    - `counter`는 호출 될 때마다 `x`의 값을 증가시킨 후 반환한다.
    - 그렇다면, 아래 program은 무엇을 출력할까?
    - `1)`의 경우 1이 출력되겠지만, 나머지를 예측하는 것은 까다롭다.
    - 이러한 질문에 답하기위해서 mutable variable에 대한 명확한 semantic이 필요하다.

  ```scala
  def makeCounter(): () => Int = {
      var x = 0
      def counter(): Int = {
          x += 1
          x
      }
      counter
  }
  val counter1 = makeCounter()
  val counter2 = makeCounter()
  println(counter1())		// 1)
  println(counter2())		// 2)
  println(counter1())		// 3)
  println(counter2())		// 4)
  ```



- 이번 장에서 FAE에 mutable variable을 추가한 MFAE를 정의할 것이다.
  - Mutable variable의 semantic을 정의할 것이다. 
  - Mutable variable을 추가함으로써 function application(call)이 다른 방식으로도 접근 가능하다는 것을 알아볼 것이다.
  - Call-by-reference semantic이 무엇인지 알아보고, 그것이 call-by-value semantic과 무엇이 다른지도 알아볼 것이다.



- Syntax 정의하기

  - MFAE의 variable들은 mutable하다.
    - 따라서 variable의 value를 변경하기 위한 expression을 정의해야한다.
  - 기존 FAE의 semantic에 variable의 value를 변경하는 expression을 추가한다.
    - `x`는 변경될 variable이고, `e`는 variable의 새로운 값을 결정한다.
    - BFAE에의 `e1:=e2`와 달리, 할당의 왼쪽은 variable로 제한된다.
    - 이는 variable은 값이 아니기 때문이다. 즉, expression을 평가함으로서 variable을 얻을 수는 없다.

  $$
  e:=\cdots\ |\ x:=e
  $$

  - MFAE에는 BFAE와는 달리 sequencing expression이 없다.
    - Sequencing expression을 정의할 수 없는 것이 아니라, 정의하지 않는 것이다.
    - Sequencing expression은 lambda abstraction과 function application(call)으로 desugar할 수 있다.
    - `e1;e2`를 `(λx.e_2) e_1`로 변환 가능하다(`x`가 `e_2`에서 free indentifier가 아닌 경우에만).
    - `e1;e2`의  semantic은 `e1`을 먼저 평가하고 그 후에 `e2`를 평가한다.
    - `(λx.e_2) e_1`도 마찬가지로, `(λx.e_2)`가 먼저 closure로 평가되고(`e_2`는 평가되지 않는다) `e_1`이 평가된 후, 마지막으로 closure의 body인 `e_2`가 평가된다.
    - 또한 x가 `e_2`에서 free identifier가 아니기 때문에, 전체 expression의 결과는 `e_1`의 결과가 아닌 `e_2`의 결과이다.
    - 그러므로, desugaring이 잘 되었다고 할 수 있다.



- Semantic 정의의 접근 방식

  - MFAE는 mutation을 제공하기에, MFAE의 semantic도 BFAE의 semantic 처럼 store를 전달하는 방식을 사용한다.
    $$
    Sto = Addr \overset{\text{fin}} \nrightarrow V
    \\
    M \in Sto
    $$

  - MFAE의 semantic은 Env, Sto, E, V 그리고 Sto 사이의 관계로 정의할 수 있다.
    $$
    ⇒⊆Env×Sto×E×V×Sto
    $$

  - FAE와 마찬가지로 MFAE의 value도 interger이거나 closure이다.

    - BFAE에서 address도 value로 허용했던 것과 차이가 있다.
    - BFAE는 box의 생성이 address로 평가됐기에 address를 value로 취급했다.
    - 그러나 MFAE에도 mutation을 위해 address가 있기는 하지만, address는 오직 variable의 값을 추적하기 위해서만 사용한다.
    - 따라서 address는 값으로서 programmer에게 보여지지는 않는다.

  - MFAE의 environment는 identifier에서 address로의 유한 부분 함수이다.

    - 즉 input으로 들어온 identifier 중 일부만이 address를 반환한다.

    $$
    Env = Id \overset{\text{fin}} \nrightarrow Addr
    \\
    σ \in Env
    $$

    - Variable이 가리키는 value를 찾기 위해서 environment가 필요하다.
    - Variable이 immutable 했던 FAE의 경우, identifier를 input으로 받고, value를 반환하는 environment면 충분했다.
    - 그러나, variable이 mutable한 MFAE의 경우 value와 store를 함께 반환한다.
    - Environment는 output에 포함되지 않는다.
    - 그러므로 environment를 variable의 value의 변화를 기록하는 데 사용할 수 없다.
    - 반면에, store는 output에 포함되므로 variable의 value의 변화를 기록하는 데 사용할 수 있다.
    - 이는 variable을 mutable하게 만들기 위해서 store가 반드시 variable의 value를 저장하고 있어야한다는 것을 의미한다.
    - 특정 variable의 value가 특정 store의 특정 address에 저장되기 때문에 environment는 각 variable의 address를 알고 있어야한다.
    - 그럼 아예 environment를 semantic에서 없애고 store를 identifier에서 value로의 유한 부분 함수로 사용해도 되지 않느냐고 생각할 수도 있다.
    - 그러나 semantic에서 environment를 제거하는 것은 static scope를 사용하지 못하게 만든다.
    - Semantic에서 environment를 제거하고, store를 유한 부분 함수로 사용한다고 가정해보자.
    - `((λx.x:=1)0);x`와  같은 expression이 있을 때, 앞의 function application(`(λx.x:=1)0`)을 평가하기 위해서, argument의 value가 store에 저장되어야한다.
    - 즉 `(λx.x:=1)0`에 대한 평가가 끝나면, store에는 `x`가 1을 가리킨다는 정보가 저정된 상태가 된다.
    - 그 후 store는 `x`(`;`뒤의 `x`)의 평가에 넘겨지게 되고, store에서 `x`값인 1을 찾을 수 있다.
    - 그러나, static scope를 가지는 언어의 경우, `x`의 scope는 오직 `x:=1`뿐이다.
    - 따라서 function 밖의 `x`(`;`뒤의 `x`)는 free identifier이므로, `((λx.x:=1)0);x`는 run-time error를 뱉는 것이 정상이다.
    - 그러나 environment를 사용하지 않으면, static scope를 적용할 수 없게 되어(즉, 모든 값이 전역으로 관리된다) 위 expression이 error를 발생시키지 않게 된다.
    - Environment는 static scope를 가능하게 하고, store는 variable을 mutable하게 만드므로, semantic은 반드시 둘 모두를 포함해야 한다.



- Semantic 정의하기

  - Identifier의 semantic 정의하기

    - Environment의 정의가 변경되었기 때문에, identifier의 semantic도 변경이 필요하다.
    - Environment는 주어진 identifier에 대한 address를 가지고 있고, store는 주어진 address에 대한 value를 가지고 있다.
    - 그러므로, variable의 값을 찾기 위해서는 두 단계를 거쳐야한다.
    - 먼저 variable의 address를 environment에서 찾고, store에서 address로 value를 찾아야한다.
    - 만약 `x`가 `σ`의 domain이고, `σ(x)`(address)가 M의 domain이면, `x`는 `σ`하에서 `M(σ(x))`로 평가되고, store는 `M`에서 `M`으로 변경된다.

    $$
    x \in Domain(σ)\ \ \ \ \ σ(x)\in Domain(M) \over σ, M├x⇒M(σ(x)), M
    $$

  - Function application의 semantic 정의하기

    - BFAE의 box처럼, MFAE의 각 variable들은 자신들의 address를 가지고 있다.
    - 새로운 variable은 오직 function application을 통해서만 정의될 수 있다.
    - 그러므로, function application은 새로운 address를 생성하는 유일한 expression이다.
    - `e_1`이 `σ`하에서 `<λx.e, σ'>`로 평가되고, store를 `M`에서 `M_1`으로 변경하며, `e_2`가 `σ` 하에서 `v'`로 평가되고, store가 `M_1`에서 `M_2`로 변경되며, `a`가 `M_2`의 domain에 속하지 않으며, `e`가 `σ'[x↦a]`하에서 `v`로 평가되고, store가 `M_2[a↦v']`에서  `M_3`로 변경되면, `e_1 e_2`는 `σ`하에서  `v`로 평가되고, store `M`은 `M_3`로 변경된다.

    $$
    σ, M├e_1⇒\left\langle λx.e, σ' \right\rangle,M_1\ \ \ \ \  σ, M_1├e_2⇒v',M_2\ \ \ \ \ a \notin Domain(M_2)\ \ \ \ \ σ'[x↦a], M_2[a↦v']├e⇒v, M_3
    \over σ, M├e_1\ e_2⇒v,M_3
    $$

    - Subexpression의 평가는 BFAE와 동일하지만, 나머지 절차는 다르다.
    - Argument의 value를 environment가 아닌 store에 저장해야하며, 이를 위해 새로운 address가 필요하다.
    - Parameter명은 environment에서 address와 연결되며, address는 store에서 argument의 값과 연결된다.

  - Variable의 값을 변경하는 semantic 정의하기

    - Variable의 값을 변경하는 것은 BFAE에서 box의 값을 변경하는 것과 유사하다.
    - 그러나, BFAE에서는 변경될 box의 address를 찾기 위해 expression을 평가했어야 했지만, MFAE에서는 변경될 variable의 address를 environment에서 name을 사용하여 찾을 수 있다.
    - `x`가 `σ`의 domain이고, `σ`하에서 `e`가 `v`로 평가되고, store가 `M`에서 `M_1`으로 변경되면, `x:=e`는 `σ`하에서 `v`로 평가되고, store는 `M`에서 `M_1[σ(x)↦v]`로 변경된다.

    $$
    x \in Domain(σ)\ \ \ \ \ σ,M├e⇒v,M_1 
    \over σ,M├x:=e⇒v,M_1[σ(x)↦v]
    $$

  - 다른 semantic들은 BFAE의 것을 그대로 사용하면 된다.



- Interpreter 수정하기

  - MFAE의 syntax 정의하기
    - `Set(x: String, e: Expr)`는 `x:=e`를 표현한 것이다.

  ```scala
  sealed trait Expr
  ...
  case class Set(x: String, e: Expr) extends Expr
  ```

  - Address와 store의 type은 BFAE에 정의된 것과 같지만, environment의 type은 변경해야한다.

  ```scala
  type Addr = Int
  type Sto = Map[Addr, Value]
  ```

  - `interp` 함수 수정하기
    - BFAE와 마찬가지로, `interp` 함수는 expression, environment 그리고 store를 parameter로 받고, value와 store의 쌍을 반환한다.
    - `Id` case는 variable의 address를 찾은 후, address에 해당하는 value를 찾는다.
    - `App` case는 새로운 address를 계산하기 위해 BFAE와 같은 전략을 사용하며, function의 body는 확장된 environment와 store 하에서 평가된다.
    - `Set` case는 environment를 사용하여 variable의 address를 찾고, variable의 value를 변경하기 위해 store를 변경한다.

  ```scala
  def interp(e: Expr, env: Env, sto: Sto): (Value, Sto) =
      e match {
          ...
          case Id(x) => (sto(env(x)), sto)
          case App(f, a) =>
              val (CloV(x, b, fEnv), ls) = interp(f, env, sto)
              val (v, rs) = interp(a, env, ls)
              val addr = rs.keys.maxOption.getOrElse(0) + 1
              interp(b, fEnv + (x -> addr), rs + (addr -> v))
          case Set(x, e) =>
              val (v, s) = interp(e, env, sto)
              (v, s + (env(x) -> v))
  }
  ```



- Call-by-Reference

  - 초보 개발자들은 종종 swap function을 잘못 구현하곤한다.
    - 예를 들어 아래 C++ code를 작성할 때, `a`와 `b`가 swap 되어 `2 1`이 출력될 것을 기대하겠지만, `1 2`가 출력된다.

  ```c++
  void swap(int x, int y) {
      int tmp = x;
      x = y;
      y = tmp;
  }
  
  int a = 1, b = 2;
  swap(a, b)
  std::cout << a << " " << b << std::endl;
  ```

  - 위와 같은 실수가 발생하는 이유를 이번 장에서 배운 내용을 토대로 설명할 수 있다.
    - `swap`이 호출되면, 두 개의 새로운 address가 `x`와 `y`를 위해서 생성된다.
    - `a`와 `b`의 값은 복제되어 각 address에 저장된다.
    - `swap` function은 오직 `x`와 `y`의 address가 가리키는 값에만 영향을 미치며, `a`와 `b`의 address에는 절대 영향을 미치지 않는다.
  - CBV
    - Argument의 value는 복제되어 새로운 address에 저장된다는 것은 function application의 일반적인 semantic이다.
    - 이러한 semantic을 call-by-value(CBV)라 부른다.
    - 지금까지 사용해온 방식이다.
  - CBR
    - 사람들은 `swap`과 같은 함수를 보다 간편하게 구현하기 위해서 function application의 다른 semantic을 찾았다.
    - 새롭게 찾아낸 semantic을 call-by-reference(CBR)이라 부른다.
    - CBR에서 variable이 argument로 사용될 때, function call은 reference(즉, address)를 전달한다.



- CBR, CBV 적용하기

  - Function application의 semantic에 CBR을 적용하기

    - Argument가 variable인 경우로 한정된다.
    - `e`가 `σ`하에서 `<λx'.e', σ'>`로 평가되고, store를 `M`에서 `M_1`으로 변경하며,  `x`가 `σ`의 domain에 속하고,  `e'`가 `σ'[x'↦σ(x)]`하에서 `v`로 평가되며, store가 `M_1`에서  `M_2`로 변경되면, `e x`는 `σ`하에서  `v`로 평가되고, store `M`은 `M_2`로 변경된다.

    $$
    σ, M├e⇒\left\langle λx'.e', σ' \right\rangle,M_1\ \ \ \ \  a \in Domain(σ)\ \ \ \ \ σ'[x'↦σ(x)], M_1⇒v, M_2
    \over σ, M├e\ x⇒v,M_2
    $$

    - Value를 얻기 위해 argument를 평가하지 않고, 단순히 variable의 address를 사용한다.
    - 그러면, function의 parameter는 argument와 정확히 같은 address를 갖고 있게 된다.
    - Function body에서 발생하는 parameter의 모든 변경사항은 function 밖의 variable에도 영향을 주게 된다.
    - 이처럼 parameter와 argument가 같은 address를 공유하는 상황을 parameter가 argument의 alias라고 표현한다.

  - Function application의 semantic에 CBV를 적용하기

    - 위에서 기존의 MFAE의 semantic에 CBR을 적용했지만, argument가 variable이 아니면 사용이 불가능하다.
    - Variable이 아닌 argument의 address를 가져올 수는 없기 때문이다.
    - 이러한 경우에, CBV semantic으로 돌아가야한다.
    - `e_1`이 `σ`하에서 `<λx.e, σ'>`로 평가되고, `e_2`가 identifier가 아니며, store를 `M`에서 `M_1`으로 변경하며, `e_2`가 `σ` 하에서 `v'`로 평가되고, store가 `M_1`에서 `M_2`로 변경되며, `a`가 `M_2`의 domain에 속하지 않으며, `e`가 `σ'[x↦a]`하에서 `v`로 평가되고, store가 `M_2[a↦v']`에서  `M_3`로 변경되면, `e_1 e_2`는 `σ`하에서  `v`로 평가되고, store `M`은 `M_3`로 변경된다.

    $$
    σ, M├e_1⇒\left\langle λx.e, σ' \right\rangle,M_1\ \ \ \ \  e_2 \notin Id\\ \ \ \ \ σ, M_1├e_2⇒v',M_2\ \ \ \ \ a \notin Domain(M_2)\ \ \ \ \ σ'[x↦a], M_2[a↦v']├e⇒v, M_3
    \over σ, M├e_1\ e_2⇒v,M_3
    $$

    - MFAE의 기존 semantic에 `e_2 ∉ Id`가 추가된 것이다(즉 argument가 variable이 아니라는 전제가 추가된 것이다).

  - CBV를 적용하면 Interpreter도 아래와 같이 변경시켜야한다.

    - Function application의 argument expression에 pattern matching을 사용한다.
    - 만약 argument가 identifier라면(즉, variable이면), CBR semantic이 사용될 수 있고, 아니라면, CBV semantic이 적용된다.

  ```scala
  case App(f, a) =>
      val (CloV(x, b, fEnv), ls) = interp(f, env, sto)
      a match {
          case Id(y) =>
          	interp(b, fEnv + (x -> env(y)), ls)
          case _ =>
              val (v, rs) = interp(a, env, ls)
              val addr = rs.keys.maxOption.getOrElse(0) + 1
              interp(b, fEnv + (x -> addr), rs + (addr -> v))
  }
  ```











