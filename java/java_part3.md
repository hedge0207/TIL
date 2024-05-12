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

  