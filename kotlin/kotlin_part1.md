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



- 주석

  - Compiler에 의해 compile 되지 않는 문장이다.
    - 주로 코드를 더 명확히 하기 위해 사용한다.

  - End-of-line comment

    - `//`를 사용하여 주석을 생성할 수 있다.
  
  ```kotlin
  // This is line will be ignored by compiler
  ```
  
    - 여러 줄 comment
  
      - `/* */`를 사용하여 여러 줄 주석을 작성할 수 있다.
  
  ```kotlin
  /* multi
     line
     comment*/
  ```
  
    - Documentation comments(doc comments)
  
      - `/** */`를 사용하여 작성한 주석을 특별히 doc comments라고 부른다.
      - 주로 코드에 대한 설명을 위해 사용한다.
  
  ```kotlin
  /**
   * Documentation comments for main function
  */
  fun main() {
      // body
  }
  ```



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





# Data type

- 변수의 type

  - 모든 변수는 type을 가진다.
  - 변수의 type은 변수가 선언될 때 정해진다.
  - Kotlin에는 두 가지 type 지정 방식이 존재한다.
    - 변수에 할당된 값에 따라서 kotlin이 자동적으로 변수의 타입을 정하는 방식(type inference).
    - 변수를 선언할 때 변수의 type을 지정하는 방식.

  ```kotlin
  // type inference
  var text = "text"
  
  // 직접 지정
  var text: String = "text"
  ```

  - 만일 변수의 선언을 먼저 하고, 초기화(값의 할당)은 나중에 해야 할 경우, type inference방식은 사용할 수 없다.

  ```kotlin
  val greeting 		// error 발생
  greeting = "hello"
  ```

  - Data type의 가장 중요한 기능 중 하나는 변수에 적절하지 않은 값이 할당되는 것을 막아주는 것이다.

  ```kotlin
  val n: Int = "abc"	// Type mismatch error 발생
  ```



- Character

  - 작은 따옴표로 문자(혹은 숫자, 기호) 하나를 표현하면 Char type이 된다.
    - 크기는 16bit이다.

  ```kotlin
  val lowerCase = 'a'
  val number = '1'
  val space = ' '
  ```

  - 모든 char type의 값은 그에 해당하는 unicode 값을 지니고 있다.
    - Char type인 값에 숫자를 더하거나 빼면 unicode상에서 해당 숫자만큼 더한 char 값이 나온다.
    - 또한 이 값에 따라 대소, 동등 비교 등이 가능하다. 
    - `.code`를 통해 code 값을 확인 가능하다.

  ```kotlin
  val ch1 = 'b'
  val ch2 = ch1 + 1 // 'c'
  val ch3 = ch2 - 2 // 'a'
  
  var ch = 'A'
  
  ch += 10
  println(ch)   // 'K'
  println(++ch) // 'L'
  println(++ch) // 'M'
  println(--ch) // 'L'
  
  println('a' < 'c')  // true
  
  print('a'.code)		// 97(ascii code 97, 16진수로는 0x61)
  ```

  - escape sequences
    - `\`로 시작하는 특수한 character들이다.
    - `'\n'`: newline
    - `'\t'`: tab
    - `'\r'`: 커서를 행의 앞으로 이동
    - `'\''`: single quote
    - `'\"'` : double quote

  - `isDigit()`
    - 주어진 char 값이 숫자형이면 하면 true, 아니면 false를 반환한다.

  ```kotlin
  val one = '1'
  
  val isDigit = one.isDigit()	// true
  ```

  - `isLtter()`
    - 주어진 char 값이 문자면 true, 아니면 false를 반환한다.

  ```kotlin
  val one = '1'
  
  val isLetter = one.isLetter() // false
  ```

  - `isLetterOrDigit()`
    - 주어진 char 값이 문자거나 숫자면 true, 아니면 false를 반환한다.

  ```kotlin
  val one = '1'
  
  val isLetter = one.isLetterOrDigit() // true
  ```

  - `isUpperCase()`, `isLowerCase()`
    - 주어진 char 값이 각각 대문자, 소문자면 true, 아니면 false를 반환한다.

  ```kotlin
  val capital = 'A'
  
  val isUpperCase = capital.isUpperCase() // true
  val isLowerCase = capital.isLowerCase() // false
  ```

  - `uppercase()`, `lowercase()`
    - 주어진 char 값을 각기 대문자, 소문자로 변환한 값을 **string** type으로 반환 한다.
    - Kotlin 1.5 이전까지는 `toUpperCase`, `toLowerCase`를 사용했다.
    - char type으로 반환하려면 `uppercaseChar`, `lowercaseChar`를 사용하면 된다.



- String

  - 큰 따옴표로 값을 표현한다.
    - 따라서 `"A"`는 character가 아닌 string이다.

  ```kotlin
  val message = "Hello World!"
  ```

  - index로 string의 각 character에 접근하는 것이 가능하다.
  
  ```kotlin
  val greeting = "Hello"
  
  val first = greeting[0]  // 'H'
  ```
  
  - Immutable하다.
  
  ```kotlin
  val valString = "string"
  valString[3] = 'o' // error
  ```
  
  - String의 길이 구하기
    - character의 개수와 동일하다.
    - `length`를 사용한다.
  
  ```kotlin
  val language = "kotlin"
  println(language.length)	// 6
  ```
  
  - 빈 string인지 확인하기
    - `isEmpty()` 메서드를 사용하거나, 길이가 0인지를 확인한다.
  
  ```kotlin
  val emptyString = ""
  println(emptyString.length == 0) //true
  println(emptyString.isEmpty()) //true
  ```

  - String 합치기
    - `+` 연산자를 사용한다.
    - text type이 아닌 다른 type과 합치는 것도 가능하다.
  
  ```kotlin
  val hello = "hello"
  val name = "Tom"
  println(hello + " " + name)		// hello Tom
  
  val age = 47
  println(name + ":" + age)		// Tom:47
  ```
  
  - 대소문자 변경하기
    - `lowercase()`, `uppercase()`  메서드를 사용한다.

  ```kotlin
  val example = "UPPERCASE String"
  println(example.lowercase())
  
  val example = "Lowercase String"
  println(example.uppercase())
  ```
  
  - String 반복하기
    - `repeat` 메서드를 활용하여 string을 반복할 수 있다.
    - `*` 연산자는 사용 할 수 없다.
  
  ```kotlin
  print("Hello".repeat(4))	// HelloHelloHelloHello
  ```
  
  - `substring`
    - `substring` 메서드를 사용하여 substring을 얻을 수 있다.
    - 만일 두 번째 인자를 주지 않을 경우 첫 번째 인덱스부터 끝 까지 substring을 생성한다.
  
  ```kotlin
  val greeting = "Hello"
  println(greeting.substring(0, 3)) // "Hel"
  println(greeting.substring(2))    // "llo"
  ```
  
  - `substringAfter`, `substringBefore`
    - 각기 인자로 받은 delimiter의 이후, 이전까지의 substring을 생성한다.
    - String에서 가장 앞에 위치한 delimiter를 기준으로 한다.
    - 만일 delimiter가 존재하지 않을 경우 string 전체를 반환한다.
    - 두 번째 인자로 delimiter가 존재하지 않을 때 반환할 string을 넘길 수 있다.
  
  ```kotlin
  println(greeting.substringAfter('l'))  // "lo"
  println(greeting.substringBefore('o')) // "Hell"
  println(greeting.substringBefore('z')) // "Hello"
  println(greeting.substringBefore('z', "can't find a character"))
  ```
  
  - `substringAfterLast`, `substringBeforeLast`
    - `substringAfter`, `substringBefore`와 유사하지만 차이는 string에서 가장 앞에 위치한 delimiter를 기준으로 한다는 점이다.
  - `replace`
    - Substring을 다른 substring으로 교체할 수 있다.
    - `replaceFirst`를 사용하면 가장 처음 매칭된 substring 하나만 교체한다.
  
  ```kotlin
  val example = "Good morning..."
  println(example.replace("morning", "bye")) // "Good bye..."
  println(example.replace('.', '!'))         // "Good morning!!!"
  ```
  
  - `split`
    - String을 separator로 분리하여 List type으로 반환한다.
  
  ```kotlin
  val sentence = "a long text"
  val wordsList: List<String> = sentence.split(" ")
  val mutableWordList = sentence.split(" ").toMutableList()
  ```
  
  - Raw string
    - 쌍 따옴표 3개로 감싼 문자열.
    - escape sequence를 사용하지 않아도 문자열을 있는 그대로 저장한다.
  
  ```kotlin
  val largeString = """
      This is the house that Jack built.
        
      This is the malt that lay in the house that Jack built.
         
      This is the rat that ate the malt
      That lay in the house that Jack built.
         
      This is the cat
      That killed the rat that ate the malt
      That lay in the house that Jack built.
  """.trimIndent()	// 첫 줄과 마지막 줄을 삭제하고, 들여쓰기를 정리한다.
  print(largeString)
  ```
  
  - String template
    - 문자열 내에서 `$변수명` 형태로 변수명을 넣으면, 해당 변수의 값이 출력되게 된다.
    - 단순 변수명 뿐 아니라 `{}`로 묶어 표현식을 사용하는 것도 가능하다.
    - `+` 연산자를 통해 문자열을 합치는 것 보다 string template을 사용하는 것을 권장한다.
  
  ```kotlin
  val city = "Paris"
  val temp = "24"
  
  println("Now, the temperature in $city is $temp degrees Celsius.")
  
  // 표현식 사용
  val language = "Kotlin"
  println("$language has ${language.length} letters in the name")
  
  // 권장사항
  val language = "Kotlin"
  println("Have a nice $language!")        // nice code
  println("Have a nice " + language + "!") // bad practice
  ```
  
  



- Number

  - Kotlin에는 4가지 integer이 type 있다(큰 수부터 작은 수 순으로).
    - Long: 64bit, -(2<sup>63</sup>) ~ (2<sup>63</sup>)-1
    - Int: 32bit, -(2<sup>31</sup>) ~ (2<sup>31</sup>)-1
    - Short: 16bit, -(2<sup>15</sup>) ~ (2<sup>15</sup>)-1
    - Byte: 8bit, -(2<sup>7</sup>) ~ (2<sup>7</sup>)-1
  - Long type변수를 type inference를 통해 선언 할 경우 수자 뒤에 `L`을 붙인다.
    - 명시적으로 Long type으로 지정한 경우 붙이지 않아도 된다.
    - 혹은 Int type이 표현할 수 있는 수 보다 더 큰 값을 할당하면 자동으로 Long type이 된다.

  ```kotlin
  val twoMillion = 2_000_000L
  val twoMillion: :Long = 2_000_000
  ```

  - Interger type의 값에 `_`를 포함시키는 것이 가능하다.
    - 숫자가 너무 클 경우 숫자의 단위를 보다 쉽게 확인하기 위해 사용한다.

  ```kotlin
  var num = 100_000_000
  ```

  - Kotlin에는 2가지 Floating-point type이 있다.
    - Double: 64bits
    - Float: 32bits
    - Double을 Float보다 많이 사용한다.
  - Float type변수를 type inference를 통해 선언 할 경우 수자 뒤에 `f`을 붙인다.
    - 명시적으로 Float type이라고 지정한 경우 붙이지 않아도 된다.

  ```kotlin
  val pi = 3.1415              // Double
  val e = 2.71828f             // Float because it is tagged with f
  val fraction: Float = 1.51f
  ```

  - 각 숫자 type별 최대값과 최소값을 보고 싶을 경우 `MAX_VALUE`와 `MIN_VALUE`를 사용한다.

  ```kotlin
  println(Int.MIN_VALUE)  // -2147483648
  println(Int.MAX_VALUE)  // 2147483647
  println(Long.MIN_VALUE) // -9223372036854775808
  println(Long.MAX_VALUE) // 9223372036854775807
  ```

  - 각 type별 bit 또는 byte 크기를 보는 것도 가능하다.

  ```kotlin
  println(Int.SIZE_BYTES) // 4
  println(Int.SIZE_BITS)  // 32
  ```

  - Unsigned integer
    - Int, Long, Byte, Short와 같은 integer type에는 양수뿐 아니라 음수도 저장 가능하다.
    - Kotlin은 음수가 아닌 수(0, 양수)만을 저장하기 위한 자료형도 지원한다.
    - UByte: 0~255까지의 8 bit integer
    - Ushort: 0~65535까지의 16 bit interger
    - UInt: 4,294,967,295까지의 32 bit integer
    - ULong: 18,446,744,073,709,551,615까지의 64 bit interger
    - type을 명시하고, 값 뒤에 `u`를 붙인다.
    - type 명시 없이 값 뒤에 `u`를 붙이면 자동으로 UInt type이 된다.
    - Long type의 경우 `uL` 혹은 `UL`을 붙여준다.

  ```kotlin
  val uByte: UByte = 5u
  val uShort: UShort = 10U
  
  val smallSize = 100u	 // UInt type
  val smallLong = 10uL
  ```

  - Data type overflow
    - 만일 값이 data type이 담을 수 있는 값 보다 커질 경우 예상치 못 한 결과가 나올 수 있다.
    - 아래 예시에서 Int type의 최대값인 2147483647는 이진수로 변환하면 01111111111111111111111111111111<sub>2</sub>이다.
    - 여기에 1을 더하면 10000000000000000000000000000000<sub>2</sub>가 된다.
    - 10000000000000000000000000000000<sub>2</sub>는 01111111111111111111111111111111<sub>2</sub>의 보수로, 음수가 된다.

  ```kotlin
  // MAX_VALUE: Int = 2147483647
  var d: Int = 2147483647
  d += 1
  println(d) // -2147483648
  ```



- Boolean

  - `true` 또는 `false` 값만 저장이 가능하다.
    - 크기는 1bit이다.
  
  ```kotlin
  val enabled = true
  ```
  
  - kotlin에서는 0과 false가 다르다.





## Type 변환

- 숫자 type들 사이의 type 변환

  - type 변환하기
    - `toDouble()` method를 통해 다른 숫자 type을 Double type으로 변경할 수 있다.
    - 주의할 점은 `toDouble()`는 값 자체를 변경시키는 것이 아니라 변경된 값을 반환한다는 점이다.
    - 마찬가지로 다른 자료형으로의 변환도 `to<자료형>` 메서드를 사용하면 된다.

  ```kotlin
  val num: Int = 100
  num = num.toDouble()
  println(num)
  ```

  - 만일 특정 type이 표현할 수 있는 이상의 값을 변환하려고 할 경우, type이 표현할 수 있는 값으로 변환된다.
    - 이를 type overflow라 부른다.

  ```kotlin
  val bigNum: Long = 100_000_000_000_000
  
  val n: Int = bigNum.toInt() // 276447232
  ```

  - target type이 source type보다 클 경우에도 변환이 가능하다.
    - Java, C# 등에서는 불가능하다.
    - 예를 들어 아래 예시에서 처럼 target type인 Long은 source type인 Int보다 큰데도 변환이 가능하다.

  ```kotlin
  val num: Int = 100
  val bigNum: Long = num.toLong() // 100
  ```

  - Char type의 경우 숫자형 type이 아님에도 불구하고 unicode 값 기반으로 변환이 가능하다.

  ```kotlin
  val n1: Int = 125
  val ch: Char = n1.toChar() // '}'
  val n2: Int = ch.code      // 125
  ```



- Short와 Byte type으로 변환

  - Short와 Byte type은 매우 작기 때문에 거의 사용되지 않는다.
    - 그럼에도 변환 메서드를 지원하긴 한다.
    - 각기 `toShort`, `toByte` 메서드를 사용하여 변환한다.
    - 그러나 Short와 Byte type으로 변환하는 것을 최대한 지양해야한다.
    - 이후 버전에서는 변환하는 기능 자체가 삭제될 예정이다.

  - Short와 Byte type으로 변환하는 것을 최대한 지양해야하는 이유
    - 두 type의 size가 너무 작기 때문에, 예상치 못한 결과가 나올 수 있다.
    - 따라서 우선 Int type으로 변경하고, 그 값을 다시 Short와 Byte type으로 변환하는 것을 권장한다.

  ```kotlin
  val floatNumber = 10f
  val doubleNumber = 1.0
  
  val shortNumber = floatNumber.toShort() // avoid this
  val byteNumber = doubleNumber.toByte()  // avoid this
  
  val shortNumber = floatNumber.toInt().toShort() // correct way
  val byteNumber = doubleNumber.toInt().toByte()  // correct way
  ```



- Type coercion

  - 만일 서로 type이 다른 두 숫자 사이에 연산을 할 경우 결과 값의 type은 아래 순서로 결정된다.
    - Byte, Short -> Int -> Long -> Float -> Double
    - 예를 들어 Int type과 Long type을 더할 경우 결과 값은 Long type이 된다.

  ```kotlin
  val num: Int = 100
  val longNum: Long = 1000
  val result = num + longNum // 1100, Long
  ```

  - 그러나 short type과 byte type의 경우 약간 다르다.
    - 이들 type은 같은 type끼리 연산하더라도 결과값은 무조건 Int type이 된다.

  ```kotlin
  val one: Byte = 1
  val two: Byte = 2
  val three = one + two // 3, Int
  
  val fourteen: Short = 14
  val ten: Short = 10
  val four = fourteen - ten // 4, Int
  
  val hundred: Short = 100
  val five: Byte = 5
  val zero = hundred % five // 0, Int
  ```

  - 만일 byte(혹은 short) type 간의 연산 결과를 원래 type으로 얻고싶다면 아래와 같이 수동으로 변환해줘야한다.

  ```kotlin
  val one: Byte = 1
  val five: Byte = 5
  val six = (one + five).toByte() // 6, Byte
  ```



- String type의 변환

  - `toString` 메서드를 사용하여 모든 type을 string type으로 변환 가능하다.

  ```kotlin
  val num = 42
  val double = 4.2
  val char = 'a'
  val bool = true
  
  println(num.toString())			// "42"
  println(double.toString())		// "4.2"
  println(char.toString())		// "a"
  println(bool.toString())		// "true"
  ```

  - 또한 string type의 값이 숫자 형태일 경우 숫자형으로 변환이 가능하다.

  ```kotlin
  val num = "42".toInt()
  val double = "4.2".toDouble()
  ```

  - boolean도 마찬가지다.
    - `toBoolean()` 메서드는 대소문자를 구분하지 않는다.
    - 대소문자를 구분하고자 한다면 `toBooleanStrict` 메서드를 사용해야한다.
    - `toBooleanStrictOrNull` 메서드는 값이 true나 false가 아닐 경우 null을 반환한다.
  
  ```kotlin
  val bool = "true".toBoolean()
  ```





# 연산자

- 산술연산자

  - Kotlin에는 5개의 산술 연산자가 있다.
    - `+`(덧셈),  `-`(뺄셈),  `*`(곱셈),  `/`(나눗셈), `%`(나머지)
    - 이들은 모두 이항 연산자로, 연산자의 좌우에 피연산자를 하나씩 받는다.
  - 예시

  ```kotlin
  println(4+2)	// 6
  println(4-2)	// 2
  println(4*2)	// 8
  println(4/2)	// 2
  println(4%2)	// 0
  ```



- 단항연산자

  - 단항연산자는 피연산자를 하나만 받는 연산자를 의미한다.
  - 예시

  ```kotlin
  println(+42)	// 42
  println(-42)	// -42
  ```



- 할당 연산자

  - 변수에 값을 할당할 때 사용하는 연산자이다.

  ```kotlin
  var value = "something"	// 할당 연산자 "="
  ```

  - 복합 할당 연산자
    - 할당 연산자와 산술연산자를 결합한 형태의 할당 연산자이다.
    - `+=`: 좌측의 피연산자에 우측의 피연산자를 더한 값을 좌측의 피연산자에 할당한다.
    - `-=`: 좌측의 피연산자에서 우측의 피연산자를 뺀 값을 좌측의 피연산자에 할당한다.
    - `*=`: 좌측의 피연산자에 우측의 피연산자를 곱한 값을 좌측의 피연산자에 할당한다.
    - `/=`: 좌측의 피연산자에서 우측의 피연산자를 나눈 값을 좌측의 피연산자에 할당한다.
    - `%=`: 좌측의 피연산자에서 우측의 피연산자를 나눈 나머지 값을 좌측의 피연산자에 할당한다.

  ```kotlin
  var a = 3
  a += 2 // 5
  a -= 2 // 3
  a *= 2 // 6
  a /= 2 // 3
  a %= 2 // 1
  ```

  - 복합 할당 연산자는 이미 할당된 값에만 가능하다.

  ```kotlin
  var a: Int
  a += 42		// error 발생
  ```



- 증감연산자

  - 변수의 값을 1 증가시키거나 1 감소시킬 때 사용하는 연산자이다.

  ```kotlin
  var num = 3
  num++  // 4
  num--  // 3
  ```

  - prefix로 사용
    - 변수 앞에 사용할 경우, 변수가 사용되기 전에 증가시킨다.

  ```kotlin
  var a = 10
  val b = ++a		// a를 먼저 1 증가시키고, b에 할당
  println(a)  	// a = 11
  println(b)  	// b = 11
  ```

  - postfix로 사용
    - 변수 뒤에 사용할 경우, 변수가 사용된 후에 증가시킨다.

  ```kotlin
  var a = 10
  val b = a--		// a를 b에 할당한 후, a를 감소시킨다.
  println(a)  // a = 9
  println(b)  // b = 10
  ```

  - 예시

  ```kotlin
  var num = 0
  println(num++ + ++num)	// 2
  
  /*
  계산 순서는 다음과 같다.
  (num = 0) num++ + ++num
  (num = 1) 0 + ++num 
  (num = 2) 0 + 2
  */
  ```



- 우선 순위

  - 연산자는 아래와 같은 우선순위를 가진다.
    - 괄호
    - Postfix 증감연산자
    - 단항 `+`, `-` 연산자 및 postfix 증감연산자
    - 곱샘, 나눗셈, 나머지 연산자
    - 덧셈, 뺄셈 연산자
    - 할당연산자

  - 예시

  ```kotlin
  var a = 5
  val b = 9
  val c = 3
  val d = a++ + (b / 2) - c - 4
  println(d)   // 2
  ```



- 논리 연산자

  - NOT
    - Boolean 값을 반전시키는 단항 연산자이다.
    - `!`로 사용한다.

  ```kotlin
  val t = true
  val f = !t
  ```

  - AND
    - AND는 두 값 모두 참일 경우에만 true를 반환하는 이항연산자다.
    - `&&`로 사용한다.

  ```kotlin
  val b1 = true
  val b2 = true
  val b3 = b1 && b2	// true
  ```

  - OR
    - OR는 두 값 중 하나라도 참이면 true를 반환하는 이항 연산자다.
    - `||`로 사용한다.

  ```kotlin
  val b1 = true
  val b2 = false
  var b3 = b1 || b2 // true
  ```

  - XOR(eXclusive OR)
    - 두 값이 서로 다르면 true를 반환하는 이항 연산자다.
    - `xor`로 사용한다.

  ```kotlin
  val b1 = false xor false // false
  val b2 = false xor true  // true
  ```

  - 평가 순서
    - `!`
    - `xor`
    - `&&`
    - `||`



- 관계 연산자
  - Kotlin은 아래와 같은 관계 연산자들을 제공한다.
    - `==`
    - `!=`
    - `===`
    - `!==`
    - `>`
    - `>=`
    - `<`
    - `<=`
  - 관계 연산자는 boolean 값을 반환한다.
  - Int type과 Long type 사이의 대소비교는 가능하지만 동등비교(`==`, `!=`)는 불가능하다.
  - Kotlin에서 아래와 같은 비교는 불가능하다.
    - `a <= b <= c`
    - 위와 같은 비교를 하려면 논리연산자를 사용하여 `a<=b && b<=c`와 같이 작성해야 한다.



- `in` 연산자
  - 좌항이 우항에 존재하는지를 판별한다.



# if expression

- 조건에 따라 다른 연산을 할 수 있게 해주는 표현식이다.
  - true 혹은 false를 반환하는 boolean 표현식에 따라 다른 연산을 수행한다.
  - 다른 프로그래밍 언어와 달리, Kotlin에서 if는 문(statemnet)이 아니라 표현식(expression)이다.
    - 따라서 value를 반환할 수 있다.



- if expression

  - `if` keyword를 사용한다.
    - 표현식이 true를 반환하면, block 내의 코드가 실행된다.

  ```kotlin
  if (표현식) {
      // 표현식이 true일 경우 수행할 연산
  }
  ```

  - `else` 키워드를 사용하면 if문에 걸리지 않았을 경우의 연산을 지정할 수 있다.

  ```kotlin
  if (표현식) {
      // 표현식이 true일 경우 수행할 연산
  } else {
      // 표현식이 false일 경우 수행할 연산
  }
  ```

  - `else if` 키워드를 사용하여 조건을 추가하는 것이 가능하다.

  ```kotlin
  if (표현식) {
      // 표현식이 true일 경우 수행할 연산
  } else if (표현식2) {
      // 표현식2가 true일 경우 수행할 연산
  }
  ```

  - 값을 반환하기
    - 상기했듯, if는 문이 아니라 표현식이기에 값을 반환할 수 있다.
    - 조건 내에 가장 마지막 값을 반환한다.
    - 또한 if를 값을 반환하기위해 사용할 경우 반드시 else도 함께 사용해야 한다.

  ```kotlin
  // 아래 연산의 결과 max에는 a 또는 b가 할당된다.
  val max = if (a > b) {
      println("Choose a")
      a
  } else {
      println("Choose b")
      b
  }
  
  // 혹은 아래와 같이 사용하는 것도 가능하다.
  fun main() {
      val a = readln().toInt()
      val b = readln().toInt()
  
      println(if (a == b) {
          "a equal b"
      } else if (a > b) {
          "a is greater than b"
      } else {
          "a is less than b"
      })
  }
  ```





# when expression

- 여러 조건에 따라 각기 다른 코드가 실행되도록 해주는 표현식이다.

  - 다른 프로그래밍 언어의 switch문과 유사하다.
  - `when` 키워드를 사용한다.
    - `else`는 아무 조건에도 해당하지 않을 때 실행된다(굳이 정의하지 않아도 된다).

  ```kotlin
  fun main(){
      val (var1, op, var2) = readln().split(" ")
  
      val a = var1.toInt()
      val b = var2.toInt()
  
      when (op) {
          "+" -> println(a + b)
          "-" -> println(a - b)
          "*" -> println(a * b)
          else -> println("Unknown operator")
      }
  }
  ```

  - 아래와 같이 comma로 구분하여 하나의 branch에 여러 조건을 주는 것도 가능하다.

  ```kotlin
  when (op) {
      "+", "plus" -> println(a + b)
      "-", "minus", -> println(a - b)
      "*", "times" -> println(a * b)
      else -> println("Unknown operator")
  }
  ```

  - 각 branch 별 실행할 block을 작성하는 것도 가능하다.

  ```kotlin
  when (op) {
      "+", "plus" -> {
          val sum = a + b
          println(sum)
      }
      "-", "minus" -> {
          val diff = a - b
          println(diff)
      }
      "*", "times" -> {
          val product = a * b
          println(product)
      }
      else -> println("Unknown operator")
  }
  ```



- 표현식으로서의 when

  - `when`은 표현식이기에 값을 반환할 수 있다.

    - 이 경우 모든 branch는 반환 값이 있어야 하며, `else` branch를 반드시 작성해야한다.

    - 또한 block으로 작성했다면 block의 마지막 줄이 반환되므로, block의 마지막줄은 단일 값이어야한다.

  ```kotlin
  when (op) {
      "+", "plus" -> {		// block으로 작성
          val sum = a + b
          sum					// 마지막 줄에 단일 값을 준다.
      }
      else -> println("Unknown operator")
  }
  ```



- argument 없이 `when` 사용하기

  - 이 경우 모든 branch의 조건이 boolean 표현식이어야한다.

  ```kotlin
  fun main(){
      val n = readln().toInt()
      
      when {
          n == 0 -> println("n is zero")
          n in 100..200 -> println("n is between 100 and 200")
          n > 300 -> println("n is greater than 300")
          n < 0 -> println("n is negative")
          // else-branch is optional here
      }
  }
  ```

  







# 반복문

- 일련의 statement들을 반복해서 실행할 수 있게 해준다.
  - `continue`, `break` 등 다른 언어에서 사용되는 keyword들을 사용 가능하다.




- repaet

  - `repeat` keyword를 사용하여 repeat block 내의 문을 여러번 반복할 수 있다.
    - n에는 반복할 횟수를 설정한다.
    - 만일 0이하의 값이 올 경우 repeat문 자체가 무시된다.

  ```kotlin
  repeat(n) {
      // 반복할 statemnet
  }
  ```

  - `it`
    - repeat block 내에서 `it` 변수를 사용하여 몇 번째 반복인지 확인이 가능하다.

  ```kotlin
  fun main() {
      repeat(3) {
          println(it)
      }
  }
  ```




- while

  - 조건이 true인 동안 반복을 지속한다.
    - 조건의 true/false 판단은 다음 반복이 시작되기 전에 이루어진다.

  ```kotlin
  while (condition) {
      // 반복할 statement
  }
  ```

  - `do...while`
    - 그냥 `while`문과 달리 실행 후에 조건의 true/false를 판단한다.
    - 무조건 한 번은 실행되기에 block 내에 조건에 사용할 변수를 선언해도 된다.

  ```kotlin
  do {
      // 반복할 statement
  } while (condition)
  ```



- range

  - Kotlin에서는 `..`를 활용하여 range를 표시한다.

  ```kotlin
  val range = 1..100
  ```

  - `in` keyword는 좌측의 값이 우측 안에 포함되는지를 판단한다.
    - `in` 앞에 `!`를 붙이면 포함하지 않는지를 판단한다.

  ```kotlin
  println(5 in 5..15)  // true
  println(20 in 5..15) // false
  println(20 !in 5..15) // true
  ```

  - 숫자뿐 아니라 Char(unicode 순), String(사전 순) type에도 적용이 가능하다. 



- for

  - range, 배열, 그리고 요소들의 집합을 순회할 수 있게 해준다.

  ```kotlin
  for (element in source) {
      // 반복할 내용
  }
  ```

  - 문자열로 이루어진 range를 순회하는 것은 불가능하다.
    - 아래 예시에서 `aa`와 `ae`라는 문자열 사이에는 무수히 많은 값들("ab", "aba", "abb"."aaab" 등)이 존재할 수 있다.
    - 따라서 문자열로 이루어진 range를 순회하는 것은 불가능하다.
    - 그러나 char type은 가능하다.
  
  ```kotlin
  for (i in "aa".."ae") {
      print(i)
  }
  ```
  
  - 역순으로 순회하기
    - `downTo`를 사용한다.
    - b부터 a까지 내려가면서 순회한다.
  
  ```kotlin
  for (element in b downTo a) {
      // 반복할 내용
  }
  ```
  
  - 마지막 수 제외하고 순회하기
    - `until`을 사용한다.
    - a부터 b 이전까지 순회한다.
  
  ```kotlin
  for (element in a until b) {
      // 반복할 내용
  }
  ```
  
  - step 설정하기
    - `step`을 사용한다.
  
  ```kotlin
  for (i in 1..10 step 3) {
      println(i)
  }
  ```
  
  - String 순회하기
    - String의 `indices`를 사용하여 보다 간편하게 순회가 가능하다.
  
  ```kotlin
  val rainbow = "ROYGCBV"
  
  for (index in rainbow.indices){
      println("${index+1}: ${rainbow[index]}")
  }
  ```
  
  



- label 사용하기

  - label은 `@`로 끝나는 식별자를 의미한다.
    - `kotlin@`, `abc@`와 같이 Kotlin 예약어를 제외한 어떠한 문자로든 만들 수 있다.
  - `continue`, `break`문과 함께 사용하여, 반복문의 흐름을 변경할 때 사용한다.
    - 아래와 같이 외부 for문에 `loop@`라는 label을 달아주고, `break`뒤에 label을 입력하면, `loop@` label이 달린 외부 for문이 종료된다.
    - 즉, label을 달아둔 반복문의 흐름을 제어할 수 있다.
    - `for`문 뿐 아니라 `while`문에도 사용 가능하다.

  ```kotlin
  loop@ for (i in 1..3) { 
      for (j in 1..3) {
          println("i = $i, j = $j")   
          if (j == 3) break@loop  
      }  
  }
  ```



# MutableList

- Kotlin의 standard library는 배열을 다룰 수 있게 해주는 다양한 방식을 제공한다.
  - MutableList도 그 중 하나로, 같은 type의 data들을 저장할 수 있는 순서가 있는 배열이다.



- MutableList의 객체 생성하기

  - `mutableListOf`를 사용하여 MutableList 객체를 생성할 수 있다.

  ```kotlin
  val myMutableList = mutableListOf<Int>(1, 2, 3, 4)
  ```

  - type을 명시적으로 지정하지 않는 것도 가능하다.

  ```kotlin
  val myMutableList = mutableListOf(1, 2, 3, 4)
  ```

  - 빈 MutableList 객체를 생성하는 것도 가능하다.
    - 이 때는 type을 반드시 지정해줘야 한다.
  
  ```kotlin
  val myMutableList = mutableListOf<type>()
  
  // 혹은 아래와 같이 선언한다.
  val myMutableList: MutableList<Int> = mutableListOf()
  ```
  
  - `.size`를 통해 list의 size를 확인 가능하다.



- 특정 크기의 MutableList 객체 생성하기

  - `MutableList`를 사용하여 특정 크기의 MutableList 객체를 생성할 수 있다.
    - 중괄호 안에는 list 내부를 채울 값을 지정한다.

  ```kotlin
  al list = MutableList(5) { 0 }
  
  println(list) // [0, 0, 0, 0, 0]
  ```



- 요소에 접근하기

  - list의 index를 통해 접근 가능하다.
    - index는 0부터 시작한다.

  ```kotlin
  val nums = mutableListOf<Int>(1, 2, 3, 4)
  nums[0] = 5
  println(nums[0])	//5
  ```

  - 마지막 요소에 접근하기
    - Python과 같이 -1로는 접근할 수 없다.
    - 마지막 index는 `list의 크기-1 `이므로 아래와 같이 접근 가능하다.

  ```kotlin
  val nums = mutableListOf<Int>(1, 2, 3, 4)
  println(nums[nums.size-1])
  ```

  - 관련 메서드들
    - `fisrt()`: list의 첫 번째 요소를 반환한다.
    - `last()`: list의 마지막 요소를 반환한다.
    - `lastIndex()`: list의 마지막 index를 반환한다.

  ```kotlin
  val nums = mutableListOf<Int>(1, 2, 3, 4)
  println(nums.first())		// 1
  println(nums.last())		// 4
  println(nums.lastIndex())	// 3
  ```




- 메서드

  - `joinToString()`
    - list를 comma로 분리된 string으로 변환하여 반환한다.
    - comma가 아닌 다른 문자를 줄 수도 있다.

  ```kotlin
  val myList = mutableListOf("foo", "bar", "baz", "qux")
  println(myList.joinToString())   // foo, bar, baz, qux
  println(myList.joinToString("-"))   // foo-bar-baz-qux
  ```

  - 두 개의 list 합치기
    - `addAll()` 메서드를 사용하여 두 list를 합칠 수 있다.
    - `+` 연산자를 사용한다.
    - `addAll()`의 경우 list를 반환하지 않고 list에 다른 리스트를 추가하지만, `+` 연산자는 두 리스트를 합친 결과를 반환한다.

  ```kotlin
  val lst1 = mutableListOf("foo", "bar")
  val lst2 = mutableListOf("baz", "qux")
  val newList = lst1 + lst2
  
  val lst3 = mutableListOf("foo", "bar")
  val lst4 = mutableListOf("baz", "qux")
  lst1.addAll(lst2)
  ```

  - 두 개의 list 비교하기
    - `==`, `!=` 연산자를 사용한다.
    - `==`는 두 list의 요소들이 완전히 같고, 동일한 순서로 정렬되어 있을 경우에만 true를 반환한다.

  ```kotlin
  val lst1 = mutableListOf("foo", "bar")
  val lst2 = mutableListOf("foo", "bar")
  val lst3 = mutableListOf("baz", "qux")
  val lst4 = mutableListOf("bar", "foo")
  
  println(lst1 == lst2) 	// true
  println(lst1 == lst3)	// false
  println(lst1 == lst4)	// false
  ```

  - list의 element 변경하기
    - `var` keyword로 선언하든, `val` 키워드로 선언하든 상관 없이 list의 element를 변경할 수 있다.
    - 이는 list 내부의 element를 변경하는 것이지, 아예 새로운 list를 선언하여 재할당하는 것이 아니기 때문에 가능하다.

  ```kotlin
  val lst = mutableListOf("foo", "bar")
  lst[0] = "baz"
  println(lst[0])		// baz
  ```

  - list의 element 추가하기
    - `add([index,] element)` 메서드를 사용하여 추가가 가능하다.
    - 혹은 `+` 연산자를 사용해도 된다.

  ```kotlin
  val lst = mutableListOf("foo")
  lst.add("baz")
  lst.add(1, "bar")
  lst += "qux"
  ```

  - list의 element 삭제하기
    - `remove()`를 사용하여 특정 element를 삭제할 수 있다.
    - `removeAt()`을 사용하여 특정 index에 있는 element를 삭제할 수 있다.
    - `remove`의 경우 삭제에 성공하면 true, 실패하면 false를 반환하며, `removeAt()`은 삭제 후 삭제한 element를 반환한다.
    - `clear()`는 list의 모든 element를 삭제한다.

  ```kotlin
  val lst = mutableListOf("foo", "bar", "baz", "qux")
  lst.remove("foo")
  lst.remove(0)
  lst.clear()
  ```

  - list 복사하기
    - `toMutableList()`를 사용하여 복제가 가능하다.
    - 이는 객체 자체를 복제하는 것이 아니라, 새 MutableList 객체를 생성하고, 해당 객체에 기존 list의 모든 요소를 추가하는 것이다.

  ```kotlin
  val origList = mutableListOf(1, 2, 3)
  val copyList = origList.toMutalbleList()
  ```

  - list가 비었는지 확인하기
    - `isEmpty()`, `isNotEmpty()` 메서드를 사용하여 list가 비었는지 확인이 가능하다.

  - element의 index 확인하기
    - `indexOf(element)`를 사용하여 element가 list의 몇 번째 index에 있는지 확인 할 수 있다.
  - sub list 생성하기
    - `subList(from, to)`를 사용하여 list의 sub list를 생성한다.
    - from부터 to-1까지의 index에 해당하는 element들로 sub list를 생성한다.

  ```kotlin
  val lst = mutableListOf("foo", "bar", "baz", "qux")
  println(lst.subList(1,3))	// ["bar", "baz"]
  ```

  - 최대, 최소값 찾기
    - `minOrNull()`, `maxOrNull()` 메서드를 사용하여 최소, 최대값을 찾을 수 있다.
  - list의 값들 합산하기
    - `sum()` 메서드를 사용하여 list의 모든 값을 합한 값을 구할 수 있다.
  - 정렬하기
    - `sorted()`, `sortedDescending()`을 사용하여 오름차순, 내림차순으로 정렬할 수 있다.



- for문으로 순회하기

  - 요소들을 순회하기

  ```kotlin
  val members = mutableListOf("John", "Mike", "Martin", "Lucia", "Jack")
  
  for (member in members) {
      println(member)
  }
  ```

  - index로 순회하기
    - `mutableList.indices`를 사용하여 인덱스로 순회가 가능하다.

  ```kotlin
  for (index in members.indices) {
      println(members[index])
  }
  ```

  - list의 길이만큼 순회하기

  ```kotlin
  for (index in 0..members.lastIndex) {
      println(members[index])
  }
  ```



- 다차원 list

  - 다차원 list란 list들의 list를 의미한다.
  - 2차원 list 만들기
    - 다른 list들을 품고 있는 list를 main list, list 내부의 list를 nested list라 부른다.
    - nested list들이 꼭 같은 size를 가져야 하는 것은 아니다.

  ```kotlin
  val mutList2D = mutableListOf(
      mutableListOf<Int>(1, 2, 3, 4),
      mutableListOf<Int>(5, 6, 7, 8),
      mutableListOf<Int>(9, 10, 11, 12)
  )
  ```

  - 요소에 접근하기
    - 아래와 같이 각 배열의 index를 통해 접근 가능하다.

  ```kotlin
  print(mutList2D[0][0]) 	// 1
  print(mutList2D[2][3])	// 12
  ```



