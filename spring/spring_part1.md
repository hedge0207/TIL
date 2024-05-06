# 스프링 기초 개념

## POJO

- 정의: Java의 언어 규약에서 강제된 것 이외에는 특별한 제한에 종속받지 않는 일반적인 Java Object.



- 진정한 POJO(Plain Old Java Object)란 객체지향적인 원리에 충실하면서 환경과 기술에 종속되지 않고 필요에 따라 재활용 될 수 있는 방식으로 설계된 오브젝트를 말한다.

  - 어떤 클래스가 특정 기술, 부모 클래스, 인터페이스에 종속되는 순간부터 사용에 제약이 걸리게 된다.
  - 따라서 새로운 기능을 만들어 낼 때 마다 기존 클래스를 재활용 하는 방식이 아닌 새로운 클래스를 생성해야 하는 상황에 처하게 되고 이는 비효율을 초래한다.

  - 간단하게 Getter, Setter로 구성된 가장 순수한 형태의 기본 클래스를 `POJO`라 한다.



- 따라서 다음과 같은 특징을 지닌다.
  - 미리 지정한 클래스를 `extends`하지 않는다(부모 클래스의 종속을 받지 않는다).
  - 미리 정의된 인터페이스를 `implement`하지 않는다(인터페이스에 종속을 받지 않는다).
  - 미리 정의된 `Annotation`을 포함하지 않는다(어노테이션의 종속을 받지 않는다).
  - 특정 기술에 종속되지 않는다.



- 등장 배경
  - Java는 객체 제향 언어로 설계되어, 원하는 것이 있을 때 개발자는 해당 기술을 직접적으로 사용하는 객체를 설계해야 했다. 
  - 그러나 시간이 흐르면서 특정 기술과 환경에 종속되어 의존하게 된 자바 코드는 가독성이 떨어지고 유지보수에 어려움이 생겼다.
  - 또한 특정 클래스를 상속 받거나 인터페이스에 의존하게 되어 확장성이 떨어지는 문제가 생겼다.
  - 자바는 위와 같은 점들로 인해 객체 지향 설계의 장점들을 잃게 되었다.
  - 마틴 파울러 등의 프로그래머는 이와 같이 특정 프레임 워크, 기술에 종속된 무거운 객체를 만들게 된 것에 반발하며 `POJO`라는 이름을 만들어 냈다.



- 예시: Getter, Setter로 구성된 순수한 형태의 기본 클래스

  ```java
  public class MyPojo {
      private String name;
      private String value;
  
      public String getName() {
      return name;
      }
      public String getValue() {
      return value;
      }
      public void setName(String name) {
      this.name = name;
      }
      public void setValue(String value) {
      this.value = value;
      }
  }
  ```

  



## PSA

- PSA(Portable Service Abstraction)

- 환경의 변화와 관계 없이 일관된 방식의 기술로의 접근 환경을 제공하려는 추상화 구조를 말한다.
- 배경
  - `POJO`는 특정 기술에 종속되지 않은 순수한 Java Object를 지칭한다.
  - 그렇다고 기술을 사용하지 않을 수는 없기에 `POJO`로 개발을 하면서도 기술을 사용할 수 있도록 한 것이 `PSA`다.
- Spring은 라이브러리들을 POJO 원칙을 지키도록 PSA형태의 추상화 과정을 거치게 한다.
  - 따라서 같은 라이브러리라도 Spring에서 사용될 때와 다른 Java Framework에서 사용될 때는 다르다. 
  - 예를 들어 Spring의 MyBatis와 다른 Framework에서의 MyBatis는 다르다.





## IoC와 DI

- IoC(Inversion of Control)

  - 정의: 객체 지향 언어에서 객체 간의 연결 관계(의존성)를 컨테이너가 결정하게 하는 방법, 객체의 생성과 생명주기를 컨테이너가 관리한다.
  - 어떤 객체가 사용할 객체(의존적인 객체)를 직접 선언하여 사용하는 것이 아니라, 어떤 방법을 사용하여 주입 받아 사용하는 방법
  - 기존에는 의존성(객체 간의 연결 관계 설정)에 대한 제어권이 개발자에게 있었다면 IoC는 개발자가 아닌 컨테이너가 제어권을 가지게 된다(제어의 역전).

  ```java
  //일반적인 제어권 관리
  //BookService에서 BookRepository를 사용하고자 할 경우 아래와 같이 작성했다.
  @Service
  public class BookService {
      //의존적인 객체를 개발자가 직접 생성하여 사용
      private BookRepository bookRepository = new BookRepository();
  }
  
  
  //IoC
  @Service
  public class BookService {
      //사용은 하지만 new를 통해 만들진 않는다.
      private BookRepository bookRepository;
      //BookService 밖에서 의존성을 줄 수 있도록 생성자를 통해서 의존성을 주입
      public BookService(BookRepository bookRepository){
          this.bookRepository = bookRepository
      }
  }
  ```

  

- 객체 간의 관계가 느슨하게 연결된다.

  - A와 B 객체가 바로 연결 된 것을(`A-B`) 강하게 연결되었다고 하고
  - A와 B 객체가 C라는 인터페이스를 통해 연결 된 것을(`A-B-C`) 느슨하게 연결되었다고 한다.
  - 느슨하게 연결했을 때의 장점은 수정, 삭제 후 새로운 클래스 이식 등이 비교적 자유롭다는 점이다.
  - `IoC`의 구현 방법 중 하나가 `DI`(Dependency Injection)다.



- 의존성 관리 방법1.클래스와 클래스를 직접 연결(강한 연결)

  - 처음에는 "안녕! "이라는 문구를 넣었는데 영어로 "Hello! "라고 바꿔야 한다면 직접 수정해야 한다.

  ```java
  //Hello.java
  
  package step1;
  
  public class Hello {
  	public void sayHello(String name) {
  		//System.out.println("안녕! "+name);
          System.out.println("Hello! "+name);
  	}
  }
  
  
  //HelloTest.java
  package step1;
  
  public class HelloTest {
  	public static void main(String[] args) {
          //연결된 class인 Hello로 객체를 생성한 후 객체를 지칭하고 있는 hello를 가지고 sayHello() 메서드를 호출한다.
  		Hello hello = new Hello();
  		hello.sayHello("홍길동");
  	}
  }
  ```



- 의존성 관리 방법2. 인터페이스를 사용하여 느슨한 연결

  - 인터페이스를 사용하는 클래스를 생성
  - 처음에는 "안녕! "이라는 문구를 넣었는데 영어로 "Hello! "라고 바꿔야 한다면 코드를 수정해야 한다.

  ```java
  //Hello.java
  package step2;
  //인터페이스 생성
  public interface Hello {
  	//선언된 메서드
  	public void sayHello(String name);
  }
  
  
  //HelloKo.java
  package step2;
  
  public class HelloKo implements Hello{
  
  	@Override
  	public void sayHello(String name) {
  		System.out.println("안녕! "+name);
  	}
  }
  
  
  //HelloEn.java
  package step2;
  
  public class HelloEn implements Hello{
  
  	@Override
  	public void sayHello(String name) {
  		System.out.println("Hello! "+name);
  	}
  }
  
  
  //HelloTest.java
  package step2;
  
  public class HelloTest {
  	public static void main(String[] args) {
          //이 부분을 직접 수정해야 한다.
  		//Hello hello = new HelloKo();
  		//hello1.sayHello("홍길동");
  		Hello hello = new HelloEn();
  		hello2.sayHello("홍길동");
  	}
  }
  ```



- 의존성 관리 방법3. IoC

  - 이 방법을 사용하기 위해선 spring이 필요
  - 만일 수정하고 싶다면 xml 파일만 수정하면 된다.
  - `@Authowired` 어노테이션을 통해 더 쉽게 하는 방법이 있다.

  ```xml
  <!--applicationContext.xml-->
  <?xml version="1.0" encoding="UTF-8"?>
  <beans xmlns="http://www,springframework.org/chema/beans"
  	   xmlns:xsi="http://www.w3.org/2001/XNLSchema-istance"
  	   xsi:schmaLocation="http://www.springframework.org/schema/beans
  	   						http://www.springframework.org/schema/beans/spring-beans.xsd">
  	   <!--xml의 태그 명은 데이터에 대한 서술, 설명-->
  	   <!-- 등록할 Bean을 정의, 추상 클래스, 인터페이스는 등록 불가 -->
      
  	   <!-- 아래 코드는 HelloKo hk = new HelloKo() 와 동일한 코드 -->
  	   <!--
      	<Bean class="step3.HelloKo"
  	   		 id="hi"</Bean>
      	-->
      
      	<!-- 영어로 표시하고 싶다면 아래와 같이 class명만 바꾸면 된다. -->
      	<Bean class="step3.HelloEn"
  	   		 id="hi"</Bean>
  </beans>
  ```

  ```java
  //Hello.java
  package step3;
  
  public interface Hello {
  	public void sayHello(String name);
  }
  
  
  //HelloKo.java
  package step3;
  
  public class HelloKo implements Hello{
  	
  	//생성자
  	public HelloTestKo() {
  		System.out.println("기본 생성자가 호출되었습니다.");
  	}
  
  	@Override
  	public void sayHello(String name) {
  		System.out.println("안녕! "+name);
  	}
  }
  
  
  //HelloEn.java
  package step3;
  
  public class HelloEn implements Hello{
  
  	@Override
  	public void sayHello(String name) {
  		System.out.println("Hello! "+name);
  	}
  }
  
  
  //HelloTest.java
  package step3;
  
  //ApplicationContext를 import 해야 한다.
  import org.springframework.context.ApplicationContext;
  import org.springframework.context.support.ClassPathXmlApplicationContext;
  
  public class HelloTest {
  	public static void main(String[] args) {
  		//테스트가 실행되면 HelloKo의 생성자가 실행되어 "기본 생성자가 호출되었습니다."가 출력된다.
  		ApplicationContext ctx = new ClassPathXmlApplicationContext
            		//step3/applicationContext.xml은 src부터 applicationContext.xml파일 까지의 경로이다.
  				("step3/applicationContext.xml");
          //.getBean("hi")에 들어간 "hi"는 xml에서 지정해준 id이다.  
          Hello hello = (Hello) ctx.getBean("hi");
          hello.sayHello("홍길동");
          //xml파일에 어떤 클래스를 작성했는가에 따라 "안녕! 홍길동"이 나오기도 하고 "Hello! 홍길동"이 나오기도 한다.
  	}
  }
  ```





## AOP

- AOP(Aspect Oriented Programming)
  - 정의: 관심사의 분리를 통해 소프트웨어의 모듈성을 향상시키고자 하는 프로그래밍 패러다임
  - 프로젝트를 진행하다 보면 여러 기능이 필요하게 되고 여러 기능에 공통적으로 들어가야 하는 코드가 생기게 된다.
  - 이러한 공통 코드를 따로 작성(메서드)하여 각 기능에서 활용하는 것

- 횡단관심(Cross-cutting concern): 어플리케이션의 다양한 관점에 영향을 미치는 기능

  - 예를 들어 보안은 어플리케이션의 많은 기능에 적용 될 보안 규칙을 가지고 있다는 차원에서 횡단 관심이다.
  - 핵심관심은 구현하고자 하는 기능, 횡단 관심은 핵심 관심에 공통적으로 적용되는 기능들을 의미한다.
  - 예를 들어 수업 관리용 어플리케이션을 개발한다고 할 때 교수를 위한 관리 기능, 학생을 위한 관리 기능이 있을 것이고 이것들이 이 어플리케이션의 핵심 기능이라고 할 수 있다. 그런데 이들 기능은 공통적으로 개인 정보를 담고 있을 것이기에 보안에 신경을 써야한다. 따라서 보안이 이 기능들의 횡단 관심이라 할 수 있다.

  - 횡단 관심은 aspect라고 하는 특별한 객체로 모듈화가 가능하다.

- 용어

  - aspect: 횡단 관심사의 동작과 그 횡단관심사를 적용하려는 소스 코드에서의 위치를 모아 둔 것, 하나 이상의 advice(동작)과 pointcut(동작 조건)을 조합한 것
  - joinpoint: advice가 실행하는 동작을 끼워 넣을 수 있는 때를 의미한다. 스프링에서는 메소드가 호출될 때와 원래 호출한 곳으로 돌아갈 때가 advice를 끼워 넣을 수 있는 joinpoint다.
  - advice: joinpoint에서 실행되는 코드(메소드)로 보안, 로깅, 트랜잭션 관리 등의 코드가 기술된다.
    - before: joinpoint 앞에서 실행할 advice
    - after: joinpoint 뒤에서 실행할 advice
    - afterreturning: joinpoint가 정상 종료한 다음 실행되는 advice
    - around: joinpoint 앞뒤에 실행되는 advice
    - afterthrowing: joinpoint에서 예외가 발생했을 때 실행되는 advice
  - pointcut: joinpoint와 advice의 중간에 있으면서 처리가 joinpoint에 이르렀을 때 advice를 호출할지 선별한다.
