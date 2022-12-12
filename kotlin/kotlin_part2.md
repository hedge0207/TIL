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

  