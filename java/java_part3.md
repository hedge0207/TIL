# 예외처리

- 예외 상황

  ```java
  package first;
  
  public class ExeptionExam {
  	
  	public static void main(String[] args) {
  		int a = 0;
  		int b = 10;
  		int c = b/a;
  		System.out.println(c);
          //Exception in thread "main" java.lang.ArithmeticException: / by zero
          //파이썬과 마찬가지로 0으로 나누려고 할 경우 Exception이 발생한다.
  	}
  }
  ```

  

- `try` - `catch` - `finally`

  - try: 에러가 발생할 수 있는 부분을 작성
  - catch: 예외 발생시 실행할 코드를 작성
    - 발생할 수 있는 예외 클래스의 이름과 예외 정보를 담을 변수명을 적는다.
    - 모든 예외 클래스는 `Exception` 클래스를 상속 받는다. 
    - 따라서 `catch(Exception 변수명)`과 같이 적으면 특정 예외가 아닌 모든 예외를 처리 할수 있다. 
    - 복수의 catch 블록을 작성할 수 있다.
  - finally: 예외 상황 발생 여부와 무관하게 실행할 코드를 작성, 생략 가능

  ```java
  package first;
  
  public class ExeptionExam {
  	
  	public static void main(String[] args) {
  		int a = 0;
  		int b = 10;
          
          try{
  		int c = b/a;
  		System.out.println(c);
          //catch는 아래와 같이 catch(발생할 수 있는 예외 클래스)형식으로 적는다. 변수에는 예외 내용이 들어가게 된다.
          //catch(Exception e)로 적으면 ArithmeticException 뿐 아니라 모든 예외가 여기서 걸리게 된다.
          }catch(ArithmeticException e){
              System.out.println(e);  
              //java.lang.ArithmeticException: / by zero
              System.out.println("0으로 나눌 수 없습니다."+e.toString());  
              //0으로 나눌 수 없습니다.java.lang.ArithmeticException: / by zero
          }finally {
          	System.out.println("어떤 경우든 실행되는 코드");
              //어떤 경우든 실행되는 코드
          }
  	}
  }
  ```

  

- Throws

  - 예외가 발생했을 경우 예외를 호출한 쪽에서 처리하도록 던져주는 것
  - `throws` 키워드를 사용하며 뒤에 예외 내용을 작성한다.
    - 하나만 작성할 수 있는 것은 아니고 ,로 구분하여 여러 예외를 throw 할 수 있다.
    - catch와 마찬가지로 모든 예외 클래스가 상속받는 `Exception` 클래스를 작성하면 모든 예외처리가 가능하다.

  ```java
  package first;
  
  public class ExceptionExam2 {
  	
  	//실제 예외가 발생하는 곳(0으로 나누게 되는 곳)은 main이 아닌 이 메소드에서 발생하게 된다.
      //그러나 여기서 예외를 바로 처리하지 않고 throws를 사용하여 예외를 호출한 main에서 예외처리를 하도록 할 수 있다.
      //아래의 경우 ArithmeticException하나만 적었지만 ,로 구분하여 다양한 예외를 throw 할 수 있다.
      //throws 예외1, 예외2
  	public static int divide(int a, int b) throws ArithmeticException{
  		int c = a/b;
  		return c;
  	}
  	
  	public static void main(String[] args) {
  		int i = 10;
  		int j = 0;
  		try {
  		int k = divide(i,j);
  		System.out.println(k);
  		}catch(ArithmeticException e) {
  			System.out.println(e);
  		}
  	}
  }
  
  ```

  

- Throw

  - 강제로 오류를 발생시키는 
  - 주로 `throws`와 함께 사용한다.

  ```java
  package first;
  
  public class ExceptionExam3 {
  	
  	//메소드
  	public static int divide(int a, int b){
  		if(b == 0){
              System.out.println("2번째 매개변수는 0이면 안됩니다.");
              //이 메소드는 반드시 int를 리턴해야 한다.
              //따라서 본래 0으로 나누는 것은 불가능함에도 return 값을 적지 않으면 에러가 발생하기에 0이라고 적어놓았다.
              //그러나 다른 사람이 보기에 계산 결과가 0이라고 착각할 수도 있으므로 아래와 같이 실행해선 안된다.
              return 0;
          }
          int c = a / b;
          return c;
  	}
  	
  	public static void main(String[] args) {
  		int i = 10;
  		int j = 0;
  		int k = divide(i,j);
  		System.out.println(k); //0
  	}
  }
  
  ```

  - 위와 같은 경우에 사용하는 것이 throw다.

  ```java
  package first;
  
  public class ExceptionExam3 {
  	
  	//메소드
  	public static int divide(int a, int b) throws IllegalArgumentException{
  		if(b == 0){
              //IllegalArgumentException이라는 예외 객체를 생성, 자바 내부에는 아래와 같이 다양한 예외 객체가 존재.
              throw new IllegalArgumentException("0으로 나눌 수 없습니다.");
          }
          int c = a / b;
          return c;
  	}
  	
  	public static void main(String[] args) {
  		int i = 10;
  		int j = 0;
  		try {
  		int k = divide(i,j);
  		System.out.println(k);
  		}catch(IllegalArgumentException e) {
  			System.out.println(e.toString()); //java.lang.IllegalArgumentException: 0으로 나눌 수 없습니다.
  		}
  	}
  }
  ```

  

- 사용자 정의 Exception

  - 굳이 사용자 정의 Exception을 만드는 이유는 클래스의 이름만으로 어떤 오류가 발생했는지 알려주기 위함이다.
  - `Exception` 클래스나 `RuntimeException ` 클래스를 상속 받아 만든 예외 클래스
    - `Checked Exception`: `Exception` 클래스를 상속 받아 정의한 예외 클래스, 반드시 오류를 처리 해야만 하는 exception, 예외 처리하지 않으면 컴파일 오류를 발생 시킨다.
    - `Unchecked Exception`: `RuntimeException ` 클래스를 상속 받아 정의한 예외 클래스 예외 처리하지 않아도 컴파일 시에는 오류를 발생시키지 않는다.
  - 방법
    - `eclipse` 기준으로 새로운 클래스 생성시 어떤 예외 클래스(checed, unchecked)를 만들지에 따라서  `superclass`에 `Exception` 이나 `RuntimeException ` 를 선택 후 생성

  ```java
  //CustomException.java
  package first;
  
  //RuntimeException을 상속
  public class CustomException extends RuntimeException {
      //생성자1
  	public CustomException(String msg){
          super(msg);
      }
      //생성자2
      public CustomException(Exception e){
          super(e);
      }
  }
  
  
  
  //ExampleForCustomExeption.java
  package first;
  
  public class ExampleForCustomExeption {
  	
  	public void exMethod(int i) throws CustomException{
  		System.out.println("메소드 시작");
  		
  		if(i<0){ 
  			throw new CustomException("넘어갈 메세지 입니다.");
  		}
  		
  		System.out.println("메소드 종료");
  	}
  	
  	public static void main(String[] args) {
  		ExampleForCustomExeption ex = new ExampleForCustomExeption();
  		ex.exMethod(1);
  		ex.exMethod(-1);
  	}
  }
  
  out
  //ex.exMethod(1);이 실행된 결과
  메소드 시작
  메소드 종료
  메소드 시작
  
  //ex.exMethod(-1);이 실행된 결과, 아래에서 직접 정의한 CustomException을 확인할 수 있다.
  Exception in thread "main" first.CustomException: 넘어갈 메세지 입니다.
  	at first/first.ExampleForCustomExeption.exMethod(ExampleForCustomExeption.java:9)
  	at first/first.ExampleForCustomExeption.main(ExampleForCustomExeption.java:18)
  ```

  





# 입출력

## 콘솔 입력

- `InputStream`

  - `System.in`은 python의 `input()`과 유사하다.
  - java 내장 클래스인 `InputStream`을 import해서 사용
  - `System.in`은 `InputStream`의 객체다.
  - `InputStream`의 `read` 메소드는 1byte의 사용자 입력을 받아들인다.
    - `read` 메소드로 읽은 1 byte의 데이터는 byte 자료형이 아닌 int 자료형으로 저장된다.
    - 저장되는 값은 0~255 사이의 아스키 코드값이다. 

  ```java
  package first;
  
  import java.io.InputStream;
  
  public class Input1 {
  
  	public static void main(String[] args) throws Exception {
          
          //System.in은 InputStream의 객체다.
          InputStream i = System.in;
  
          int a;
          a = i.read();
  
          System.out.println(a);
      }
  
  }
  
  //input a
  out
  97  //a의 아스키 코드 값
  ```

  - 여러 byte를 입력 받았을 때 모두 처리하는 방법
    - 위 방식으로는 abc라는 3byte 값을 입력 받아도 출력되는 것은 a의 아스키 코드 값인 97뿐이다.
    - 3 byte를 전부 읽히게 하고 싶다면 아래와 같이 해야 한다.

  ```java
  //방법1. 일일이 받아서 출력
  package first;
  
  import java.io.InputStream;
  
  public class Input1 {
  
  	public static void main(String[] args) throws Exception {
          InputStream i = System.in;
  
          int a;
          int b;
          int c;
  
          a = i.read();
          b = i.read();
          c = i.read();
  
          System.out.println(a);
          System.out.println(b);
          System.out.println(c);
      }
  
  }
  //input abc
  out
  97
  98
  99
      
  //방법2. 리스트에 한번에 받아서 따로 출력
  package first;
  
  import java.io.InputStream;
  
  public class Input1 {
  
  	public static void main(String[] args) throws Exception {
          InputStream in = System.in;
  
          byte[] a = new byte[3];
          in.read(a);
  
          System.out.println(a[0]);
          System.out.println(a[1]);
          System.out.println(a[2]);
      }
  }
  
  //input abc
  out
  97
  98
  99
  ```

  

- `InputStreamReader`

  - 입력 받은 값을 아스키 코드 값으로 변환하지 않고 그대로 출력하기 위해 사용
  - 입력 받을 값의 길이를 미리 정해야 한다는 단점이 존재

  ```java
  package first;
  
  import java.io.InputStream;
  import java.io.InputStreamReader;  //InputStreamReader를 import
  
  public class Input1 {
  
  	public static void main(String[] args) throws Exception {
          InputStream i = System.in;
          InputStreamReader reader = new InputStreamReader(i);
          char[] a = new char[3];
          reader.read(a);
  
          System.out.println(a);
      }
  
  }
  
  //input abc
  out
  abc
  ```

  

- `BufferedReader`

  - 입력 받을 값의 길이를 미리 정하지 않아도 입력을 받을 수 있다.

  ```java
  package first;
  
  import java.io.InputStream;
  import java.io.InputStreamReader;
  import java.io.BufferedReader;
  
  public class Input1 {
  
  	public static void main(String[] args) throws Exception {
          InputStream i = System.in;
          InputStreamReader reader = new InputStreamReader(i);
          BufferedReader br = new BufferedReader(reader);
  
          String a = br.readLine();
          System.out.println(a);
      }
  
  }
  //input abcde
  out
  abcde
  ```

  

- `Scanner`

  - 입력을 훨씬 간편하게 받을 수 있게 해준다.
  - `Scanner`의 메소드
    - `nextLine()`: 한 줄을 통째로 입력받는다.
    - `next()`: 공백을 기준으로 한 단어를 입력 받는다.
  
  ```java
  package first;
  
  import java.util.Scanner;
  
  public class Input1 {
  
  	public static void main(String[] args) {
          Scanner sc = new Scanner(System.in);
          System.out.println(sc.next());
      }
  }
  
  // input abcde
  // out
  abcde
  ```





## 콘솔 출력

- `System.out.println`
  - `System.out`은 `PrintStream` 클래스의 객체다.
    - `PrintStream`은 콘솔에 값을 출력할 때 사용되는 클래스이다. 



- `System.out.printf`

  - 같은 값이라도 다른 형식으로 출력하고자 할 때 사용한다.
    - `println`은 사용하기엔 편하지만 수의 값을 그대로 출력하므로, 값을 변환하지 않고는 다른 형식으로 출력할 수 없다.
    - 그러나 `printf`를 사용하면 소수점 둘째자리까지만 출력한다던가, 정수를 16진수나 8진수로 출력한다던가 하는 것이 가능하다.

  ```java
  byte b = 1;
  System.out.printf("b=%d%n", b);		// b=1
  
  int hexNum = 0x10;
  System.out.println("hex=%x, %d%n", hexNum, hexNum);		// hex=10, 16
  ```

  - `printf`는 지시자(specifier)를 통해 변수의 값을 여러 가지 형식으로 변환하여 출력하는 기능을 가지고 있다.
    - 지시자는 값을 어떻게 출력할 것인지를 지정해주는 역할을 한다.

  | 지시자 | 설명                                      |
  | ------ | ----------------------------------------- |
  | %b     | boolean 형식으로 출력                     |
  | %d     | 10진(decimal) 형식으로 출력               |
  | %o     | 8진(octal) 정수 형식으로 출력             |
  | %x, %X | 16진(hexa-decimal) 정수 형식으로 출력     |
  | %f     | 부동 소수점(floating-point) 형식으로 출력 |
  | %e, %E | 지수(exponent) 표현식으로 출력            |
  | %c     | 문자(charater)로 출력                     |
  | %S     | 문자열(string)로 출력                     |

  - 지시자 `%d`는 출력될 값이 차지할 공간을 숫자로 지정할 수 있다.
    - 숫자 앞에 공백을 무엇으로 채울지도 지정할 수 있다.

  ```java
  int num = 10;
  System.out.printf("[%5d]%n", num);		// [     10]
  System.out.printf("[%-5d]%n", num);		// [10     ]
  System.out.printf("[%05d]%n", num);		// [0000010]
  ```

  - 지시자 `%x`와 `%o`에 `#`을 사용하면 접두사 `0x`와 `0`이 각각 붙으며, `%X`는 16진수에 사용되는 접두사와 영문자를 대문자로 출력한다.

  ```java
  long hex = 0xFFFF_FFFF_FFFF_FFFFL;
  System.out.printf("%#x%n", hex);		// 0xffffffffffffffff
  System.out.printf("%#X%n", hex);		// 0XFFFFFFFFFFFFFFFF
  ```

  - 10진수를 2진수로 출력해주는 지시자는 없기 때문에, 정수를 2진 문자열로 변환해주는 메서드를 사용해야한다.
    - `Integer.toBinaryString(int i)`는 정수를 2진수로 변환해서 문자열로 반환한다.
    - 문자열로 반환하므로 `%s` 지시자를 사용한다.

  ```java
  System.out.printf("%s%n", Integer,toBinaryString(binNum));
  ```

  - `%f` 지시자는 전체 자리수와 소숫점 아래 자리수를 지정할 수 있다.
    - 예를 들어 아래 코드는 전체 14자리 중 10자리를 소수점 아래 자리로 출력하겠다는 의미이다.
    - `%d`와 마찬가지로 숫자 앞에 공백을 무엇으로 채울지 지정하는 것이 가능하다.

  ```java
  System.out.printf("%14.10f", d);
  System.out.printf("%014.10f", d);
  ```

  





## 파일 읽기

- `FileInputStream` 클래스를 사용하여 파일을 읽을 수 있다.

- 이 외에도 `Sacnner`를 사용하는 방법, `BufferedReader`를 사용하는 방법 등이 존재

  ```java
  package first;
  
  import java.io.BufferedReader;
  import java.io.FileReader;
  import java.io.IOException;
  
  public class Input3 {
  
  	public static void main(String[] args) throws IOException {
          BufferedReader br = new BufferedReader(new FileReader("d:/영화.txt"));
          while(true) {
              String line = br.readLine();
              if (line==null) break;
              System.out.println(line);
          }
          br.close();
      }
  }
  ```

  





# 패키지

- 비슷한 성격의 자바 클래스들을 모아놓은 자바의 디렉토리



-  `.`로 구분하여 서브 패키지를 생성할 수 있다.

  - 예를 들어 animal 패키지의 서브 패키지로 mammalia가 있고 그 서브 패키지로 dog이 있다면 아래와 같이 표현 가능하다.

  ```java
  package animal.mammalia.dog;
  ```



- 한 패키지에 속한 클래스들은 해당 패키지 폴더에 들어가게 된다.
  - .java 파일과 .class파일로 각기 src, bin 폴더에 들어가게 된다.
  - 예를 들어 `package animal.mammalia.dog;` 패키지의 클래스들은 아래와 같은 경로에 생성된다.
    - src/animal/mammalia/dog/Dog1.java
    - bin/animal/mammalia/dog/Dog1.class



- 패키지 사용하기

  - 패키지 사용을 위해선 import를 해야한다.
  - `*`를 사용하면 패키지 내의 모든 클래스를 import 한다는 뜻이다.
  - 만일 동일한 패키지 내에 있는 클래스라면 굳이 동일한 패키지 내에 있는 다른 클래스를 사용하기 위해 import 할 필요는 없다.

  ```java
  //Dog1 클래스만 import
  import animal.mammalia.dog.Dog1;
  
  //dog 패키지 내의 모든 클래스 import
  import animal.mammalia.dog.*;
  ```






# Enum

- 열거형

  - 서로 관련된 상수를 편리하게 선언하기 위한 것
    - 여러 상수를 정의할 때 사용하면 유용하다.
    - JDK 1.5부터 새로 추가되었다.
  - 기존에 아래와 같았던 class가

  ```java
  class Card {
      static final int CLOVER = 0;
      static final int HEART = 1;
      static fianl int DIAMOND = 2;
      static final int SPADE = 3;
      
      stacic final int ACE = 0;
      static final int TWO = 1;
      static final int THREE = 2;
      
      final int kind;
      final int value;
  }
  ```

  - Enum을 사용하면 보다 단순해진다.

  ```java
  class Card {
      // 열거형 kind
      enum Kind { CLOVER, HEART, DIAMOND, SPADE }
      // 열겨형 Value
      enum Value { ACE, TWO, THREE }
      
      final Kind kind;
      final Value value
  }
  ```

  - Typesafe enum
    - Java의 enum은 타입에 안전한 열거형이다.
    - C에서는 타입이 달라도 값이 같으면 조건식 결과가 참이었으나, Java의 열거형은 타입까지 체크한다.
    - 이는 실제 값이 같아도 타입이 다르면 컴파일 에러가 발생한다는 의미이다.
    - 값뿐만 아니라 타입도 체크하기 때문에 typesafe라 표현한다.

  ```java
  // Enum을 사용하지 않았을 때, 아래는 참이 되지만 의미상으로는 거짓이어야 한다.
  Card.HEART == Card.TWO 	
      
  // Enum을 사용했을 때, 컴파일 에러가 발생한다.
  Card.Kind.HEART == Card.TWO
  ```

  - Enum을 사용하면 상수가 변경되더라도 기존의 소스를 다시 컴파일하지 않아도 된다.
    - 원래 상수의 값이 바뀌면, 해당 상수를 참조하는 모든 소스를 다시 컴파일해야 한다.
    - 그러나 열거형 상수를 사용하면, 기존의 소스를 다시 컴파일하지 않아도 된다.



- 열겨형의 정의와 사용

  - 열거형을 정의하는 방법

  ```java
  enum <열거형이름> { 상수명1, 상수명2, ... }
  
  // e.g.
  enum Direction { EAST, WEST, SOUTH, NORTH}
  ```

  - 열거형에 정의된 상수를 사용하는 방법
    - `열거형이름.상수명`으로 사용하면 된다.
    - 클래스의 static 변수를 참조하는 것과 동일하다.

  ```java
  dir = Direction.SOUTH
  ```

  - 열거형 상수간의 비교
    - 열거형 상수간의 비교에는 `==`를 사용할 수 있으며 `equals()`가 아닌 `==`로 비교한다는 것에서 알 수 있듯 매우 빠른 성능으로 비교가 가능하다.
    - 그러나 `<`, `>`와 같은 비교 연산자는 사용할 수 없고, `compareTo()`는 사용 가능하다.

  ```java
  dir == Direction.SOUTH
  ```

  - `switch`문의 조건식에도 열거형을 사용할 수 있다.
    - 이 때 주의할 점은 case문에 열거형의 이름은 적지 않고 상수의 이름만 적어야 한다는 것이다.

  ```java
  void move() {
      switch(dir) {
          case EAST:
              // ...
          case WEST:
              // ...
          // ...
      }
  }



- `java.lang.Enum`

  - 모든 열거형의 조상이 되는 클래스이다.
    - 아래와 같은 메서드를 가지고 있다(즉, 모든 열거형은 아래 메서드를 사용 가능하다).

  | 메서드                                      | 설명                                                      |
  | ------------------------------------------- | --------------------------------------------------------- |
  | `Class<E> getDeclaringClass()`              | 열거형의 Class 객체를 반환한다.                           |
  | `String name()`                             | 열거형의 상수 이름을 문자열로 반환한다.                   |
  | `int ordinal()`                             | 열거형 상수가 정의된 순서를 반환한다.                     |
  | `T valueOf(Class<T> enumType, String name)` | 지정된 열거형에서 name과 일치하는 열거형 상수를 반환한다. |

  - 컴파일러가 모든 열거형에 자동으로 추가해주는 메서드에는 아래와 같은 것들이 있다.

  | 메서드                          | 설명                                                         |
  | ------------------------------- | ------------------------------------------------------------ |
  | `static E values()`             | 열거형의 모든 상수를 배열에 담아 반환한다.                   |
  | `static E valueOf(String name)` | 상수의 이름으로 문자열 상수에 대한 참조를 얻을 수 있게 해준다. |

  - 메서드 예시

  ```java
  Direction[] dArr = Direction.values();
  
  for (Direction d : dArr) {
      System.out.printf("%s=%d%n", d.name(), d.ordinal());
  }
  ```



- 열겨헝에 멤버 추가하기

  - `Enum.ordinal()` 메서드가 열거향 상수가 정의된 순서를 반환하지만, 이 값을 열거형 상수의 값으로 사용하지 않는 것이 좋다.
  - 열거형 상수의 값이 불연속적인 경우에는 아래와 같이 열거형 상수의 이름 옆에 원하는 값을 괄호와 함께 적어주면 된다.

  ```java
  enum Direction { EAST(3), WEST(9), SOUTH(6), NORTH(12) }
  ```

  - 그 후 지정된 값을 저장할 수 있는 인스턴스 변수와 생성자를 새로 추가해야한다.
    - 이 때 주의할 점은, 먼저 열거형 상수를 모두 정의한 다음에 다른 멤버들을 추가해야 한다는 것이다.
    - 또한 열거형 상수 정의의 끝에는 `;`를 붙여줘야한다.
    - 열거형의 인스턴스 변수는 반드시` final`이 있어야 한다는 제약이 있는 것은 아니지만, value는 열거형 **상수**의 값을 저장하기 위한 것이므로 일반적으로 `final`을 붙인다.
    - 열거형의 생성자는 제어자가 묵시적으로 `private`이다.

  ```java
  class Direction {
      // 열거형 상수를 정의하고
      EAST(3), WEST(9), SOUTH(6), NORTH(12);
      
      // 인스턴스변수와 생성자를 추가한다.
      private final int value;
      
      // 생성자의 제어자는 묵시적으로 private이다.
      Direction(int value) {
          this.value = value;
      }
      
      // 외부에서 값을 얻을 수 있는 메서드도 추가한다.
      public int getValue() { return value; }
  }
  ```

  - 필요에 따라 열거형 상수에 복수의 값일 지정할 수도 있다.
    - 이에 맞게 인스턴스 변수와 생성사를 생성해야 한다.

  ```java
  class Direction {
      // 열거형 상수를 정의하고
      EAST(3, "e"), WEST(9, "w"), SOUTH(6, "s"), NORTH(12, "n");
      
      private final int value;
      private final char acronym;
      
      Direction(int value, char acronym) {
          this.value = value;
          this.acronym = acronym;
      }
      
      public int getValue() { return value; }
      
      public char getAcronym { return acronym; }
  }
  ```



- 열거형에 추상 메서드 추가하기

  - 아래 열거형 `Trasportation`은 운송 수단의 종류별로 상수를 정의하고 있으며, 각 운송 수단에는 기본 요금이 책정되어 있다.

  ```java
  enum Transportation {
      BUS(100), TRAIN(150), SHIP(100);
      
      private final int BASIC_FARE;
      
      private Transportation(int basicFare) {
          BASIC_FARE = basicFare;
      }
      
      // 운송 요금을 반환
      int fare() {
          return BASIC_FARE
      }
  }
  ```

  - 이 때, 거리에 따라 추가 요금을 계산하는 방식이 각 운송 수단마다 다르다고 가정해보자.
    - 이럴 때, 열거형에 추상 메서드를 선언하면 각 열거형 상수가 이 추상 메서드를 반드시 구현해야 한다.

  ```java
  enum Transportation {
      BUS(100) { int fare(int distnace) { return distance * BASIC_FARE * 1.2; }}
      TRAIN(150) { int fare(int distance) { return distnace * BASIC_FARE; }}
      SHIP(100) { int fare(int distance) { return distance * BASIC_FARE * 1.3; }}
      
      // 거리에 따른 요금을 계산하는 추상 메서드
      abstract int fare(int distance);
      
      // 제어자를 protected로 설정하여 각 상수에서 접근 가능하도록한다.
      protected final int BASIC_FARE;
      
      Transportation(int basciFare) {
          BASIC_FARE = basciFare
      }
      
      public int getBasicFare() { return BASIC_FARE; }
  }



- 열거형의 내부 구현

  - 아래와 같은 열거형이 있다고 가정해보자.

  ```java
  enum Direction { EAST, WEST, SOUTH, NORTH }
  ```

  - 이 때 열거형 상수 하나하나가 `Direction`객체이다.
    - 위 enum 클래스를 일반 클래스로 정의하면 아래와 같을 것이다.
    - `Direction` 클래스의 static 상수 `EAST`, `WEST`, `SOUTH`, `NORTH`의 값은 객체의 주소이고, 이 값은 바뀌지 않는 값이므로 `==`로 비교가 가능한 것이다.

  ```java
  class Direction {
      static final Direction EAST = new Direction("EAST");
      static final Direction WEST = new Direction("WEST");
      static final Direction SOUTH = new Direction("SOUTH");
      static final Direction NORTH = new Direction("NORTH");
      
      private String name;
      
      private Direction(String name) {
          this.name = name;
      }
  }
  ```

  - 모든 열거형의 조상 클래스인 추상 클래스 `Enum`을 간략화하면 아래와 같다.
    - `MyEnum<T extends MyEnum<T>>`와 같이 선언한 이유는 `MyEnum<T>`와 같이 선언할 경우, 타입 `T`에 `ordinal()`이 정의되어 있는지 확인할 수 없기에 `compareTo()`를 아래와 같이 간단하게 작성할 수 없기 때문이다.
    - 타입 `T`가 `MyEnum`의 자손이므로 `ordinal()`이 정의되어 있는 것이 분명하므로 형변환 없이도 에러가 나지 않는다. 

  ```java
  abstract class MyEnum<T extends MyEnum<T>> implements Comparable<T> {
      static int id = 0;
      
      int ordinal;
      String name = "";
      
      public int ordinal() { return ordinal; }
      
      MyEnum(String name) {
          this.name = name;
          ordinal = id++;		// 객체를 생성할 때마다 증가시킨다.
      }
      
      public int compareTo(T t) {
          return ordinal - t.ordinal();
      }
  }
  ```

  - 위에서 작성한 `MyEnum`을 상속받도록 다시 `Direction`를  작성하면 아래와 같다.
    - 추상 메서드를 추가하면 클래스 앞에도 abstact를 붙여야 하고, 각 static 상수도 추상 메서드를 구현해야한다.
    - 익명 클래스 형태로 추상 메서드를 구현한다.

  ```java
  abstract class Direction extends MyEnum {
      static final Direction EAST = new Direction("EAST") {
          // 익명클래스
          Point move(Point p) { /* 생략 */ }
      }
      static final Direction WEST = new Direction("EAST") {
          // 익명클래스
          Point move(Point p) { /* 생략 */ }
      }
      static final Direction SOUTH = new Direction("EAST") {
          // 익명클래스
          Point move(Point p) { /* 생략 */ }
      }
      static final Direction NORTH = new Direction("EAST") {
          // 익명클래스
          Point move(Point p) { /* 생략 */ }
      }
      
      private String name;
      
      private Driection(String name) {
          this.name = name;
      }
      
      abstract Point move(Point p);
  }
  ```






# 스레드

- 프로세스와 스레드

  - 프로세스(process)란 실행 중인 프로그램(program)이다.

    - 프로그램을 실행하면 OS로부터 필요한 자원을 할당 받아 프로세스가 된다.

    - 프로세스는 프로그램을 수행하는 데 필요한 데이터와 메모리 등의 자원 그리고 스레드로 구성된다.

  - 프로세스의 자원을 이용해서 실제 작업을 수행하는 것이 바로 스레드이다.

    - 모든 프로세스에는 하나 이상의 스레드가 존재한다.
    - 둘 이상의 스레드를 가진 프로세스를 멀티스레드 프로세스라고 한다.
    - 하나의 프로세스가 가질 수 있는 스레드의 개수는 제한되어 있지 않으나 스레드가 작업을 수행하는 데 개별적인 메모리 공간(call stack)을 필요로 하기 때문에 프로세스의 메모리 한계에 따라 생성할 수 있는 스레드의 수가 결정된다.
    - 실제로는 프로세스의 메모리 한계에 도달할 정도로 많은 스레드를 생성하는 일은 거의 없다.
    - 스레드를 가벼운 프로세스라는 의미로 경량 프로세스(LWP, light-weight process)라고 부르기도 한다.



- 멀티태스킹과 멀티스레딩
  - 현대의 OS는 대부분 멀티태스킹(multi-tasking, 다중작업)을 지원하기 때문에 여러 개의 프로세스가 동시에 실행될 수 있다.
  - 이와 마찬가지로 멀티스레딩은 하나의 프로세스 내에서 여러 스레드가 동시에 작업을 수행하는 것이다.
    - CPU의 코어가 한 번에 단 하나의 작업만 수행할 수 있으므로. 실제로 동시에 처리되는 작업의 개수는 코어의 개수와 일치한다.
    - 그러나 실제로 처리해야 하는 스레드의 수는 코어의 개수보다 훨씬 많기 때문에 각 코어가ㅏ 아주 짧은 시간 동안 여러 작업을 번갈아 가며 수행함으로써 여러 작업들이 모두 동시에 수행되는 것처럼 보이게 한다.
    - 따라서 프로세스의 성능이 단순히 스레드의 개수에 비례하는 것은 아니며, 하나의 스레드를 가진 프로세스 보다 두 개의 스레드를 가진 프로세스가 오히려 더 낮은 성능을 보일 수 있다.
  - 멀티스레딩의 장점
    - CPU 사용률을 향상시킨다.
    - 자원을 보다 효율적으로 사용할 수 있다.
    - 사용자에 대한 응답성이 향상된다.
    - 작업이 분리되어 코드가 간결해진다.
  - 멀티스레딩의 단점
    - 멀티스레드 프로세스는 여러 스레드가 같은 프로세스 내에서 자원을 공유하면서 작업을 하기 때문에 아래와 같은 문제가 발생할 수 있으므로, 이를 고려해서 신중히 프로그래밍해야 한다.
    - 동기화(synchronization)
    - 교착상태(deadlock)





## 스레드의 동기화

- 동기화(synchronization)

  - 멀티스레드의 문제점
    - 멀티스레드의 경우 여러 스레드가 같은 프로세스 내의 자원을 공유해서 작업하기 때문에 서로의 작업에 영향을 주게 된다.
    - 만일 스레드 A가 작업하던 도중 다른 스레드 B에게 제어권이 넘어갔을 때, A가 작업하던 공유 데이터를 B가 임의로 변경했다면, 다시 A가 제어권을 받아서 나머지 작업을 마쳤을 때 의도와 다른 결과를 얻을 수 있다.
    - 이를 방지하기 위해 한 스레드가 특정 작업을 완료하기 전까지 다른 스레드에 의해 방해받지 않도록 하는 것이 필요하다.

  - 멀티스레드가 문제가 되는 경우
    - `withdraw`메서드는 `balance`가 출금하려는 금액 보다 클 경우에만 출금하도록 되어 있다.
    - 그러나 아래 예시를 실행하면, `balance`가 음수가 되는 것을 확인할 수 있다.
    - 이는 한 스레드가 if문의 조건식을 통과하고 출금하기 바로 직전에 다른 스레드가 끼어들어 먼저 출금을 했기 때문이다.

  ```java
  class ThreadEx {
      public static void main(String args[]) {
          Runnable r = new RunnableEx();
      }
      
      class Account {
          private int balance = 1000;
          
          public int getBalance() {
              return balance;
          }
          
          public void withdraw(int money) {
              if (balance >= money) {
                  try {
                      Thread.sleep(1000);
                  } catch (InterrupedException e) {}
                  balance -= money;
              }
          }
      }
      
      class RunnableEx implements Runnable {
          Account acc = new Account();
          
          public void run() {
              while (acc.getBalance > 0 ) {
                  int money = (int) (Math.random() * 3 + 1) * 100;
                  acc.withdraw(money);
                  System.out.println("balance:"+acc.getBalance());
              }
          }
      }
  }
  ```

  - 임계 영역(critical section)과 잠금(lock)
    - 공유 데이터를 사용하는 코드 영역을 임계 영역으로 지정하놓고, 공유 데이터(객체)가 가지고 있는 lock을 획득한 단 하나의 스레드만 임계 영역 내의 코드를 수행할 수 있게 한다.
    - 그리고 해당 스레드가 임계 영역을 벗어나면 lock을 반납해 다른 스레드가 반납된 lock을 획득하여 임계 영역의 코드를 수행한다.
  - 이처럼 한 스레드가 진행 중인 작업을 다른 스레드가 간섭하지 못하도록 막는 것을 동기화라고 한다.
    - Java에서는 `synchronized` 블럭을 이용해 스레드의 동기화를 지원했다.
    - JDK 1.5부터는 `java.util.concurrent.locks`와 `java.util.concurrent.atomic` 패키지를 통해 다양한 방식으로 동기화를 구현할 수 있게 됐다.



- `synchronized`를 이용한 동기화

  - `synchronized`는 임계 영역을 설정하는 키워드이다.
    - 아래와 같이 메서드 전체를 임계 영역으로 설정하는 방법과, 특정한 영역을 임계 영역으로 설정하는 방법이 있다.
    - 두 방법 모두 lock의 획득과 반납이 자동으로 이루어지므로, 개발자는 `synchronized` 키워드로 임계 영역만 설정해주면 된다.

  ```java
  // 메서드 전체를 임계 영역으로
  public synchronized void calcSum() {
      // ...
  }
  
  // 특정한 영역을 임계 영역으로
  synchronized (객체의 참조변수) {
      // ...
  } 
  ```

  - 모든 객체는 lock을 하나씩 가지고 있다.
    - 해당 객체의 lock을 가지고 있는 스레드만 임계 영역의 코드를 수행할 수 있다.
    - 다른 스레드들은 lock을 얻을 때까지 기다리게 된다.
  - 임계 영역은 멀티스레드 프로그램의 성능을 좌우한다.
    - 따라서 가능한 메서드 전체에 lock을 거는 것 보다 임계 여역을 최소화해서 보다 효율적인 프로그램이 되도록 해야 한다.
  - 위에서 살펴본 출금 예시에서 발생한 문제는 `withdraw`메서드에 `synchronized`를 사용하여 해결할 수 있다.
    - 이제 `withdraw` 메서드가 종료되어 lock이 반납될 때까지 다른 스레드는 `withdraw`를 호출하더라도 대기 상태에 머물게 된다.
    - 주의할 점은 `balance`의 접근저에자가 private이라는 것이다.
    - 만일 private이 아니면, 외부에서 직접 접근할 수 있기 때문에 아무리 동기화를 해도 이 값의 변경을 막을 방법이 없다.

  ```java
  public synchronized void withdraw(int money) {
      if (balance >= money) {
          try {
              Thread.sleep(1000);
          } catch (InterrupedException e) {}
          balance -= money;
      }
  }
  ```

  - 혹은 아래와 같이 `synchronized` 블럭을 설정해도 된다.

  ```java
  public void withdraw(int money) {
      synchronized(this) {
          if (balance >= money) {
              try {
                  Thread.sleep(1000);
              } catch (InterrupedException e) {}
              balance -= money;
          }
      }
  }
  ```

  
