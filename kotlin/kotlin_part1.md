# Kotlin 개요

- Kotlin
  - JetBrain에서 개발한 프로그래밍 언어이다.
    - Java의 대체 언어로 개발되었다.
  - 주로 Android 개발에 사용된다.
    - 기존에는 Kotlin뿐 아니라 Java도 Android 개발에 많이 사용되었다.
    - Android의 개발사인 Google이 Kotlin을 공식 언어로 지정하면서 Kotlin을 사용하는 비율이 빠르게 증가하고 있다.
  - 간략한 역사
    - 2011년 Jetbrain이 Kotlin 프로젝트를 공개.
    - 이름은 러시아 상트페테르부르크 인근의 Kotlin이라는 섬에서 따왔다.
    - 2016년 Kotlin v1.0이 공개되었다.
    - 2017년 Goolgle I/O 컨퍼런스에서 Android 개발에서 Kotlin에 대한 fisrt-class support를 발표하였다.



- 기본적인 용어

  > Kotlin 이외의 언어들에서도 통용되는 용어들이다.

  - program
    - statement라 불리는 instruction들의 연속된 묶음이다.
    - 일반적으로 위에서 아래로, 작성된 순서대로 실행된다.
  - statement
    - 실행 되는 하나의 명령어다.
  - expression
    - 값을 처리하는 코드 조각이다.
  - block
    - 대괄호(`{}`)로 감싼 0개 이상의 statements들의 그룹이다.
    - program은 하나의 block으로 구성된다.
  - keyword
    - 프로그래밍 언어에서 특수한 의미를 지니는 단어들이다.
    - keyword들의 이름은 변경될 수 없다.
  - comment
    - program이 실행될 때, 실행되지 않고 무시되는 text이다.
    - 주로 코드를 설명할 때 사용한다.
  - whitespace
    - blank space, tap, newline 등을 의미한다.
    - code의 가독성 향상을 위해 사용한다.



- 변수

  - 변수란
    - 값을 저장하기 위한 저장소이다.
    - 모든 변수는 다른 변수들과 구분되기 위한 이름을 가지고 있다.
    - 변수의 값이 접근하기 위해 변수의 이름을 사용한다.
  - 변수 선언하기
    - Kotlin에서는 2 keyword로 변수를 선언할 수 있다.
    - `val`(value): 변경할 수 없는 변수를 선언하기 위해 사용한다.
    - `var`(variable): 변경 가능한 변수를 선언하기 위해 사용한다.

  ```kotlin
  // val로 선언한 변수는 변경이 불가능하다.
  val language = "Kotlin"
  
  // var로 선언한 변수는 변경이 가능하다.
  var age = 1
  age = 2
  ```

  - Type 지정하여 선언하기
    - 변수를 선언할 때 type을 지정하는 것도 가능하다.

  ```kotlin
  var text: String = "text"
  ```

  - 주의 사항

    - 변수명은 숫자로 시작할 수 없다.
    - 변수명은 대소문자를 구분한다.

    - 오직 같은 type의 값만 재할당이 가능하다.

  ```kotlin
  var num = 10
  num = 11		// 같은 type의 값만 재할당 가능
  num = "string" 	// error 발생
  ```

  - Val 변수

    - 프로그래밍을 하다보면 프로그램 실행 중에 변경되어선 안되는 변수를 사용해야 하는 경우가 있다.
    - 이러한 변수를 일반적으로  constants라 부르며, kotlin에서는 val variables라 부른다.

    - 주의할 점은 val variable이 immuatable과 완전한 동의어는 아니라는 점이다.

  ```kotlin
  // 재할당은 불가능하지만
  val myMutableList = mutableListOf(1, 2, 3, 4, 5)
  myMutableList = mutableListOf(1, 2, 3, 4, 5, 6)
  
  // 요소를 추가하는 것은 가능하다.
  val myMutableList = mutableListOf(1, 2, 3, 4, 5)
  myMutableList.add(6)
  println(myMutableList) // [1, 2, 3, 4, 5, 6]
  ```

  - const 변수
    - `val` 키워드 앞에 `const` 키워드를 추가하면, 해당 변수는 const 변수가 된다.
    - const변수는 컴파일 타임에 정의되어, 런타임에 변경되지 않는다.

  ```kotlin
  const val STRING = "Const String"
  
  // 아래와 같이 런타임에 값을 받는 것은 불가능하다.
  const val STRING = readln()
  ```



- Standard output

  - Standard output은 device에 정보를 표시해주는 기본적인 동작이다.
    - 그러나 모든 프로그램이 output을 가져야 하는 것은 아니다.
  - println
    - `println`함수(print line)는 새로운 줄에 string을 출력한다.
    - 출력시에는 쌍따옴표는 사라진다.

  ```kotlin
  println("Kotlin is a modern programming language.")		// Kotlin is a modern programming language.
  println() 												// 공백 line 출력
  println("It is used all over the world!")				// It is used all over the world!
  ```

  - print
    - println과 달리 개행을 하지 않는다.

  ```kotlin
  print("I ")
  print("know ")
  print("Kotlin ")
  print("well.")
  
  // I know Kotlin well.
  ```



- Standard input

  - `readLine`
    - Kotlin에서 standard input으로부터 data를 읽기 위한 함수
    - 입력으로 들어온 모든 값을 string으로 읽는다.
    - `readln` 함수는 `readLine()!!`과 동일하게 동작하는 함수이다(1.6 버전부터 추가).

  ```kotlin
  // 입력으로 들어온 data를 읽어서 출력하는 함수
  fun main() {
      val line = readLine()!!	// !!는 null 방지를 위해 넣은 것이다.
      println(line)
  }
  ```

  - Java Scanner
    - Java standard library의 Scanner를 사용하여 standard input을 읽어올 수  있다.
    - 무조건 string으로 읽어오는 `readLine`과 달리, type을 지정 가능하다.
    - `Scanner.next()`는 line이 아니라 단어 하나를 읽는다.

  ```kotlin
  import java.util.Scanner
  
  val scanner = Scanner(System.`in`)	// System.`in`는 standard input stream을 표현하는 객체이다.
  
  val line = scanner.nextLine() // line을 읽는다.
  val num = scanner.nextInt()   // 숫자를 읽는다.
  val string = scanner.next()   // string을 읽는다.
  ```







