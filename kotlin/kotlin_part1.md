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
  var 
  ```

  





