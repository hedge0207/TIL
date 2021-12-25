 # 목차

- [JAVA 기초](#JAVA-기초)

  - [객체지향 프로그래밍](#객체지향-프로그래밍)
  - [Hello World](#Hello-World)
  - [변수](#변수)
  - [자료형](#자료형)
  - [연산자](#연산자)

- [제어문](#제어문)

  - [조건문](#조건문)

  - [반복문](#반복문)





# JAVA 기초

## 객체지향 프로그래밍

- 객체 지향 프로그래밍
  - 정의
    - 프로그램을 구성하는 요소는 객체이며 이것이 상호작용하도록 프로그래밍 하는 것.
    - 실세계의 개체를 속성(자료)과 메서드(프로세서)가 결합한 형태의 객체로 표현하는 개념.
  - 객체 지향 프로그래밍은 컴퓨터 프로그램을 명령어의 목록으로 보는 시각에서 벗어나 여러 개의 독립된 단위, 즉 "객체"들의 모임으로 파악하고자 하는 것이다. 각각의 객체는 메세지를 주고 받고 데이터를 처리할 수 있다. 즉 객체를 블럭으로 하여 프로그래밍을 블럭 조립하듯이 할 수 있게 된다.
  - 객체 지향 프로그래밍은 프로그램을 유연하고 변경이 용이하게 만들기 때문에 대규모 소프트웨어 개발에 많이 사용된다.



- 객체 지향 구성 요소
  - 클래스(Class)
    - 같은 종류의 집단에 속하는 속성과 행위를 정의
    - 속성은 변수의 형태로, 행위는 메서드 형태로 선언
  - 객체(Object)
    - 객체의 행위(메서드)는 클래스에 정의된 행위에 대한 정의를 공유함으로써 메모리를 경제적으로 사용
    - 객체마다 각각의 상태와 식별성을 가진다.
  - 메서드(Method)
    - 전통적 시스템의 함수 또는 프로시저에 해당하는 연산 기능
  - 메시지(Message)
    - 객체에게 어떤 행위를 하도록 지시하기 위한 방법
  - 인스턴스(Instance)
    - 객체지향 기법에서 클래스에 속한 각각의 객체
    - 실제로 메모리상에 할당된다.
  - 속성(Property)
    - 한 클래스 내에 속한 객체들이 가지고 있는 데이터 값들을 단위별로 정의.
    - 성질, 분류, 식별, 수량, 현재 상태 등에 대한 표현 값.



- 객체 지향 기법
  - 캡슐화
    - 서로 관련성이 높은 데이터들과 이들을 처리하는 함수들을 한 묶음으로 처리하는 기법.
    - 결합도가 낮아지고 재사용이 용이해진다.
    - 변경 발생 시 오류의 파급 효과가 적다.
    - 인터페이스가 단순화 된다.
  - 상속성
    - 상위 클래스의 속성과 메서드를 하위 클래스에서 재정의 없이 물려 받아 사용하는 기법
  - 다형성
    - 하나의 메시지에 대해 각 객체가 가지고 있는 고유한 방법으로 응답할 수 있는 능력
    - 오버로딩, 오버라이딩이 대표적.
  - 추상화
    - 공통 성질을 추출하여 추상 클래스를 설정하는 기법
    - 기능 추상화, 자료 추상화, 제어 추상화
  - 정보 은닉
    - 코드 내부 데이터와 메서드를 숨기고 공개 인터페이스를 통해서만 접근이 가능하도록 하는 코드 보안 기술
    - 사이드 이펙트를 최소화하기 위해 사용



- 다형성(Polymorphism)
  - 하나의 객체가 여러개의 자료형 타입을 가질 수 있는 것
  - 역할과 구현
    - 역할과 구현이 있다고 할 때 자동차는 역할, K3, 아반떼 등은 구현이라고 할 수 있다. 이 때 운전자(클라이언트)는 K3를 타다가 아반떼를 타도 운전을 잘 할 수 있듯이 구현체가 바뀌어도 역할이 동일하면 해당 역할을 수행할 수 있다.
    - 따라서 자동차의 구현체는 자동차라는 역할에만 충실하면, 운전자에게 영향을 주지 않고 무한히 확장이 가능하다.
    - 핵심은 자동차라는 역할에서 벗어나지만 않으면 새로운 자동차가 출시되어도 운전자는 새로 운전을 배울 필요가 없다는 점이다. 즉, 서버가 변경되어도 클라이언트는 변경을 하지 않아도 된다는 점이다.
    - 따라서 위와 같이 역할과 구현으로 세상을 구분하면 보다 단순하고 유연해지며, 변경도 편리해진다.
    - 운전자는 자동차의 역할만 이해하고 있으면 자동차의 구현체들의 내부 구조를 몰라도 되며 구현체의 내부 구조가 변경되어도 영향을 받지 않는다.
    - 자바에서 역할은 인터페이스, 구현은 클래스, 객체에 해당 된다.
  - 자바의 다형성
    - 자바에서의 다형성은 오버라이딩에서 찾을 수 있다.
    - 오버라이딩이 가능하게 하는 것이 다형성이다.
  - 다형성의 본질
    - 인터페이스를 구현한 객체인스턴스를 실행하는 시점에서 유연하게 변경할 수 있다.
    - 클라이언트(운전자)를 변경하지 않고, 서버의 구현 기능을 유연하게 변경할 수 있다.



## Hello World

- JAVA의 실행 순서: 코드 작성-컴파일(작성한 코드를 실행 가능한 파일로 변환)-코드 실행
  - 우리가 작성한 코드는 `.java`라는 확장자명을 가지고 있다.
  - 컴파일러는 컴파일 과정을 거쳐 우리가 작성한 `.java` 파일을 `.class` 파일로 변환시킨다.
    - 컴파일: 프로그래머가 작성한 소스코드를 컴퓨터가 이해할 수 있는 말(기계어)로 바꾸는 행위
    - javac는 java complier의 약자다.
    - 컴파일 된 클래스 파일은 Java VM(Java Virtual Machine)이 인식할 수 있는 바이너리 파일이다.
  - Java VM은 클래스 파일의 바이너리 코드를 해석하여 프로그램을 수행(`.class` 파일이 실행)한다.
    - 정확히는 class 내의 `main` 메서드를 실행시킨다.
  - 마지막 단계로 우리가 짠 코드의 수행 결과가 컴퓨터에 반영된다.



- Java의 기본 구조

  - `package`: 자바 클래스가 위치하고 있는 디렉토리명과 일치한다.
  - `public`:  자바 프로그래밍 시 중요하게 사용되는 접근제어자로 class 명 앞에 사용 될 경우에는 조금 다른 의미로 사용된다.
    - 소스파일(`.java`)의 이름은 public class의 이름과 일치해야 한다.
    - 만일 소스파일 내에 public class가 없다면, 소스파일의 이름은 소스파일 내의 어떤 클래스의 이름으로 해도 상관 없다.

  - `main` 메소드
    - main 메소드는 반드시 필요하다. main 메소드는 프로그램 실행 시 파라미터를 입력으로 받을 수 있는데 입력 받은 파라미터는 메소드의 입력 파라미터`String[] args`에 저장된다.
    - `public`: 메소드의 접근제어자로, 누구나 이 메소드에 접근할 수 있다는 의미다.
    - `static`: 메소드에 static이 지정되어 있는 경우 이 메소드는 인스턴스 생성 없이 실행 할 수 있음을 의미
    - `void`: 메소드의 리턴 값이 없음을 의미한다.
    - `String`: 문자열
    - `args`: string 자료형에 대한 변수명으로 String 뒤에 []가 있으므로 한 개가 아닌 여러 개의 값으로 이루어진 배열임을 의미
    - `System.out.println`: 표준출력으로 데이터를 보내는 자바의 내장 메소드로 println 메소드로 들어오는 문자열 값을 화면에 출력한다.

  ```java
  //HelloWorld.java 파일
  
  package first;
  
  public class HelloWorld {
  
  	public static void main(String[] args) {
  		System.out.println("Hello World");
  	}
  }
  ```

  - 모든 코드의 끝에는 `;`을 붙여야 한다.




- `eclipse`
  - `eclipse`에서는 저장할 때마다 컴파일이 이루어진다.
  - `file`-`new`-`other`-`Java Project`를 통해 프로젝트 생성
  - `src`우클릭-`new`-`class`를 통해 새로운 파일 생성(`public static void main~`체크)



- syso까지 입력하고 `ctrl+spacebar`를 누르면 `System.out.println()`가 자동완성 된다.

​	

- 주석 다는 방법
  - 행 단위 주석: `//`
  - 블럭 단위 주석: `/* */`
  - 문서화 주석: `/** * */`를 사용, python과 마찬가지로 `ctrl+/`로 주석 처리 가능
  
  ```java
  //행 단위 주석
  
  /*
  블럭
  단위
  주석
  */
  
  /**
  *문서화
  *주석
  */
  ```







## 변수

- 변수: 값을 저장할 수 있는 메모리 공간



- 자바는 강형 언어다.
  - 강형언어:모든 변수의 타입이 컴파일 시에 결정되는 언어로 자료형에 대한 오류를 컴파일 시 검출 가능하다.
  - 따라서 자바는 처음 변수를 선언 할 때부터 어떤 값을 넣을 지 정해야하며 선언된 변수에 알맞은 값을 넣어야 한다.



- 변수명을 정하는 규칙
  - 변수명은 숫자로 시작할 수 없다.
  - `_`(underscore)와 `$`문자 이외의 특수문자는 사용할 수 없다.
  - 자바의 키워드는 변수명으로 사용할 수 없다.
  - 변수명은 **lowerCamelCase** 로 작성한다(네이밍 문법으로 지키지 않아도 에러가 발생하지는 않는다).



- 변수의 선언과 대입

  - `자료형 변수명`의 형태로 선언한다.

  ```java
  int a;
  ```

  - 선언한 후의 대입에는 자료형을 붙이지 않는다. 

  ```java
  a = 3
  ```

  - 선언과 대입을 동시에 할 수 있다.

  ```java
  int b = 1;
  ```



- 상수: 데이터를 담을 수 있는 공간이라는 것은 변수와 유사하지만 변수와 달리 대입한 값을 변화시킬 수 없다.

  - 원주율 등의 변하지 않는 값을 저장하여 사용하기 위해 사용한다.
  - `final 자료형 상수명`으로 선언한다.
  - 상수명은 모두 대문자로 구성된 명사로 작성한다. 단어와 단어 사이를 `_`로 구분하여 작성한다.

  ```java
  final double PI;
  PI = 3.141592;
  
  //아래와 같은 재대입은 불가
  //A = 3.14;
  
  //단어와 단어 사이를 _로 구분하여 작성
  final int AVG_PRICE;
  AVG_PRICE=150;
  ```



- `final`키워드
  - final은 해당 entity가 오로지 한 번 할당될 수 있음을 의미한다.
  - final 변수
    - 해당 변수가 생성자나 대입연산자를 통해 한 번만 초기화 가능함을 의미.
    - 이를 활용하여 상수를 선언할 때 사용.
  - final 메소드
    - 해당 메소드를 오버라이드하거나 숨길 수 없음을 의미.
  - final 클래스
    - 해당 클래스는 상속할 수 없음을 의미. 
    - 문자 그대로 상속 계층 구조에서 ‘마지막’ 클래스이다.



## 자료형

- 기본형(primitive)과 참조형(reference)

  - 기본형(원시 자료형)
    - 숫자(정수형, 실수형), 문자형,논리형
    - 클래스가 아니다.
    - 원시 자료형은 리터럴로 값을 세팅할 수 있다. 리터럴이란 계산식 없이 소스코드에 표기하는 상수 값을 의미한다.
    -  원시 자료형은 `new` 키워드로 생성할 수 없다.
    - String은 원시 자료형은 아니지만 리터럴 표현식을 사용할 수 있도록 자바에서 특별 대우 해주는 자료형이다.
  - 참조형
    - 기본형 타입을 제외한 모든 타입, 문자열 등

  ```java
  //예를 들어 아래와 같이 기본형 int 변수와 참조형 String 변수가 있을 경우
  
  //리터럴 표현식
  int num = 1;
  
  //new를 사용한 객체 생성 방식
  //String 역시 위와 마찬가지로 리터럴 표현식으로 생성할 수 있도록 Java에서 허용하고 있으나 참조형이라는 것을 강조하기 위해 여기서는 아래와 같이 객체 생성 방식으로 선언
  String str = new String "asd";
      
      
  //기본 자료형인 int형인 변수 num의 경우 1이라는 값을 저장하고 있다.
  //그러나 참조형인 String 형인 변수 str의 경우 asd를 저장하고 있는 것이 아니라 asd를 저장하고 있는 String 객체를 참조하고 있는 것이다. 정확히는 str에 참조하는 String 객체의 주소값이 저장되어 있다.
  ```



- 숫자
  - 정수형(크기순)
    - long(8byte), int(4byte),  short(2byte), byte 등의 키워드가 있으며 int가 가장 많이 쓰인다. Long을 쓰고자 할 경우 그냥 int를 쓰듯 1,2,3 과 같이 써선 안되고 1L, 2L, 3L과 같이 써야 한다.
    - int는 -2147483648 ~ 2147483647를 표현 할 수 있다.
    - 8진수, 16진수는 int 자료형으로 표현한다.
    - long은 -9223372036854775808 ~ 9223372036854775807를 표현 할 수 있다.
    - long 변수에 값을 대입할 때는 대입하는 숫자 값이 int 자료형의 최대값인 2147483647 보다 큰 경우 `L` 또는 `l(소문자 L)`을 붙여주어야 한다.  단, 소문자 l의 경우 1과 혼동될 수  있으므로 가급적 대문자로 적는다.
  - 실수형
    - double(8byte)과 float(4byte)으로 나뉜다. 
    - 디폴트는 double이므로 float 변수에 값을 대입할 때에는 접미사 `F`, 또는 `f`를 붙여 줘야 한다.
    - 파이썬과 마찬가지로 **과학적 지수 표현식**으로도 표현이 가능하다(ex.1.234e2).
    - 정수보다 실수의 크기가 더 크다. 즉 수를 다루는 타입의 크기는 다음과 같다.
    - byte < char = short <  int < long < float < double
    - 실수는 소수점 뒤의 자릿수들을 담을 공간이 필요하기에 정수보다 크다.



- 논리형(boolean, 1byte의 크기를 가진다)
  - true나 false중 하나의 값을 가진다.



- 문자

  - char(문자): 2byte의 크기를 가진다, 쓸 일이 거의 없다.

    - 작은 따옴표('')를 사용하여 한 글자를 표현
    - 문자값, 아스키코드 값, 유니코드 값으로 모두 표현이 가능하다.

    ```java
    package first;
    
    public class HelloWorld {
    
    	public static void main(String[] args) {
    		char a1 = 'a';       //문자값
    		char a2 = 97;        //아스키코드 값
    		char a3 = '\u0061';  //유니코드 값
    		System.out.println(a1);  //a
    		System.out.println(a2);  //a
    		System.out.println(a3);  //a
    	}
    }
    ```

    

  - String(문자열): 문장을 표현, 한 글자도 포함된다.

    - 큰 따옴표를 사용하여 묶어야 하며 작은 따옴표 사용시 error가 발생한다.
    - 아래와 같은 두 가지 방식으로 표현이 가능하다.
    - `new` 키워드는 객체를 만들 때 사용하는 것으로 일반적으로는 `new`를 쓰지 않는 첫 번째 방법을 사용

    ```java
    package first;
    
    public class HelloWorld {
    
    	public static void main(String[] args) {
            //String은 원시 자료형은 아니지만 리터럴 표현식을 사용할 수 있도록 자바에서 특별 대우해주기에 아래와 같이 리터럴 표현식으로 쓸 수 있다. 이 경우 변수는 문자열 자체가 저장되어 있다.
    		String a = "Hi";
    		String b = "My name is";
    		String c = "Java";
            
            //방법2. new 사용 방법, String은 기본적으로 클래스이므로 아래와 같이 객체를 생성하는 키워드인 new를 사용 가능하다. 이 경우 변수에는 문자열 자체가 아닌 문자열 객체를 가리키는 주소가 저장되어 있다.
    		String a2 = new String("Hi");
    		String b2 = new String("My name is");
    		String c2 = new String("Java");
    		System.out.println(a);
    		System.out.println(b);
    		System.out.println(c);
    		System.out.println(a2);
    		System.out.println(b2);
    		System.out.println(c2);
    	}
    }
    ```

  - String 자료형과 관련된 메소드들

    ```java
    //1. equals: 두 개의 문자열이 동일한 값을 가지고 있는지 비교하여 true, false 값을 리턴
    //==연산자를 사용할 경우 리터럴 방식으로 생성한 변수와 new를 사용하여 생성한 변수를 비교할 때 같은 값이더라도 false를 반환하는데 이는 == 연산자가 값이 동일한지 여부를 판별하는 것이 아닌 같은 객체인지를 판별하는 것이기 때문이다.
    package first;
    
    public class HelloWorld {
    
    	public static void main(String[] args) {
            // 리터럴 표기법
    		String a = "My name is";
    		String b = "My name is";
    		String c = "My name Is";
            
            // 생성자 방식
            // part2에 적혀 있듯 new 키워드 자체가 생성자가 아니다. 
            // 클래스명과 메소드명이 동일하고 리턴 자료형이 없는 메소드를 생성자라고 한다.
            // 생성자는 객체가 생성될 때 호출되고 객체가 생성될 때는 new라는 키워드로 객체가 만들어질 때이다.
    		String d = new String("My name is");
            String e = new String("My name is");
    		System.out.println(a.equals(b));   //true
            
            //둘이 같다고 나오는 이유는 객체를 생성하는 방식이 아닌 리터럴을 저장하는 방식이기 때문이다.
            System.out.println(a==b);          //true
            
            //c에 Is라고 썼으므로 다르다고 나온다.
    		System.out.println(a.equals(c));   //false
            
            //equals는 값이 같은지를 판단하기에 true가 출력
            System.out.println(a.equals(d));   //true
            
            //==는 같은 객체인지를 판단하기에 false가 출력
    		System.out.println(a==d);          //false
            
            //d와 e도 마찬가지로 값은 같지만서로 다른 객체를 지칭하고 있으므로 다르다고 출력된다.
            System.out.println(d==e);          //false
    	}
    }
    
    //2.indexOf: 문자열에서 특정 문자가 시작되는 인덱스를 리턴한다. 없을 경우 -1을 리턴한다.
    package first;
    
    public class HelloWorld {
    
    	public static void main(String[] args) {
    		String a = "My name is";
    		System.out.println(a.indexOf("e"));     //6
            System.out.println(a.indexOf("name"));  //3
    		System.out.println(a.indexOf("qwer"));  //-1
    	}
    }
    
    //3.replaceAll: 특정 문자를 다른 문자로 바꾸고 싶을 경우 사용
    package first;
    
    public class HelloWorld {
    
    	public static void main(String[] args) {
    		String a = "My name is";
    		System.out.println(a.replaceAll("My","His"));  //His name is
    	}
    }
    
    //4.substring: 문자열 중 특정 부분을 뽑아낼 경우에 사용
    package first;
    
    public class HelloWorld {
    
    	public static void main(String[] args) {
    		String a = "My name is";
    		System.out.println(a.substring(1,4)); //y n
    	}
    }
    
    //5.toUpper(Lower)Case: 문자열을 모두 대(소)문자로 변경
    package first;
    
    public class HelloWorld {
    
    	public static void main(String[] args) {
    		String a = "My name is";
    		System.out.println(a.toUpperCase());  //MY NAME IS
    		System.out.println(a.toLowerCase());  //my name is
    	}
    }
    
    //6.concat: 문자열과 문자열을 결합
    package first;
    
    public class HelloWorld {
    
    public static void main(String[] args) {
    		String a = "My";
    		System.out.println(a.concat(" name is")); //My name is
            System.out.println(a) //My, 값이 변경되는 것은 아니다.
                
            //아래와 같이 하면 변경시킬 수 있다.
            a = a.concat(" name is")
            System.out.println(a)  //My name is
    	}
    }
    
    //7.charAt(숫자): 인덱스에 해당하는 문자를 반환
    package first;
    
    public class HelloWorld {
    
    public static void main(String[] args) {
    		String a = "My";
            System.out.println(a.charAt(1))  //M
    	}
    }
    ```
  
  - StringBuffer: 문자열을 추가하거나 변경할 때 주로 사용하는 자료형
  
    - 아래 과정에서 String과 StringBuffer는 완전히 동일해 보이지만 그렇지 않다. 두 변수의 값은 동일하지만 StringBuffer 타입은 객체를 단 한 번만 생성시키는 반면에 String은 +연산을 할 때마다 새로운 객체가 생성된다(따라서 아래 예시에서는 총 4개의 객체가 생성된다). 
    - 이는 String 객체가 값을 변경할 수 없기(immutable)때문으로 위에서 살펴본 `toUpperCase`등도 마찬가지로 기존의 String 객체를 모두 대문자로 변화시키는 것이 아니라  모두 대문자로 변환 된 새로운 객체를 생성하는 것이다. StringBuffer 는 이와 반대로 값을 변경할 수 있다(mutable)
    - StringBuffer 자료형은 String 자료형보다 무거운 편에 속한다. `new StringBuffer()` 로 객체를 생성하는 것은 일반 String을 사용하는 것보다 메모리 사용량도 많고 속도도 느리다. 따라서 문자열 추가나 변경등의 작업이 많을 경우에는 StringBuffer를, 문자열 변경 작업이 거의 없는 경우에는 그냥 String을 사용하는 것이 유리하다.
  
    ```java
    //append를 사용하여 문자열을 추가 가능
    package first;
    
    public class HelloWorld {
    
        public static void main(String[] args) {
            StringBuffer a = new StringBuffer();
            a.append("hello");
            a.append(" ");
            a.append("my name is java.");
            System.out.println(a);  		   //hello my name is java.
            //toString()메소드는 String 자료형으로 변경 해준다.
            System.out.println(a.toString());  //hello my name is java.
            //String으로는 아래와 같이 작성 가능
            String b = "";
            b += "hello";
            b += " ";
            b += "my name is java.";
            System.out.println(b);  		   //hello my name is java.
        }
    }
    
    //insert를 사용하여 특정 위치에 원하는 문자열 삽입 가능
    package first;
    
    public class HelloWorld {
    
        public static void main(String[] args) {
            StringBuffer a = new StringBuffer();
            a.append("my name is java.");
            a.insert(0,"Hello ");  //첫 번째 인자로 인덱스, 두 번째 인자로 삽입할 문자열
            System.out.println(a); //Hello my name is java.
        }
    }
    
    //substring: String자료형의 substring 메소드와 사용법이 동일
    package first;
    
    public class HelloWorld {
    
        public static void main(String[] args) {
            StringBuffer a = new StringBuffer();
            a.append("Hello my name is java.");
            System.out.println(a.substring(0,4)); //Hell
        }
    }
    ```
  
  



- Array(배열)

  - 배열은 자료형 바로 뒤에 `[]`를 사용하여 표현한다.

  ```java
  //방법1
  int[] num = {1,2,3};
  
  //방법2
  int[] num = new int[]{1,2,3};
  
  //방법3
  //이 경우 반드시 배열의 길이를 먼저 정해주어야 한다.
  int[] num = new int[3];  //길이를 정해주지 않을 경우 error가 발생
  num[0]=1;
  num[1]=2;
  num[2]=3;
  
  System.out.println(num); //[I@65b3120a, java에서는 이와 같이 출력을 하면 배열의 내용이 아닌 배열의 주소값이 출력된다.
  
  //내용을 보고자 한다면 아래와 같이 출력해야 한다.
  import java.util.Arrays; //Arrays를 import하고
  
  System.out.println(Arrays.toString(num)); //[1, 2, 3]
      
      
  //만일 선언하고 값을 지정해 주지 않을 경우 아래와 같이 null값이 들어가게 된다.
  //이는 자료형마다 기본값이 다른데 String은 null, int는 0, double은 0.0, boolean은 false가 기본값으로 들어가게 된다. 
  String[] arr = new String[3];
  arr[0]="a";
  arr[1]="b";
  System.out.println(Arrays.toString(arr));  //[a, b, null]
  ```

  - 인덱싱

  ```java
  //파이썬과 동일하게 대괄호를 사용
  String[] weeks = {"월","화","수"};
  System.out.println(weeks[1]);  //화
  ```

  - 배열의 길이

  ```java
  //.length를 사용하여 길이를 알 수 있다.
  String[] weeks = {"월","화","수"};
  System.out.println(weeks.length);  //3
  ```

  - `ArrayIndexOutOfBoundsException`에러는 파이썬의 `index out of range`와 동일한 에러다.

  -  2차원 배열 

  ```java
  //기본 구조
  package first;
  
  public class HelloWorld {
  
  	public static void main(String[] args) {
  		자료형[][] 변수명 = new 자료형[행크기][열크기];
  	}
  }
  
  //아래와 같이 행 별로 다른 크기의 배열을 생성할 수도 있다.
  int[][] arr = new int[3][];
  arr[0]=new int[1];
  arr[1]=new int[2];
  arr[2]=new int[3];
  System.out.println(Arrays.toString(arr[0]));  //[0]
  System.out.println(Arrays.toString(arr[1]));  //[0,0]
  System.out.println(Arrays.toString(arr[2]));  //[0,0,0]
  ```





- 리스트

  - 배열과 유사하지만 배열보다 편리한 기능을 많이 가지고 있다.
  - 배열과 달리 생성시에 길이를 미리 정하지 않아도 된다.
  - import해서 사용해야 한다.
  - 래퍼 클래스(wrapper class)
    - 기본 자료타입(primitive type)을 객체로 다루기 위해서 사용하는 클래스들을 래퍼 클래스(wrapper class)라고 한다.
    - ArrayList는 Array와 달리 오직 Object만 담을 수 있다(기본형을 담을 수 없다)
  - 그러나 담기는 것 처럼 보이는데(아래 예시에서도 int 타입이 담기는 것 처럼 보인다) 이는 사실 원시형이 아닌 래퍼 클래스(wrapper class)를 담는 것이다.
  - 제네릭스
    - `<>`안에 자료형을 입력한 ArrayList를 제네릭스라고 부르며  좀 더 명확한 타입체크를 위해 사용한다. 고급 주제이므로  구체적인 내용은 적지 않는다.
    - `<>`안에는 제네릭 타입을 입력하는데 생략하면 Object타입이 된다(이는 모든 객체가 상속하고 있는 가장 기본적인 자료형이 Object이기 때문이다). Object는 모든 데이터 타입을 저장 가능하지만 데이터를 추가하거나 검색할 때 형 변환을 해야 한다. 자료구조에는 주로 동일한 데이터 타입을 저장하기 때문에 제네릭 타입을 지정하고 사용하는 것이 좋다.
  
  ```java
  package first;
  
  import java.util.ArrayList; //import 해야 한다.
  
  public class HelloWorld {
  
  	public static void main(String[] args) {
          //<>안에는 포함되는 요소(객체)의 자료형을 명확하게 표현하는 것이 권장된다.
          //적지 않아도 에러는 발생하지 않는다.
  		ArrayList<Integer> lotto = new ArrayList<Integer>();
          //1.add: 값을 추가
  		lotto.add(3);
  		lotto.add(6);
  		lotto.add(7);
  		lotto.add(0,9);
          //특정 위치에 값을 추가하고자 할 경우 첫 번째 인자로 인덱스를, 두 번재 인자로 추가할 값을 넣는다.
  		lotto.add(0,9);
  		System.out.println(lotto);  //[9, 3, 6, 7]
          
          // 2.remove: 객체를 제거, 제거할 객체를 입력하는 방법과 인덱스를 입력하는 방법이 있다.
          // 1)객체를 지정하여 제거, 이 경우 성공적으로 제거될 경우 true, 아닐 경우 false를 리턴한다. 
          // 없애고자 하는 객체가 정수 타입일 경우 인덱스로 접근하여 제거하는 방식과 겹치므로 아래와 같이 (Integer)를 붙여줘야 한다.
          System.out.println(lotto.remove((Integer)9));  //true
  		System.out.println(lotto); 					   //[3,6,7]
          //2)인덱스로 접근하여 제거, 이 경우 성공적으로 제거될 경우 제거한 값을, 아닐 경우 error가 출력된다.
          System.out.println(lotto.remove(2)); //7
  		System.out.println(lotto);			 //[3,6]
          
          //3.get: 인덱스에 해당하는 값을 추출
          System.out.println(lotto.get(1)); //6
              
          //4.size: ArrayList의 갯수를 리턴
          System.out.println(lotto.size());  //2
          
          //5.contains: 리스트 내에 특정 값의 존재 유무에 따라 true,false를 리턴
          System.out.println(lotto.contains(3));   //true
          System.out.println(lotto.contains(123)); //false
          
          //6.ArrayList 합치기
          ArrayList<Integer> lotto2 = new ArrayList<Integer>();
        lotto2.add(15);
          lotto.addAll(lotto2)
  	}
  }
  ```
  
  ```java
  //제네릭스를 사용하지 않은 경우의 문제점
  //상기했듯 별도의 자료형을 입력하지 않을 경우 Object 타입이 된다.
  
  package first;
  
  import java.util.ArrayList;
  
  public class HelloWorld {
  
  	public static void main(String[] args) {
          //제네릭스를 사용하지 않은 경우
  		ArrayList aList = new ArrayList();
  		aList.add("hello");
  		aList.add("world");
          
  		//형변환 하지 않을 경우 에러가 발생
          String a = aList.get(0);
  		String b = aList.get(1);
          
          //아래와 같이 형변환을 해줘야 한다.
  		String a = (String) aList.get(0);
  		String b = (String) aList.get(1);
  		System.out.println(a);  //hello
  		System.out.println(b);  //world
  	}
  }
  ```



- 맵(Map)

  - Key와 Value를 가진 자료형으로 파이썬의 딕셔너리에 해당.
  - import를 해서 사용해야 한다.
  - 아래에서 사용한 `HashMap`뿐 아니라 입력된 순서대로 데이터가 출력되는  `LinkedHashMap`과, key의 소트순으로 데이터가 출력되는 `TreeMap`도 있다.
    - Map의 가장 큰 특징은 순서에 의존하지 않고 key로 value를 가져오는데 있다. 하지만 가끔은 Map에 입력된 순서대로 데이터를 가져오고 싶은 경우도 있고 때로는 입력된 key에 의해 소트된 데이터를 가져오고 싶을 수도 있다.
    - 위와 같은 경우 `LinkedHashMap`과 `TreeMap`을 사용하면 된다.

  ```java
  package first;
  
  import java.util.HashMap;
  
  public class HelloWorld {
  
  	public static void main(String[] args) {
  		HashMap<String, String> a = new HashMap<String, String>();
          //put: 입력
  		a.put("이름","자바");
  		a.put("취미","영화감상");
  		a.put("성별","남성");
  		System.out.println(a);  //{이름=자바, 취미=영화감상, 성별=남성}
          
          //remove: 제거 후 key에 해당하는 value 값을 리턴
          System.out.println(a.remove("취미"));  //영화감상
          System.out.println(a);   //{이름=자바, 성별=남성}
          
          //size: Map의 갯수를 출력
          System.out.println(a.size()); //2
          
          //get: key에 해당하는 value를 반환
          System.out.println(a.get("이름")); //자바
          
          //containsKey: 해당 키의 유무에 따라 true,false로 반환
          System.out.println(a.containsKey("성별")); //true
  	}
  }
  ```

  

- 타입 변환

  - 묵시적 형변환과 강제 형변환

  ```java
  //묵시적 형변환
  int x = 50000;
  long y = x;
  //error가 발생하지 않음, 자연스럽게 형 변환이 일어난다.
  
  long x2 = 1;
  int y2 = x2;
  //error가 발생, 1은 int에 들어가기에 충분히 작은 값임에도 본래 long타입으로 선언되었기에 int에 들어가지 못한다.
  
  //강제 형변환
  //아래와 같은 방식으로 형변환이 가능하다.
  int y2 = (int)x2;
  ```

  

- 열거형(`enum`)

  - JDK5에서 추가된 문법, 이전까지는 상수형을 열거형 대신 사용
  - 즉, 어떤 변수가 자유로운 값이 아닌 특정한 값만을 가지기를 원할 때 사용하는 것이 `enum`이다.

  ```java
  //기본형
  enum 변수명{
      값1,값2,...
  }
  ```

  ```java
  package first;
  
  public class Example {
  	//상수형을 선언할 때는 전부 대문자를 사용하는 것이 컨벤션
  	public static final String MALE="MALE";
  	public static final String FEMALE="FEMALE";
  	
      //메인 메소드
      public static void main(String[] args) {
      	//gender1이라는 변수에는 MALE, FEMALE 둘 중의 한 값만 넣고 싶을 경우
      	String gender1;
      	
      	//cf.staitc변수는 아래와 같이 class로 직접 접근이 가능하다(part2 static 참고)
      	gender1 = Example.MALE;    //에러 발생X
      	gender1 = Example.FEMALE;  //에러 발생X
          
      	//위 까지는 원하는 대로 동작하지만 문제는 아래와 같은 경우에도 에러가 출력되지 않는다는 것이다.
      	gender1 = "boy";  //에러 출력X
          
      	//MALE, FEMALE 둘 중 하나만 넣고자 했으나 위와 같은 방식으로는 String이기만 하면 컴파일시 에러로 인식하지 않아 모든 값을 넣을 수 있으므			로 원하는 대로 동작시킬 수 없다.
      	//따라서 enum을 사용한다.
      	Gender gender2;
      	gender2 = Gender.MALE;
      	gender2 = Gender.FEMALE;
      	gender2 = Gender.boy; //에러 발생
      }  
  }
  //class 밖에 정의한다.
  enum Gender{
  	MALE,FEMALE;
  }
  ```

  

## 연산자

- 연산과 연산자, 연산식
  - 연산: 데이터를 처리하여 결과를 산출하는 것
  - 연산자: 연산에 사용되는 표시나 기호
  - 피연산자: 연산 대상이 되는 데이터
  - 연산식: 연산자와 피연산자를 이용하여 연산의 과정을 기술한 것



- 부호연산
  - 파이썬과 동일하게 `+`, `-`가 사용된다.



- 사칙연산

  - 대부분 파이썬과 유사하다.

  - `/`는  파이썬과 달리 나눈 값을 반환하거나 몫을 반환하는데 쓰인다.

    - 둘 중 하나라도 실수(float, double)면 실수값을 반환하지만 둘 다 정수면 몫을 반환한다.
  - 즉, 둘 다 정수면 몫을 반환, 둘 중에 하나라도 실수면 나눈 값을 반환
    
  - `%`는 나머지를 반환한다.

    - 둘 중 하나라도 실수면 실수형으로 나머지를 반환
    - 둘 다 정수면 정수형으로 나머지를 반환

    ```java
    package first;
    
    public class HelloWorld {
    
    	public static void main(String[] args) {
    		double a=5;
            int b=2;
            System.out.println(a/b); //2.5
            System.out.println((int)a/b); //2
    	}
    }
    ```

    

- 증감연산

  - `++`, `--`가 존재, 파이썬의 +=1, -=1과 동일 
  - python과 동일하게 +=x, -=x 등도 사용할 수 있다.
  - 단 파이썬과 달리 뒤에도 쓸 수 있는데 연산자가 어디에 쓰는가에 따라 결과가 달라진다(js와 동일)
    - 전위 연산자: 연산자가 앞에 쓰일 경우, 값이 참조되기 전에 증가
    - 후위 연산자: 연산자가 뒤에 쓰일 경우, 값이 참조된 후에 증가

  ```java
  //기본형
  package first;
  
  public class HelloWorld {
  
  	public static void main(String[] args) {
  		int a=5;
  		int b=5;
  		a++;
  		System.out.println(a);   //6
  		b--;
  		System.out.println(b);   //4
  	}
  }
  
  //연산자의 위치에 따라 결과가 달라진다.
  package first;
  
  public class HelloWorld {
  
  	public static void main(String[] args) {
  		int c=5;
          int d=5;
  		System.out.println(c++);   //5, 값이 참조된 후에 증가
          System.out.println(c);     //6
          System.out.println(++d);   //6, 값이 참조되기 전에 증가
  	}
  }
  ```

  

- 비교연산
  - `==`: 주소값이 같은지를 판별, 값이 같아도 주소값이 다르면 false를 반환
  - `.equals()`: 값이 같은지를 판별



- 논리 연산
  - `&&`: and, 둘 모두 참이어야 참
  - `||`: or, 둘 중 하나만 참이어도 참
  - `!`: 참, 거짓 역전
  - `^`: 둘 중 하나만 true여야 참(둘 다 참이거나 둘 다 거짓이면 false)



- 삼항 연산자

  ```java
  자료형 변수명 = (조건) ? 참일 경우 변수에 대입할 값 : 거짓일 경우 변수에 대입할 값
  
  //예시
  int a = (2>1) ? 10:20
  System.out.println(a) //10
  ```

  



- 연산자 우선 순위
  - 최우선 연산자(소괄호, 대괄호 등)-단항연산자(증감 연산자, 부호 연산자, ! 등)-산술 연산자(사칙연산, shift연산자 등)-비교연산자(등호, 부등등호 등)-비트연산자-논리연산자(&& , ||등)-삼항 연산자-대입 연산자(=, +=, -= 등)
  - 논리연산자 내에서는 &&가 ||보다 우선순위가 높다.





# 제어문

## 조건문

- if문

  ```java
  if (조건문) {
      <수행할 문장1>
      <수행할 문장2>
      ...
  }else if(조건문2){
      <수행할 문장ㄱ>
      <수행할 문장ㄴ>
      ...
  } else {
      <수행할 문장A>
      <수행할 문장B>
      ...
  }
  ```



- switch문

  - case마다 break를 입력하는 이유는 break를 입력하지 않을 경우 한 케이스에 걸려서 해당 케이스가 실행되더라도 다음 케이스로 넘어가기 때문이다.
  - switch/case문은 if else 구조로 변경이 가능하지만 if else 구조로 작성된 모든 코드를 switch 문으로 변경할 수 있는 것은 아니다.

  ```java
  switch(입력변수) {
      case 입력값1: ...
           break;
      case 입력값2: ...
           break;
      ...
      default: ...
           break;
  }
  ```

  - 예시

  ```java
  package first;
  
  public class HelloWorld {
  
  	public static void main(String[] args) {
  		int m = 9;
          String month = "";
          switch (m) {
              case 1:  month = "January";
                       break;
              case 2:  month = "February";
                       break;
              case 3:  month = "March";
                       break;
              case 4:  month = "April";
                       break;
              case 5:  month = "May";
                       break;
              case 6:  month = "June";
                       break;
              case 7:  month = "July";
                       break;
              case 8:  month = "August";
                       break;
              case 9:  month = "September";
                       break;
              case 10: month = "October";
                       break;
              case 11: month = "November";
                       break;
              case 12: month = "December";
                       break;
              default: month = "Invalid month";
                       break;
          }
          System.out.println(monthString); //September
  	}
  }
  
  //아래와 같이 쓰는 것도 가능하다.
  package first;
  
  public class HelloWorld {
  
  	public static void main(String[] args) {
  		int month = 6;
          String season = "";
          switch(month) {
              case 12: case 1: case 2:
                  season = "겨울";
                  break;
              case 3: case 4: case 5:
                  season = "봄";
                  break;
              case 6: case 7: case 8:
                  season = "여름";
                  break;
              case 9: case 10: case 11:
                  season = "가을";
                  break;
          }
          System.out.println(season); //여름
  	}
  }
  ```




## 반복문

- while문

  - 파이썬과 마찬가지로 조건문이 참인 동안 반복수행.
  - break, continue 사용 가능

  ```java
  while (조건문) {
      <수행할 문장1>
      <수행할 문장2>
      <수행할 문장3>
      ...
  }
  ```

  - do while문: while문의 조건이 만족되지 않더라도 무조건 한 번은 수행된다.

  ```java
  do{
      반복 수행할 내용;
  }while(조건);
  
  
  package first;
  
  public class HelloWorld {
  
  	public static void main(String[] args) {
  		int a = 2;
  		do {
  			a++;
  		}while(a<2){};
  		System.out.println(a);  //3, 조건에 맞지 않음에도 do 속의 a++가 한 번 실행됨
  	}
  }
  ```

  

- for문

  - break, continue 사용 가능

  ```java
  for (초기치; 조건문; 증가치){
      <수행할 문장1>
      <수행할 문장2>
      <수행할 문장3>
      ...
  }
  
  //예시
  String[] numbers = {"one", "two", "three"};
  	for(int i=0; i<numbers.length; i++) {
        System.out.println(numbers[i]);
    	}
  ```

  - for each

  ```java
  //기본 구조
  for (type 변수: iterate) {
      body-of-loop
  }
    
  //예시
  package first;
    
  import java.util.HashMap;
    
  public class HelloWorld {
    
   public static void main(String[] args) {
    	int[] numbers = {1,2,3};
    	for(int number: numbers) {
    	   System.out.println(number);
   	}
    }
  }
    
  out
  1
  2
  3
    
        
  //2차원 배열에서 for each
  package first;
    
  import java.util.Arrays;
    
  public class HelloWorld {
    
      public static void main(String[] args) {
          int[][] arr = new int[3][];
          arr[0] = new int[1];
          arr[1] = new int[2];
          arr[2] = new int[3];
          //a의 type은 (위에서 int가 담기는 배열로 선언했으므로)int가 담긴 배열이 될 것이므로 int[]가 된다.
          for(int[] a:arr) {   
          	System.out.println(Arrays.toString(a));
          }
      }
  }
    
  out
  [0]
  [0, 0]
  [0, 0, 0]
  ```