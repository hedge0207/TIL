

#  Error

- Compile-time error와 run-time error
  - Compile-time error
    - compile 중에 검출되어 컴파일이 중단되는 error 들이다.
    - syntax error, import 관련 error 등이 이에 속한다.
    - IDE를 사용하면 대부분의 compile error를 예방할 수 있다.
  - Run-time error(bug)
    - 프로그램이 실행되는 중에 발생하는 error이다.
    - 프로그램이 예상치 못하게 동작하게 하거나, 프로그램의 실행을 중단시킨다.
  - Run-time error가 compile error에 비해 훨씬 까다롭다.
    - 프로그램이 성공적으로 compile 되었다고해서, bug가 존재하지 않는 다고 할 수 없다.



- Exception

  - 프로그래밍 문법적으로 정확하고, 아무 문제 없이 compile 됐더라도, error가 발생할 수 있는데, 이를 exception이라 부른다.
  - Exception text에는 여러 정보가 담겨 있다.
    - 예를 들어 아래 예시에서 `Exception in thread "main"` 부분은 예외가 발생한 thread의 이름을 알려준다.
    - `java.lang.NumberFormatException` 부분은 예외의 이름이며, `For input string: "> Hi :)"`는 message이다.
    - `at`으로 시작하는 여러 문장을 stack trace라 부르며, 어디서 예외가 발생했는지를 알려준다.
    - `at`으로 시작하는 각각의 문장을 stack trace element라 부른다.
    - stack trace element는 canonical name이라 불리는 각 class(아래 예시에서는  `java.lang.Integer`, `TmpKt`, `java.lang.NumberFormatException`)에서 예외가 발생한 위치를 알려주는 부분이 있다.

  ```
  Exception in thread "main" java.lang.NumberFormatException: For input string: "> Hi :)"
  	at java.lang.NumberFormatException.forInputString(NumberFormatException.java:65)
  	at java.lang.Integer.parseInt(Integer.java:580)
  	at java.lang.Integer.parseInt(Integer.java:615)
  	at TmpKt.readNextInt(tmp.kt:2)
  	at TmpKt.runIncrementer(tmp.kt:6)
  	at TmpKt.main(tmp.kt:11)
  	at TmpKt.main(tmp.kt)
  ```

  - Kotlin에서는 Exception도 객체다.
    - 따라서 변수에 할당이 가능하다.



- Exception의 계층
  - `Throwable`
    - Exception의 최상단에는 `Throwable`이라는 type이 존재한다.
    - Kotlin의 모든 `Error`와 `Exception`은 `Throwable`의 subtype이다.
    - `Error`는 일반적인 애플리케이션이 실행해선 안 되는 심각한 문제들을 다루기 위한 type이다.
    - `Throwable`은 예외 처리에 유용하게 사용할 수 있는 여러 메서드를 지원한다.
  - `Exception`
    - `Exception` type은 `IOException`, `RuntimeException` 등의 subtype을 지닌다.
    - `RuntimeException`은 다시 `ArithmeticException`, `IndexOutOfBoundsException` 등을 subtype으로 지닌다.
  - 이 처럼 모든 예외는 `Throwable`- `Exception`이라는 공통된 super type을 지닌다.



- Throw

  - `throw`를 사용하여 예외를 발생시킬 수 있다.

  ```kotlin
  fun main() {
      throw Exception("Exeption!")
  }
  ```

  - 위와 같이 최상위 `Exception` 뿐 아니라 `IndexOutOfBoundsException` 등 구체적인 exception을 발생시켜 구체적으로 어떤 예외인지를 나타내는 것이 좋다.



- `try`-`catch`

  - Kotlin에서 예외처리를 할 수 있도록 해주는 keyword들이다.
    - `try` 블록으로 예외를 발생시킬 가능성이 있는 code들을 감싼다.
    - `catch` 블록은 `try` 블록에서 특정 예외가 발생했을 때, 해당 예외에 대한 처리를 정의한다.

  ```kotlin
  try {
      // 예외를 발생시킬 수 있는 code
  } catch (e: Exception) {
      // 예외 처리를 하는 code
  }
  ```

  - 예외에 대한 정보 확인하기
    - exception 객체에 담겨 있는 `message`를 통해 예외에 대한 정보를 확인 가능하다.

  ```kotlin
  try {
      // 예외를 발생시킬 수 있는 code
  } catch (e: Exception) {
      println(e.message)
  }
  ```

  - 여러 개의 예외 처리하기
    - `catch` 블록을 추가해주면 된다.
    - 주의할 점은 아래와 같이 여러 개의 예외를 처리할 때, 예외의 계층에 대해 고려해야 한다는 점이다.
    - 예를 들어 아래 예시에서 `Exception`은 모든 예외의 super type이기 때문에 `ArithmeticException` 를 catch하는 블록보다 `Exception`을 catch하는 블록이 위에 있을 경우, 모든 예외가 `Exception` 블록에서 catch되어 `ArithmeticException`이 발생하더라도, `ArithmeticException` 블록이 실행되지 않을 수 있다.

  ```kotlin
  try {
      // 예외를 발생시킬 수 있는 code
  } catch (e: ArithmeticException) {
      print(e.message)
  } catch (e: Exception) {
      println(e.message)
  }
  ```

  - `finally`
    - `try` 블록에서 예외 발생 여부와 상관없이 무조건 실행되는 블록이다.
    - `finally` 블록은 `catch` 블록에서 예외가 발생하더라도 실행된다.

  ```kotlin
  try {
      // 예외를 발생시킬 수 있는 code
  } catch (e: Exception) {
      // 예외 처리를 하는 code
  } finally {
      // 항상 실행되는 code
  }
  ```

  - `try`는 표현식이다.
    - 다른 언어들과 달리 kotlin에서 `try`는 표현식이다.
    - 따라서 반환값을 가질 수 있다.
    - 아래 코드에서 예외가 발생할 경우 `catch` 블록의 마지막 표현식(0)이 number의 값이 되며, 발생하지 않을 경우 try의 마지막 표현식(`"hello".toInt()`)이 number의 값이 된다.
    - `finally` block은 반환되지 않는다.

  ```kotlin
  val number: Int = try { "hello".toInt() } catch (e: NumberFormatException) { 0 }
  
  // number에는 0이 담기게 된다.
  ```









# packages

- Random

  - 프로그래밍을 하다 보면 random한 숫자를 만들어야 할 일이 있다.
    - 암호화, 게임, 머신러닝 등 다양한 분야에서 random한 숫자를 필요로한다.
  - Kotlin에서는 `kotlin.random.Random`을 통해 random한 숫자를 생성할 수 있다.

  ```kotlin
  import kotlin.random.Random
  
  fun main() {
      println( Random.nextInt() ) 
      println( Random.nextLong() ) 
      println( Random.nextFloat() )
      println( Random.nextDouble() )
  }
  ```

  - 범위 지정하기

  ```kotlin
  // 100 미만의 음수가 아닌 수를 반환한다.
  Random.nextInt(100) 
  // 1이상, 100 미만의 수를 반환한다.
  Random.nextInt(1, 100) 
  ```

  - Pseudorandom numbers
    - Random한 수를 가져오는 메서드가 모두 get이 아니라 next로 시작하는 이유는 다음과 같다.
    - Random은 미리 일련의 숫자들을 정의해놓고, 메서드가 호출 될 때마다 다음 숫자를 반환해준다.
    - 이렇게 미리 정의된 일련의 숫자를 pseudorandom라 부른다.
    - 그 중 첫 번째 숫자를 seed라 부르며, seed를 기반으로 뒤의 숫자들이 정해진다. 
    - seed는 next... 메서드에 의해 반환되지 않는다.
    - seed 값을 지정해주는 것이 가능하다.

  ```kotlin
  // seed 값으로 42를 준다.
  val randomGenerator42 = Random(42)
  for (i in 0..5) {
      // 아래의 값은 kotlin의 버전이 변경되지 않는 한 항상 동일하다.
      println(randomGenerator42.nextInt(100))
  }
  
  // 매번 다른 값을 생성하고 싶다면 아래와 같이 default generator를 생성하면 된다.
  val defaultGenerator = Random.Default 
  for (i in 0..5) {                      
      defaultGenerator.nextInt(100)
  }
  ```

  