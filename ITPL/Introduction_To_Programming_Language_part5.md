# Lazy Evaluation

- Lazy evaluation

  - Lazy evaluation이란 expression의 평가를 해당 expression의 결과가 필요해질 때까지 미루는 것이다.
  - Eager evaluation
    - Lazy evaluation과 반대되는 개념이다.
    - Expression의 결과가 향후의 계산에 필요한지도 모르는채로 expression을 평가하는 것이다.
  - Lazy evaluation에는 programming language에 적용될 수 있는 몇 가지 특징이 있다.
    - 예를 들어 function application을 위한 argument들은 lazy하게 평가될 수 있다.
    - Function application시의 각 argument들은 function body가 시작되기 전이 아니라, function body에서 사용될 때 평가된다.
    - 또 다른 예는 변수 선언이다.
    - Variable의 초기화는 variable이 정의될 때가 아닌, variable이 처음 쓰일 때 발생할 수 있다.

  - 여기서는 function application의 argument의 lazy evaluation만을 고려할 것이다.
    - 사실, 이전 장에서 local variable이 function parameter의 syntactic sugar로 간주될 수 있다고 했으므로, function application의 argument의 lazy evaluation을 살펴보면 variable definition에서의 lazy evaluation도 설명될 것이다.



- CBV, CBN, CBR과 eager, lazy language

  - 이전장까지 정의했던 언어는 eager language였다.
    - 또한 function application의 semantic을 정의할 때 CBV를 사용했다.
    - CBV는 eager evaluation과 같은 것으로 간주될 수 있다.
    - CBV는 모든 argument가 value로 넘겨진다는 것을 의미한다.
    - 따라서 argument의 value는 오직 argument expression을 평가함으로써만 얻어질 수 있다.
    - 이는 모든 argument가, 그것이 function body의 평가에 사용되는지와 무관하게, function body의 평가 이전에 평가된다는 것을 암시한다.
    - 그러므로, CBV semantic은 eager evaluation semantic과 같다고 할 수 있다.
  - Call-by-name(CBN) semantic은 lazy evaluation의 한 형태이다.
    - CBN semantic에서 각 argument들은 그것들의 name으로 넘겨진다.
    - 즉 expression이 가리키는 값이 아니라 expression 그 자체로 넘겨진다.
    - Expression으로 넘겨지기 때문에, argument의 value를 얻기위해 expression을 평가하지 않아도 된다.
    - Expression은 function body에서 value가 필요한 경우에 평가된다.
    - CBN은 argument를 expression으로 넘김으로서 그것의 계산을  늦춘다.
    - 따라서 CBN은 lazy evaluation으로 간주될 수 있다.

  ```python
  def foo():
      print("foo")
      return "foo"
  
  def call_by_value(condition, value):
      if condition:
          return value
  
  # function이라는 parameter는 해당 값이 필요하지 않으면 평가되지 않는다.
  def call_by_name(condition, function):
      if condition:
          return function()
  
  call_by_value(False, foo())	# argument로 function의 실행 결과 값을 넘긴다.
  call_by_name(False, foo)	# argument로 function을 넘긴다.
  ```

  - Call-by-reference(CBR)의 경우
    - CBR의 경우에는 earger language인지 lazy language인지 구분하는 것과 무관하다.
    - CBR은 argument가 address가 알려진 variable인 것을 의미하는데, 이 경우, 평가할 것 자체가 없다.
    - CBR과 CBV는 address를 넘기느냐, address가 가리키는 값을 넘기느냐의 문제인데 반해, eagerness와 laziness는 argument를 언제 평가할지에 관한 문제이다.
    - CBR은 argument를 평가 하든 하지 않든 사용될 수 있다.



- 이번 장에서 FAE의 lazy version인 LFAE를 정의해 볼 것이다.
  - LFAE는 CBN semantic을 채택한다.
  - 또한 lazy evaluation의 또 다른 형태이자 CBN의 최적화 version인 call-by-need에 대해서도 알아볼 것이다.
    - 어떤 사람들은 lazy evaluation을 call-by-need를 가리키기 위해 사용한다.
    - 그러한 관점에서 보면, CBN은 lazy evaluation이 아니다.
    - 그러나, 여기서는 CBN과 call-by-name 모두 lazy evalutaion에 속한다고 간주할 것이다.



- 본격적으로 CBN semantic과 LFAE를 다루기 전에, lazy evaluation이 실제로 어떤 유용함이 있는지 살펴볼 것이다.

  - 우리는 lazy-evaluation을 소수의 실제 language들에서 찾아볼 수 있다.
    - Haskell의 경우 모든 계산을 기본적으로 lazy하게 처리하는 것으로 유명하다.
    - 만면에 Scala는 eager language지만 programmer가 선택적으로 lazy evaluation을 적용할 수 있도록 허용한다.
  - Eager evaluation을 사용할 경우의 문제점
    - `square` function은 integer를 argument로 받고, 그것의 제곱을 반환하는데, `Thread.sleep(5000)`으로 인해 항상 최소 5초 이상이 걸리게 된다.
    - `foo`의 경우 `b`가 false면 `square(10)`는 필요 없어지게 된다.
    - 그러나 Scala는 기본적으로 eager evaluation을 사용하기에, `b`와 무관하게 항상 `square(10)`가 실행되고 5초를 소비하게 된다.
    - 만일 우리가 `b`가 true일 경우에만 `square(10)`를 실행하도록 변경한다면, 많은 경우에 program의 실행 시간을 줄일 수 있다.

  ```scala
  def square(x: Int): Int = {
  	Thread.sleep(5000) // 시간이 오래 걸리는 연산을 대체
      x * x
  }
  
  def foo(x: Int, b: Boolean): Int =
  	if (b) x else 0
  
  // file에는 a.txt라는 file이 있으면 true, 없으면 false가 담기게 된다.
  val file = new java.io.File("a.txt")
  foo(square(10), file.exists)
  ```

  - Lazy evaluation 적용하기
    - Scala에서는 argument에 `=>`를 추가하여 해당 argument에 lazy evaluation을 적용할 수 있다.
    - 더 정확히는 CBN semantic을 사용하게 할 수 있다.

  ```scala
  def foo(x: => Int, b: Boolean): Int =
  	if (b) x else 0
  ```



- Semantic 정의하기

  >  LFAE의 syntax는 FAE와 동일하므로 따로 정의하지 않는다.

  - 변경이 필요하지 않은 것들

    - Environment의 정의는 FAE와 동일하다(또한 `σ ├ e ⇒ v`는 오직 `e`가 `σ`하에서 `v`로 평가될 때만 참이다).
    - Rule Num, Rule Fun, Rule ID 등도 lazy evaluation의 영향을 받지 않으므로, 수정할 필요가 없다.

  - 확실히 수정이 필요한 것은 function application의 semantic이다.

    - Function application이 lazy language와 eager language를 비교했을 때 가장 두드러진 차이를 보이기 때문이다.

  - Value의 semantic 수정하기

    - CBV semantic에서 argument의 value를 environment에 저장하고, function body를 평가하는데 environment를 사용했었다.
    - CBN에서도 마찬가지로 environment에 argument를 저장할 것이지만, argument가 expression으로 전달되고, argument는 value가 아니다.
    - 따라서 environment에 expression을 넣을 수 있는 방법이 필요하다.
    - 가장 간단한 방법은 Value의 semantic을 아래와 같이 수정하는 것이다(기존 Value의 semantic은 생략한다).

    $$
    v:= \cdots\ |\ (e, σ)
    $$

    - `(e, σ)`는 value로서의 expression을 나타내며, 이를 expression-value라 부를 것이다.
    - 이는 `σ`하에서 `e`의 계산이 지연됐다는 것을 의미한다.
    - Environment(`σ`)를 expression과 함께 묶은 이유는 expression에 environment에 값이 저장된 free identifier가 포함됐을 수 있기 때문이다.
    - 이는 closure의 개념과 비슷하다.
    - Expression-value의 형태(`(e, σ)`)와 closure의 형태(`<λx.e, σ>`)는 parameter의 이름이 없다는 것만 빼면 유사한데, 이는 우연이 아니다.
    - Expression-value와 closure 모두 지연된 계산을 가리킨다.
    - `(e, σ)`에서 `e`의 평가는 argument의 값이 필요해질 때까지 연기된다.
    - 또한 `<λx.e, σ>`에서 `e`의 평가 또한 closure가 value에 적용될 때 까지 연기된다.

  - Expression-value의 추가로, evaluation의 또 다른 형식을 정의해야한다.

    - 이를 strict evaluation이라 부를 것이다.
    - Strict evaluation의 목적은 expression-value를 integer나 closure 같은 normal value가 되도록 강제하는 것이다.
    - Strict evaluation은 expression-value의 능력이 제한되어야하기에 필요하다.
    - Expression-value는 argument가 될 수도 있고, normal value처럼 environment에 저장될 수도 있지만, 수학적 expression의 피연산자가 되거나 function이 되어 호출 될 수는 없다.
    - 따라서 strict evaluation을 통해 expression-value를 value로 변경하는 작업이 필요하다.

  - Strict evaluation은 V와 V 사이의 이항관계로 정의된다.

    -  Strict evaluation을 표현하기 위해 `⇓`를 사용할 것이다.

    $$
    ⇓\subseteq V×V
    $$

    - `v_1 ⇓ v_2`는 오직 `v_1`이 strict하게 `v_2`로 평가될 경우에만 참이다.
    - 여기서 `v_1`은 어떤 값이든 될 수 있지만, `v_2`는 expression-value는 될 수 없고 반드시 normal value여야한다.
    - 그 이유는 분명한데, strict evaluation의 목적이 expression-value를 normal value로 변경하는 것이기 때문이다.

  - Normal value는 이미 normal value이기에 strict하게 평가해도 그 자체로 평가된다.

    - Rule Strict-Num: n은 strict하게 n으로 평가된다.

    $$
    n⇓n
    $$

    - Rule Strict-Clo: `<λx.e, σ>`은 strict하게`<λx.e, σ>`로 평가된다.

    $$
    \left\langle λx.e, σ \right\rangle⇓\left\langle λx.e, σ \right\rangle
    $$

  - Rule Strict-Expr

    - `e`가 `σ`하에서 `v_1`으로 평가되고, `v_1`이 `σ`하에서 `v_2`로 strict하게 평가되면, `(e,σ)`는 `v_2`로 strict하게 평가된다.

    $$
    σ├e⇒v_1\ \ \ \ \ v_1⇓v_2\over (e, σ)⇓v_2
    $$

    - `e`의 결과는 또 다시 expression-value가 될 수 있다.
    - 그러므로, normal value를 얻를 때 까지 strict하게 평가를 반복해야한다.

  - Rule App

    - 만약 `e_1`이 `σ`하에서 `v_1`으로 평가되고, `v_1`이 `<λx.e, σ'>`로 strictly evaluate되며, e가 `σ'[x↦(e_2,σ)]`하에서 `v`로 평가되면, `e_1 e_2`는 `σ`하에서 `v`로 평가된다.

    $$
    σ├e_1⇒v_1\ \ \ \ \ v_1⇓\left\langle λx.e, σ' \right\rangle\ \ \ \ \ σ'[x↦(e_2,σ)]├e⇒v\over σ├e_1\ e_2⇒v
    $$

    - 먼저 `e_1`이 `v_1`으로 평가된다.
    - ` v_1`은 아마 expression-value일 것이며, 우리는 expression-value가 아닌 closure가 필요하다.
    - 그러므로, closure를 얻기 위해 `v_1`을 strictly evaluate한다.
    - 반면에, CBN semantic에서 argument는 function body가 평가되기 전까지는 평가되면 안되므로`e_2`를 평가하는 대신 `e_2`와 `σ`로 expression-value를 만들고, 이를 environment에 넣는다.

  - Rule Add

    - `e_1`이 `σ`하에서 `v_1`으로 평가되고, `v_1`이 `n1_1`으로 strictly evaluate되며, `e_2`가 `σ`하에서 `v_2`로 평가되고, `v_2`가 `n_2`로 strictly evaluate 되면, `e_1+e_2`는 `σ`하에서 `n_1+n_2`로 평가된다.

    $$
    σ├e_1⇒v_1\ \ \ \ \ v_1⇓n_1\ \ \ \ \ \ σ├e_2⇒v_2\ \ \ \ v_2⇓n_2\over σ├e_1+e_2⇒n_1+n_2
    $$

  - Rule Sub

    - `e_1`이 `σ`하에서 `v_1`으로 평가되고, `v_1`이 `n1_1`으로 strictly evaluate되며, `e_2`가 `σ`하에서 `v_2`로 평가되고, `v_2`가 `n_2`로 strictly evaluate 되면, `e_1-e_2`는 `σ`하에서 `n_1-n_2`로 평가된다.

    $$
    σ├e_1⇒v_1\ \ \ \ \ v_1⇓n_1\ \ \ \ \ \ σ├e_2⇒v_2\ \ \ \ v_2⇓n_2\over σ├e_1-e_2⇒n_1-n_2
    $$

  - 문제점

    - 지금까지 정의한 semantic들은 CBN을 적용하긴 했으나 실제사용하는 관점에서는 한 가지 흠이 있다.
    - `<λx.x>(1+1)`의 결과는 `(1+1, ∅)`이지 2가 아니다.
    - 대부분의 programmer는 2가 결과로 나오기를 바랄 것이다.
    - 따라서 마지막으로 전체 evaluation이 끝날 때, strict evaluation을 한 번 더 적용해야한다.
    - 즉, program `e`의 결과는 `∅├e⇒v'`이고, `v'⇓v''`일 때 `v`이다.
    - 주의할 점은 이는 program의 모든 expression에 strict evaluation을 적용하는 것과는 다르다는 점이다.
    - Strict evaluation은 오직 전체 exrpression(즉, program)의 결과에만 적용된다.

  - CBV semantic으로 expression을 평가한 결과로 value가 나왔다면, CBN semanic도 같은 value를 산출할 것이다.

    - 이는 lambda calculus(람다 대수)의 standardization theorem(표준 정리)의 따름 정리(corollary)이다.
    - 표준화 정리는 람다 대수의 식이 어떤 순서로 계산하여 값이 나온다면, 정규 순서(normal order)로 계산하였을 때 반드시 그 값이 나옴을 의미한다.
    - 단, 이는 오직 side effect가 없는 language들에서만 참이다.
    - Side effect가 있는 경우, expression의 결과는 evaluation 순서에 따라 달라진다.
    - 예를 들어 argument가 box의 값을 변경시키는 expression이고, function body에서 argument를 사용하지 않고 box의 값을 읽는다면, 이 program은 CBV와 CBN에서 다르게 동작할 것이다.
    - CBV의 경우, argument가 사용되지 않아도 일단 평가하므로, box의 값이 변경되고, 변경된 box의 값이 읽히게 된다.
    - 반면 CBN의 경우, argument가 사용되지 않으면 평가되지 않으므로, box의 값이 변경되지 않고, 변경되지 않은 box의 값이 읽히게 된다.

  - CBV semnatic의 결과는 CBN semantic의 결과와 같지만, CBVNsemantic의 결과가 CBV semantic의 결과와 항상 같은 것은 아니다.

    - 즉 오직 CBN에서만 결과를 산출하는 expression이 있다.
    - 예를 들어, argument로 종료되지 않는 expression을 받는 function application이 일어났다고 가정해보자.
    - 만약 해당 argument를 사용하지 않으면 0을 반환한다고 했을 때, CBN에서는 해당 argument가 사용되지 않으면 0을 반환하겠지만, CBV는 argument를 바로 평가하므로 실제 사용 여부와 관계 없이 종료되지 않는 expression이 계속 실행되게 된다.



- Interpreter 수정하기

  - Expression-value를 표현하기 위한 `Value`의 또 다른 변형을 추가해야한다.

  ```scala
  sealed trait Value
  ...
  case class ExprV(e: Expr, env: Env) extends Value
  ```

  - Strict evaluation을 위한 function을 추가한다.

  ```scala
  def strict(v: Value): Value = v match {
      case ExprV(e, env) => strict(interp(e, env))
      case _ => v
  }
  ```

  - `interp` function을 아래와 같이 수정한다.

  ```scala
  def interp(e: Expr, env: Env): Value = e match {
      ...
      case Add(l, r) =>
          val NumV(n) = strict(interp(l, env))
          val NumV(m) = strict(interp(r, env))
          NumV(n + m)
      case Sub(l, r) =>
          val NumV(n) = strict(interp(l, env))
          val NumV(m) = strict(interp(r, env))
          NumV(n - m)
      case App(f, a) =>
          val CloV(x, b, fEnv) = strict(interp(f, env))
          interp(b, fEnv + (x -> ExprV(a, env)))
  }
  ```



- Call-by-Need

  - 위에서 구현한 방식은 parameter가 function body에서 한 번 이하로 나타날 때만 효율적이다.
    - 그러나, parameter를 두 번 이상 사용해야할 경우 불필요한 계산이 발생한다.
    - 아래 예시에서 `x`는 function `bar`의 body에 두 번 나타나므로, 만약 `a.txt`가 있으면, `square(10)`은 두 번 계산된다.
    - 따라서 function call의 횟수를 줄이는 것이 바람직하다.
    - 만약 우리가 CBV를 사용한다면, `square(10)`을 한 번만 평가하는 것이 가능하다. 그러나 file이 있는지 여부와 무관하게 무조건 `square(10)`을 계산하므로, CBV로 돌아가는 것은 좋은 선택이 아니다.

  ```scala
  def square(x: Int): Int = {
      Thread.sleep(5000) // models some expensive computation
      x * x
  }
  def bar(x: => Int, b: Boolean): Int =
  	if (b) x + x else 0
  
  val file = new java.io.File("a.txt")
  bar(square(10), file.exists)
  ```

  - 위와 같은 문제를 해결하는 방법은 argument의 value를 저장해두고, 재사용하는 것이다.

    - 그러나 programmer 입장에서 이러한 최적화 logic을 구현하는 것은 지루한 일일 수 있따.
    - 대신, programming language가 이러한 최적화를 제공할 수도 있다.
    - 각 argument가 그 값이 필요할 때 평가되는 최적화를 call-by-name이라 부른다.

    - 만약 값이 필요하면 한 번 평가되고, 필요하지 않다면 평가되지 않는다.

  - Call-by-name과 CBN

    - 순수 functional language에서 Call-by-name의 semantic은 CBN의 semantic과 다르지 않다.
    - 둘 모두 program의 동작이 완전히 동일하다.
    - Call-by-name은 interpreter 혹은 compiler의 최적화 전략일 뿐이다.
    - 반면에 side effect가 있는 language에서 둘은 semnatic에서 차이를 보인다.
    - 특정 expression의 연산 횟수는 결과에 영향을 줄 수 있다.
    - 예를 들어 box의 value를 1 증가시키는 argument가 있다고 가정해보자.
    - 해당 argument는 function body에서 두 번 사용된다.
    - 그럼, CBN에서는 box의 값이 2 증가되겠지만, call-by-need에서는 1 증가될 것이다.

  - Lazy evaluation을 사용하는 순수 functional language는 일반적으로 call-by-need를 채택한다.

    - 순수 functional language에서는 semnatic의 변경 없이 최적화가 가능하기 때문이다.
    - 그러나 순수 functional language가 아닌 language들은 call-by-need를 최적화로 간주할 수  없으며, 종종 programmer에게 선택하게 해준다.
    - 예를 들어 Scala는 CBN을 parameter에 사용하고, call-by-name을 lazy evaluation을 위해 사용한다.



- LFAE에 call-by-need 적용하기

  - LFAE에는 side effcect가 없기 때문에, call-by-need를 적용하는 것이 가능하다.
    - Interpreter를 최적화하는 방식으로 적용할 것이다.
    - 따라서, semantic은 수정할 필요가 없다.
  - Expression-value의 strict value를 저장하기위한 class를 정의한다.
    - Field는 mutable하게 선언한다.
    - 초기에 expression의 value는 unknown이고, `v`는 None이다.
    - Value가 처음 계산될 때, value는 `v`에 저장된다.
    - 어떤 `a`에 대해서 `v`가 `Some(a)`와 같다는 사실은 expression의 value가 `a`라는 것을 의미한다.
    - 다음에 value가 다시 필요해졌을때, `Some()`의 argument가 `a`라면 `Some(a)`를 다시 계산할 필요 없이 `v`의 값을 사용하면 된다.

  ```scala
  case class ExprV(
  	e: Expr, env: Env, var v: Option[Value]
  ) extends Value
  ```

  - `strict` function은 아래와 같이 변경되어야 한다.
    - 먼저 cache된 value가 있는지 체크한 후, cache된 value가 있으면 cache 된 value를 반환한다.
    - 아니면 `e`는 이전처럼 `env`하에서 평가된다.
    - 추가적으로, v에 value를 저장한다.

  ```scala
  def strict(v: Value): Value = v match {
      // cache된 값(ExprV 의 instance)이 있으면 cache된 값을 반환.
      case ExprV(_, _, Some(cache)) => cache
      // cache된 값이 없으면, 
      case ev @ ExprV(e, env, None) =>
      	// env하에서 e를 평가하고
          val cache = strict(interp(e, env))
      	// v에 value를 저장한다.
          ev.v = Some(cache)
          cache
      case _ => v
  }
  ```

  - `interp` function도 수정이 필요하다.
    - `App` case만 변경하면 된다.
    - `App` case에서 새로운 `ExprV`의 instance가 생성될 때, `v` field를 초기화하기위한 추가적인 argument를 넘겨야 한다.
    - 우리는 `a`의 value를 모르기 때문에, `v`의 초기값은 None이된다.

  ```scala
  case App(f, a) =>
      val CloV(x, b, fEnv) = strict(interp(f, env))
      interp(b, fEnv + (x -> ExprV(a, env, None)))
  ```

