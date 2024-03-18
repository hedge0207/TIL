# 코드 가독성

> https://engineering.linecorp.com/ko/blog/code-readability-vol1

- 코드의 가독성
  - 기능 구현은 누구나 별다른 노력 없이 할 수 있지만, 가독성이 높은 코드를 작성하는 것은 특별한 노력이 필요하다.
  - 코드의 가독성이 중요한 이유
    - 코드의 가독성이 높아질수록 함께 작업하는 사람들의 생산성이 높아지게 된다.
    - 개발자는 코드를 작성하는 것 보다 다른 사람이 작성한 코드를 읽는 데 훨씬 많은 시간을 사용한다.
    - 따라서 가독성이 높은 코드를 작성할 수록 코드를 읽고 이해하는 데 사용되는 시간이 줄어들어 함께 작업하는 사람들의 생산성이 높아질 수 있다.



- 코드의 가독성을 높이는 5가지 원칙
  - 여러 프로그래밍 원칙들 중에서 아래의 5가지 원칙은 과도하게 적용해도 부작용이 별로 없는 원칙들이다.
  - Clean code whenever you have touched it.
    - Robert Baden-Powell이 말한 "Try to leave this world a little better than you found it" 라는 보이스카웃의 원칙을 Robert C. Martin이 개발에 맞게 변형한 것이다.
    - Code에 손을 댈 때 마다 더 깔끔하게 만들어야 함은 물론, 지저분한 코드를 더 지저분하게 만들지 말라는 의미도 내포되어 있다.
  - YAGNI(You Aren't Gonna Need It)
    - 오직 정말로 필요할 때만 구현해야지, 미래에 필요할 것이라 생각하여 미리 구현하면 안 된다는 XP의 원칙이다.
    - 사용하지 않는 코드의 예로는 사용하지 않는 utility function, 구현이 하나 이하인 추상화 layer, 고정 값 밖에 주어지지 않는 가인수(dummy argument) 등이 있다.
    - 다만 이 원칙은 코드의 변경이 쉽다는 것을 전제로 하고 있다.
    - 따라서 외부의 사용자를 위한 public library의 경우에는 예외로, 이런 library들 변경이 어려우므로 앞으로 어떻게 사용될지 미리 고려해서 설계하고 구현해야한다.
  - KISS(Keep It Simple Stupid)
    - 본래 장비를 정비하기 쉽도록 설계를 단순화해야 한다는 의미이다.
    - 이를 소프트웨어 개발에 적용하면 '기능과 구현을 단순화한다' 혹은 '구현 기법을 단순화 한다'는 의미가 될 것이다.
    - 프로그래밍 원칙과 패러다임, 설계 기법 등은 코드의 가독성과 견고함을 높이는 수단이어야지, 그 자체가 목적이 되면 안 된다.
  - Single responsibility principle
    - SOLID라 불리는 객체지향의 원칙 중 하나로 하나의 클래스는 딱 한 가지 이유로 변경되어야 한다는 의미이다.
    - 클래스의 책임과 관심의 범위는 하나로 좁혀야한다.
  - Premature optimization is the root of all evil
    - 조기에 최적화를 해선 안 된다는 말은, 최적화의 효과가 작을 때는 최적화를 해선 안 된다는 의미이다.
    - 다만 코드의 가독성이 좋아지는 최적화는 예외이다.



- 이름 붙이기
  - 좋은 이름
    - 좋은 이름은 이름이 나타내는 내용, 문법, 단어가 모두 잘 맞는 이름이다.
    - 정확하고, 정보를 제공하며, 분명한 이름이 좋은 이름이다.
    - 이름을 붙일 때 아래와 같은 규칙을 지켜야 한다.
  - 정확한 문법을 사용하라.
    - 정확하지 않은 문법은 역할을 헷갈리게 만들 수 있다.
    - 명사를 사용할 경우 필수적인 단어를 맨 끝에 위치시켜라.
    - 즉 MessageEventHandler와 같이 붙여야지 HandlerForMessageEvent와 같이 사용해선 안 된다.
    - 단, property function은 예외로, `indexOf()`, `maxValueIn()`과 같이 사용해도 된다.
    - 동사를 사용할 경우 맨 앞에 위치시켜라.
  - Who, when, why 등 보다 what에 집중하여 붙여라.
    - Type이나 value 혹은 무엇을 하는 procdure인지 알 수 있게 붙여야 한다.
    - 예를 들어 message를 받아올 때 호출된다고 하여 `onMessageReceived(message)`와 같이 when에 집중해서 붙여선 안되며, 받아온 message를 가지고 무엇(what)을 하는지를 알 수 있도록 붙여야한다.
    - 이름에서 what을 읽을 수 없을 경우 모호해 보이게 된다.
    - 예를 들어 `shouldShowDialogOnError`와 `isCalledFromMainActivity`라는 두 개의 boolean 변수가 있을 때, 전자가 후자에 값이 true일 때 어떤 일이 발생하는지를 더 잘 나타낸다.
    - 단, abstract callback interface에서는 사용해야 할 수도 있다(e.g. onClicked).
    - 이들은 선언할 때 무슨 일이 일어날지가 아직 정해지지 않았기 때문이다.
  - 모호하지 않은 단어들을 사용해라.
    - 예를 들어 `sizeLimit`은 최대치의 제한인지 최소치의 제한인지를 알 수 없으며, size가 길이인지, 높이인지, character의 개수인지도 알 수 없다.
    - 따라서 `maxHeight`와 같이 보다 분명하게 작성해야한다.
    - `flag`, `check`등이 대표적으로 이들은 더욱 분명한 단어로 변경해서 작성해야한다.
  - 혼란을 일으킬 수 있는 약어는 피해라.
    - 심지어 string을 나타내기 위해 흔히 쓰이는 `str`이라는 약어 조차도 보는 사람에 따라서 string, stream, structure 등 무수히 많은 단어를 떠올릴 수 있다.
    - 특히 자신만 이해할 수 있는 약어는 절대 사용해선 안된다.
    - 단 URL, IO와 같이 널리 사용되는 약어는 예외이다.
  - 단위를 suffix로 붙여라.
    - 그냥 `timeout`이라고 해선 시간의 단위를 알 수 없으므로 `timeout_ms`등과 같이 단위를 붙여야한다.
  - 부정 보단 긍정 표현을 사용해라.
    - not, no, non 등을 사용해선 안 된다(e.g. isNotEnabled).
    - `isNotEnabled`보다 `isDisabled`가 낫고, 이보다는 `isEnabled`가 더 낫다.



- 주석 사용하기

  - 주석을 다는 이유
    - 의도를 전달하기 위해서(코드로 표현한 의도를 요약해서 전달하고, 코드를 작성한 이유를 설명하기 위해서).
    - 실수를 방지하기 위해서(주의해야 할 사항들을 미리 알려줘 실수를 방지하게 한다).
    - Refactoring을 위해서(따라서 만약 코드가 충분히 깔끔하다면 이를 목적으로 하는 주석인 필요 없을 수 있다).

  - 주석의 종류

    - documentation: type/value/procedure에 대한 구조화된 주석.
    - Inline comment: code block에 대한 정보를 제공하기 위한 주석

  - 문서화 주석

    - 유형, 값, 절차 등의 선언어이나 정의에 다는 주석으로, 일정한 형식에 맞춰 작성한 주석을 의미한다.
    - 문서화 주석을 통해 상세한 코드 참조나 대상을 확인할 필요 없이 사양을 이해할 수 있다.
    - 짧은 요약은 반드시 들어가야 하며 필요에 따라 상세 설명을 추가할 수 있다.

  - 문서화 주석의 내용

    - 요약은 한 문장/문단으로 끝내야 하며, 무엇인지 혹은 무엇을 하는 것인지를 설명해야한다.
    - 일반적으로 코드에서 가장 중요한 block을 찾은 후 해당 block이 무엇을 하는지 설명하면 짧은 요약이 된다.
    - 요약 작성시 type이나 value를 요약할 때는 명사구로 시작해야 한다(e.g. A generic ordered collection of elements).
    - Preocedure를 요약할 때는 3인칭 단수 동사로 시작해야한다(e.g. Adds a new element at the end of the array).

    - 만약 specification과 용도, 반환하는 값, 한계, error가 발생하는 상황, 예시 등이 필요할 경우 상세 설명에 작성하면 된다.

  - 문서화 주석을 작성할 때의 anti-pattern들.

    - 자동으로 생성된 주석을 그대로 사용하는 것
    - 함수의 이름을 풀어서 설명한 것
    - 코드의 동작을 요약하는 것이 아니라 전부 설명하는 것
    - Private member를 언급하는 것
    - 요약을 작성하지 않는 것
    - 호출자를 언급하는 것

  - Inline 주석에는 아래와 같은 내용을 작성한다.

    - 읽는 사람에게 도움을 줄 수 있는 것이면 어떤 것이든 작성하면 된다.
    - 반드시 요약을 작성할 필요는 없다(code가 거대해 빠르게 파악하기 힘들 경우에 작성하면 된다).
    - 혹은 규모가 큰 코드를 주석을 통해 여러 개의 덩어리로 구분하기 위해 사용하기도 한다.



- 상태(state)와 절차(procedure)

  - 상태가 지나치게 많이 사용된 코드는 읽기가 힘들어진다.

    - 상태가 적게 사용될 수록 코드가 읽기 쉬워지는 것은 사실이지만, 그렇다고 무리하게 상태를 줄여서는 안된다.
    - 따라서 잘못된 상태를 줄이고 상태 변환을 단순화하는 데 집중해야한다.

  - 직교(orthogonal)와 비직교(non-orthogonal)

    - 두 개의 변수가 있다고 가정할 때, 한쪽의 변경이 다른 한쪽 값의 영향을 받지 않으면 두 변수의 관계를 직교라 한다.
    - 반대로 어느 한쪽의 변경이 다른 한쪽의 영향을 받으면 비직교라 한다.

    - 비직교 관계를 없애면 값이 잘못 조합되는 것을 줄일 수 있다.

  ```python
  # 예를 들어 아래에서 name이 바뀌면 welcome_message도 변경되어야 하므로 두 변수는 비직교 관계이다.
  name = "John"
  welcome_message = "Hello John"
  ```

  - 상태 변환이 가져오는 혼란을 줄이는 방법.
    - 가능하면 immutable한 property들을 사용해라.
    - 멱등성을 준수하여 동일한 함수를 여러 번 실행하더라도 결과가 달라지지 않도록해라.
    - 단, 최초 실행시에도 값이 변경되지 않는다면 그것이 멱등성을 준수한다고 할 수 없다.
    - Acyclic state를 유지해라
    - 상태에 순환이 있을 경우 코드를 이해하기가 힘들어질 수 있다.
    - 그러나 cycle을 무리하게 없앨 경우 model이 지나치게 복잡해질 수 있으므로 적절한 타협점을 찾아야한다.

  ```python
  # 멱등성 예시
  # 예를 들어 아래와 같은 code의 경우 chage_status method를 호출할 때 마다 값이 변경된다.
  closable = Closable()		# 초기에 open 상태
  closable.chage_status()		# close 상태로 변경
  closable.chage_status()		# open 상태로 변경
  
  # 반면에 아래와 같이 멱등성을 준수하는 method의 경우 method를 아무리 호출해도 값이 변경되지 않는다.
  closable = Closable()		# 초기에 open 상태
  closable.close()			# close 상태로 변경
  closable.close()			# 여전히 close 상태
  ```

  - 절차는 아래와 같은 것들을 의미한다.
    - Main routine, sub routine
    - function
    - method
    - computed property
    - ...
  - 절차의 책임과 흐름을 명확히 해야 가독성을 높일 수 있다.
    - 만일 절차를 한 문장/문단으로 요약하기 힘들다면 절차를 나눠야한다.
    - 좋은 절차는 절차의 이름에 부합하고, documentation을 작성하기 쉬우며, 적은 수의 error case와 limitation만을 가져야한다.
  - Command와 query를 구분할 경우 절차의 책임을 명확히 하는데 도움이 될 수 있다.
    - Command는 요청을 받은 쪽이나 parameter를 변경시키는 procedure를 의미한다.
    - Query는 변경 없이 값을 반환하는 procedure를 의미한다.
    - 단, 무작정 분할할 경우 오히려 불필요한 state들이 추가될 수 있으므로 주의해야한다.
    - 예를 들어 유저를 생성하고, 성공 여부를 반환하는 함수가 있었다고 가정해보자.
    - 이 때 command와 query를 분리하고자 `latest_operation_result`라는 새로운 state를 만드는 것은 오히려 버그의 위험성만 높이므로 이럴 경우 오히려 기존 code가 더 낫다고 볼 수 있다.

  ```python
  # 기존
  class UserDataStore:
  	def save_user(user_Data) -> bool:
          ...
  
  # 분리
  class UserDataStore:
      def __init__(self):
          latest_operation_result = NO_OPERATION
   	
      # command
  	def save_user(user_Data):
         	try:
              latest_operation_result = True
          except:
              latest_operation_result = False
      
      # query
      def was_latest_operation_successful:
          return latest_operation_result
  ```

  - 절차의 흐름을 명확하게 하기 위해서는 아래 세 가지 원칙을 지켜야한다.
    - 정의 기반 프로그래밍을 한다.
    - 최대한 빨리 반환한다.
    - Error case보단 normal case에 집중한다.
    - 로직을 케이스로 나누지 않고 대상으로 나눈다.
  - 정의 기반 프로그래밍
    - lambda, parameter, receiver, call-chain 등에 이름을 붙여 사용하는 방식이다.
    - 단, 이 역시 마찬가지로 지나칠 경우 불필요한 state를 생성하고, 불필요한 강한 결합을 만들어 가독성을 저해할 수 있다.

  ```kotlin
  // 정의 기반 프로그래밍의 예시
  // 아래와 같은 code보다
  showImage(convertImage(cropImage(loadImage(imageUri), Shape.CIRCLE), ImageFormat.PNG))
  
  // 아래와 같은 code가 더 이해하기 쉽다.
  val originalBitmap = loadImage(imageUri)
  val croppedBitmap = cropImage(originalBitmap, Shape.CIRCLE)
  val croppedPng = convertImage(croppedBitmap, ImageFormat.PNG)
  showImage(croppedPng)
  ```

  - Error case보단 normal case에 집중한다.
    - Normal case는 절차가 달성하고자 하는 주 목적을 달성하는 것을 의미한다.
    - Error case는 목적 달성 없이 절차가 종료되는 것을 의미한다.
    - Normal case에 집중하려면 반환을 빨리 하면 된다.

  ```python
  # error case에 집중하다보면 아래와 같은 code가 나오게 된다.
  # 이 절차가 달성하고자 하는 목적이 무엇인지 불분명해진다.
  if is_network_available():
      query_result = query_to_server()
      if query_result.is_valid():
          pass
      else:
          pass
  else:
      pass
  
  # 반면에 아래와 같이 빠르게 반환할 경우 보다 목적이 분명해진다.
  if not is_network_available():
      return
  
  query_result = query_to_server()
  if not query_result.is_valid():
      return
  
  # ...
  ```



