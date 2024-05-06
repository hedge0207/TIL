# 싱글톤 컨테이너

## 웹 애플리케이션과 싱글톤

- 대부분의 스프링 애플리케이션은 웹 애플리케이션이나 웹이 아닌 애플리케이션도 개발 가능하다.



- 웹 애플리케이션은 보통 여러 고객이 동시에 요청을 한다.

  - 아래 코드의 경우에 2명이 요청하면 2개의 객체가, 5명이 요청하면 5개의 객체가, 10만명이 요청하면 10만개의 객체가 생성되고 소멸된다.
  - 메모리 낭비가 굉장히 심한 방식이다.
  - 따라서 이를 해결하기 위해 해당 객체가 딱 1개만 생성되고, 공유하도록 설계한다(싱글톤 패턴).

  ```java
  package start.first.singleton;
  
  import org.assertj.core.api.Assertions;
  import org.junit.jupiter.api.DisplayName;
  import org.junit.jupiter.api.Test;
  import start.first.AppConfigSpring;
  import start.first.member.MemberService;
  
  public class SingletonTest {
      
      @Test
      @DisplayName("스프링 없는 순수한 DI 컨테이너")
      void pureContainer(){
          AppConfigSpring appConfigSpring = new AppConfigSpring();
          
          //한 유저가 조회, 호출될 때마다 MemberService의 객체를 생성
          MemberService memberService1 = appConfigSpring.memberService();
  
          //다른 유저가 조회, 호출될 때마다 MemberService의 객체를 생성
          MemberService memberService2 = appConfigSpring.memberService();
  
          //두 객체의 참조값이 다르다. 즉 매번 새로 생성한다.
          System.out.println("memberService1 = " + memberService1); 
          //memberService1 = start.first.member.MemberServiceImpl@5542c4ed
          System.out.println("memberService2 = " + memberService2); 
          //memberService2 = start.first.member.MemberServiceImpl@1573f9fc
          
          //정말 둘이 다른지 검증
          Assertions.assertThat(memberService1).isNotSameAs(memberService2);
  
      }
  
  }
  ```





## 싱글톤 패턴

- 싱글톤 패턴: 클래스의 인스턴스가 딱 1개만 생성되는 것을 보장하는 디자인 패턴이다.

  - 객체 인스턴스를 2개 이상 생성하지 못하도록 막아야 한다.
  - 싱글톤 패턴을 구현하는 방법은 다양하다. 그 중 아래 예시는 객체를 미리 생성해두는 가장 단순하고 안전한 방법이다.

  ```java
  package start.first.singleton;
  
  public class SingletonService {
  
      //클래스 자체를 클래스 내부에 private static으로 선언
      private static final SingletonService instance = new SingletonService();
  
      //이제부터 호출 될 때 계속 새로운 객체를 생성하는 것이 아니라 위에서 생성한 객체를 넘기게 된다. 따라서 항상 같은 인스턴스를 반환한다.
      //public으로 열어서 객체 인스턴스가 필요하면 오직 이 static 메서드를 통해서만 조회하도록 한다.
      public static SingletonService getInstance(){
          return instance;
      }
  
      //위에서 객체를 공유하도록 코드를 짰는데 다른 곳에서 다시 아래와 같이 쓰면 또 객체가 계속 생성되므로 다른 곳에서는 쓰지 못하게 해야 한다.
      //다른 곳에서 다시 SingletonService의 객체를 생성하지 못하도록 private을 걸어둔다.
      //SingletonService singletonService = new SingletonService(); 와 같은 코드를 이제 다른 곳에서는 쓸 수 없다.
      private SingletonService(){
      }
      
      public void logic(){
          System.out.println("싱글톤 객체 로직 호출");
      }
  }
  ```

  - 테스트

  ```java
  package start.first.singleton;
  
  import org.assertj.core.api.Assertions;
  import org.junit.jupiter.api.DisplayName;
  import org.junit.jupiter.api.Test;
  import start.first.AppConfigSpring;
  import start.first.member.MemberService;
  
  public class SingletonTest {
      //전략(스프링 없는 순수한 DI 컨테이너)
  
      @Test
      @DisplayName("싱글톤 패턴을 적용한 객체 사용")
      void singtonServiceTest(){
          //SingletonService에 private을 걸어뒀으므로 아래와 같이 다른 곳에서 새로 생성 할 수 없다.
          //new SingletonService();
          SingletonService singletonService1 = SingletonService.getInstance();
          SingletonService singletonService2 = SingletonService.getInstance();
  
          //둘의 참조값이 동일한다.
          System.out.println("singletonService1 = " + singletonService1);
          //singletonService1 = start.first.singleton.SingletonService@1165b38
          System.out.println("singletonService2 = " + singletonService2);
          //singletonService2 = start.first.singleton.SingletonService@1165b38
  
          //둘이 정말 동일한지 검증
          Assertions.assertThat(singletonService1).isSameAs(singletonService2);
          //.isSameAs: 자바 ==으로 비교하는 것과 동일
          //.isEqualTo: 자바의 .equals 메소드로 비교하는 것과 동일
      }
  
  }
  ```



- 싱글톤 패턴의 문제점
  - 싱글톤 패턴을 구현하는 코드 자체가 많이 들어간다.
  - 의존관계상 클라이언트가 구체 클래스에 의존한다. -> DIP 위반
  - 클라이언트가 구체 클래스에 의존해서 OCP 원칙을 위반할 가능성이 높다. 
  - 테스트하기 어렵다. 
  - 내부 속성을 변경하거나 초기화 하기 어렵다. 
  - private 생성자로 자식 클래스를 만들기 어렵다. 
  - 결론적으로 유연성이 떨어진다. 
  - 안티패턴으로 불리기도 한다.





## 싱글톤 컨테이너

- 스프링 컨테이너는 싱글톤 패턴의 문제점을 해결하면서, 객체 인스턴스를 싱글톤(1개만 생성)으로 관리한다. 현재까지 우리가 학습한 스프링 빈이 싱글톤으로 관리되는 빈이다.



- 싱글톤 컨테이너

  - 스프링 컨테이너는 싱글톤 패턴을 적용하지 않아도, 객체 인스턴스를 싱글톤으로 관리한다.
    - 스프링 컨테이너에 빈을 등록할 때 빈 객체를 (단 하나만)생성하여 조회할 때마다 해당 객체를 조회한다.
    - 단 스프링의 기본 빈 등록 방식은 싱글톤(99.9%)이지만, 싱글톤 방식만을 지원하는 것은 아니다. 
    - 요청할 때마다 새로운 객체를 생성해서 반환하는 기능도 제공한다(뒤의 빈 스코프에서 설명).
  - 스프링 컨테이너는 싱글톤 컨테이너 역할을 한다. 이렇게 싱글톤 객체를 생성하고 관리하는 기능을 싱글톤 레지스트리라 한다.
  - 스프링 컨테이너의 이런 기능 덕분에 싱글턴 패턴의 모든 단점을 해결하면서 객체를 싱글톤으로 유지할 수 있다.
    - 싱글톤 패턴을 구현하기 위한 복잡한 코드를 작성하지 않아도 된다.
    - DIP,OCP, 테스트, private 생성자로 부터 자유롭게 싱글톤을 사용할 수 있다.

  - 스프링 컨테이너 활용

  ```java
  package start.first.singleton;
  
  import org.assertj.core.api.Assertions;
  import org.junit.jupiter.api.DisplayName;
  import org.junit.jupiter.api.Test;
  import org.springframework.context.ApplicationContext;
  import org.springframework.context.annotation.AnnotationConfigApplicationContext;
  import start.first.AppConfigSpring;
  import start.first.member.MemberService;
  
  public class SingletonTest {
      
      //전략(싱글톤 패턴을 적용한 객체 사용)
      @Test
      @DisplayName("스프링 컨테이너와 싱글톤")
      void springContainer(){
          
          //스프링 컨테이너 생성
          ApplicationContext ac = new AnnotationConfigApplicationContext(AppConfigSpring.class);
          
          MemberService memberService1 = ac.getBean("memberService",MemberService.class);
          MemberService memberService2 = ac.getBean("memberService",MemberService.class);
  
          //둘의 참조값이 동일한다.
          System.out.println("memberService1 = " + memberService1); 
          //memberService1 = start.first.member.MemberServiceImpl@23fb172e
          System.out.println("memberService2 = " + memberService2); 
          //memberService2 = start.first.member.MemberServiceImpl@23fb172e
  
          //둘이 정말 동일한지 검증
          Assertions.assertThat(memberService1).isSameAs(memberService2);
      }
  
  }
  ```





## 싱글톤 방식의 주의점

- 무상태(stateless)로 설계해야 한다.
  - 싱글톤 패턴이든, 스프링 같은 싱글톤 컨테이너를 사용하든, 객체 인스턴스를 하나만 생성해서 공유하는 싱글톤 방식은 여러 클라이언트가 하나의 같은 객체 인스턴스를 공유하기 때문에 싱글톤 객체는 상태를 유지(stateful)하게 설계하면 안된다.
  - 특정 클라이언트에 의존적인 필드가 있으면 안된다.
  - 특정 클라이언트가 값을 변경할 수 있는 필드가 있으면 안된다.
  - 가급적 읽기만 가능해야 한다.
  - 필드 대신에 자바에서 공유되지 않는, 지역변수, 파라미터, ThreadLocal 등을 사용해야 한다.
  - 스프링 빈의 필드에 공유 값을 설정하면 정말 큰 장애가 발생할 수 있다.



- 상태를 유지하도록 설계

  - 단순한 설명을 위해 실제 Thread를 사용하지는 않았다.
  - `StatefulService`의 `price` 필드는 공유되는 필드인데, 클라이언트에 따라 값이 변경된다.
  - 실무에서도 이런 경우가 종종 발생하는데, 정말 해결하기 어려운 큰 문제들이 터진다.
  - StatefulService.java

  ```java
  package start.first.singleton;
  
  public class StatefulService {
  
      private int price; //상태를 유지하는 필드
  
      public void order(String name, int price){
          System.out.println("name = " + name + " price = " + price);
  
          //여기가 문제가 된다.
          this.price=price;
      }
  
      public int getPrice(){
          return price;
      }
  }
  ```

  - StatefulServiceTest.java

  ```java
  package start.first.singleton;
  
  import org.assertj.core.api.Assertions;
  import org.junit.jupiter.api.Test;
  import org.springframework.context.ApplicationContext;
  import org.springframework.context.annotation.AnnotationConfigApplicationContext;
  import org.springframework.context.annotation.Bean;
  
  class StatefulServiceTest {
  
      //테스트용 AppConfig
      static class TestConfig{
          @Bean
          public StatefulService statefulService(){
              return new StatefulService();
          }
      }
  
      @Test
      void statefulServiceSingleton(){
  
  
          ApplicationContext ac = new AnnotationConfigApplicationContext(TestConfig.class);
          StatefulService statefulService1 = ac.getBean(StatefulService.class);
          StatefulService statefulService2 = ac.getBean(StatefulService.class);
         
          //TreadA: A사용자가 10,000원 주문
          statefulService1.order("userA",10000);
  
          //TreadB: B사용자가 20,000원 주문
          statefulService2.order("userA",20000);
  
          //TreadA: 사용자A가 주문한 금액 조회
          int price = statefulService1.getPrice();
          //B사용자가 주문하면서 price가 20000으로 바뀌어 10000이 아닌 20000이 출력된다.
          System.out.println("price = " + price);  //price = 20000
  
          Assertions.assertThat(statefulService1.getPrice()).isEqualTo(20000);
  
      }
  
  }
  ```



- 무상태로 설계

  - StatelessService.java

  ```java
  package start.first.singleton;
  
  public class StatelessService {
  
      public int order(String name, int price){
          System.out.println("name = " + name + " price = " + price);
          return price;
     }
  }
  ```

  - StatelessServiceTest.java

  ```java
  package start.first.singleton;
  
  import org.assertj.core.api.Assertions;
  import org.junit.jupiter.api.Test;
  import org.springframework.context.ApplicationContext;
  import org.springframework.context.annotation.AnnotationConfigApplicationContext;
  import org.springframework.context.annotation.Bean;
  
  
  class StatelessServiceTest {
  
      //테스트용 AppConfig
      static class TestConfig{
          @Bean
          public StatelessService statelessService(){
              return new StatelessService();
          }
      }
  
      @Test
      void statelessServiceSingleton(){
  
          ApplicationContext ac = new AnnotationConfigApplicationContext(StatelessServiceTest.TestConfig.class);
          StatelessService statelessService1 = ac.getBean(StatelessService.class);
          StatelessService statelessService2 = ac.getBean(StatelessService.class);
  
          //아래와 같이 가격을 각각 userAPrice, userBPrice 라는 지역 변수에 담는다.
          //TreadA: A사용자가 10,000원 주문
          int userAPrice = statelessService1.order("userA",10000);
  
          //TreadB: B사용자가 20,000원 주문
          int userBPrice = statelessService2.order("userB",20000);
  
          //A사용자가 주문한 금액
          System.out.println("price = " + userAPrice); //10000
  
          Assertions.assertThat(userAPrice).isEqualTo(10000);
  
      }
  
  }
  ```





## Configuration과 싱글톤

- 아래 코드에서 싱글톤이 지켜질까?

  - AppConfigSpring.java
    - 아래 코드에서 `memberService`가 스프링 컨테이너에 등록될 때 `MemberServiceImpl`이 호출되고 `memberRepository`도 함께 호출된다.
    - 이 경우 `new MemoryMemberRepository();`코드가 실행되면서 새로운 객체를 만들게 된다.
    - `orderService`도 마찬가지로 스프링 컨테이너에 등록될 때 `OrderServiceImpl`이 호출되고 `memberRepository`, `discountPolicy` 도 함께 호출되어  `new MemoryMemberRepository()`, `new FixDiscountPolicy()`가 실행되면서 새로운 객체를 만들게 된다.
    - 결과적으로 각각 다른 2개의 `MemoryMemberRepository`가 생성되게 된다.
    - 이러한 문제를 스프링 컨테이너는 어떻게 해결하는가?

  ```java
  //전략
  
  @Configuration
  public class AppConfigSpring {
      
      @Bean
      public MemberService memberService(){
          return new MemberServiceImpl(memberRepository());
      }
  
      @Bean
      public MemoryMemberRepository memberRepository() {
          return new MemoryMemberRepository();
      }
  
      @Bean
      public OrderService orderService(){
          return new OrderServiceImpl(memberRepository(),discountPolicy());
      }
  
      @Bean
      public DiscountPolicy discountPolicy(){
          return new FixDiscountPolicy();
      }
  }
  ```



- 싱글톤 유지 여부 테스트

  - MemberServiceImpl.java

  ```java
  //전략
  
  public class MemberServiceImpl implements MemberService{
  
      private final MemberRepository memberRepository;
  
      public MemberServiceImpl(MemberRepository memberRepository) {
          this.memberRepository = memberRepository;
      }
  
      @Override
      public void join(Member member) {
          memberRepository.save(member);
      }
  
      @Override
      public Member findMember(Long memberId) {
          return memberRepository.findById(memberId);
      }
  
      //싱글톤이 지켜지는지 테스트용
      public MemberRepository getMemberRepository(){
          return memberRepository;
      }
  }
  ```

  - OrderServiceImpl.java

  ```java
  //전략
  
  public class OrderServiceImpl implements OrderService{
  
      private final MemberRepository memberRepository;
      private final DiscountPolicy discountPolicy;
  
      public OrderServiceImpl(MemberRepository memberRepository, DiscountPolicy discountPolicy) {
          this.memberRepository = memberRepository;
          this.discountPolicy = discountPolicy;
      }
  
      @Override
      public Order createOrder(Long memberId, String itemName, int itemPrice) {
          Member member = memberRepository.findById(memberId);
          int discountPrice = discountPolicy.discount(member, itemPrice);
          return new Order(memberId,itemName,itemPrice,discountPrice);
      }
  
      //싱글톤이 지켜지는지 테스트용
      public MemberRepository getMemberRepository(){
          return memberRepository;
      }
  }
  ```

  - ConfigurationSingletonTest.java

  ```java
  package start.first.singleton;
  
  import org.assertj.core.api.Assertions;
  import org.junit.jupiter.api.Test;
  import org.springframework.context.ApplicationContext;
  import org.springframework.context.annotation.AnnotationConfigApplicationContext;
  import start.first.AppConfigSpring;
  import start.first.member.MemberRepository;
  import start.first.member.MemberServiceImpl;
  import start.first.order.OrderServiceImpl;
  
  public class ConfigurationSingletonTest {
  
      @Test
      void configurationTest(){
          ApplicationContext ac = new AnnotationConfigApplicationContext(AppConfigSpring.class);
  
          //본래 아래와 같이 구체 타입(MemberServiceImpl, OrderServiceImpl)으로 빈을 꺼내는 것은 좋지 않은 방법이지만 편의를 위해 아래와 같이 꺼낸다.
          MemberServiceImpl memberService = ac.getBean("memberService", MemberServiceImpl.class);
          OrderServiceImpl orderService = ac.getBean("orderService", OrderServiceImpl.class);
          MemberRepository memberRepository = ac.getBean("memberRepository", MemberRepository.class);
  
          MemberRepository memberRepository1 = memberService.getMemberRepository();
          MemberRepository memberRepository2 = orderService.getMemberRepository();
  
          //셋의 참조값이 같다.
          System.out.println("memberService -> memberRepository1 = " + memberRepository1);
          //memberService -> memberRepository1 = start.first.member.MemoryMemberRepository@299321e2
          System.out.println("orderService -> memberRepository2 = " + memberRepository2);
          //orderService -> memberRepository2 = start.first.member.MemoryMemberRepository@299321e2
          System.out.println("memberRepository = " + memberRepository);
          //memberRepository = start.first.member.MemoryMemberRepository@299321e2
  
          Assertions.assertThat(memberService.getMemberRepository()).isSameAs(memberRepository);
          Assertions.assertThat(orderService.getMemberRepository()).isSameAs(memberRepository);
  
      }
  }
  ```



- MemoryMemberRepository가 3번 호출 되는지 테스트

  - 위 테스트에서 확인했듯 셋의 참조값이 같았다.
  - 이는 사실 MemoryMemberRepository가 1번만 호출되었기 때문이다.
  - AppConfigSpring.java

  ```java
  //전략
  
  @Configuration
  public class AppConfigSpring {
  
      @Bean
      public MemberService memberService(){
          System.out.println("call AppConfig.memberService");  //호출 여부 확인을 위한 sout
          return new MemberServiceImpl(memberRepository());
      }
  
      @Bean
      public MemoryMemberRepository memberRepository() {
          System.out.println("call AppConfig.memberRepository"); //호출 여부 확인을 위한 sout
          return new MemoryMemberRepository();
      }
  
      @Bean
      public OrderService orderService(){
          System.out.println("call AppConfig.orderService");   //호출 여부 확인을 위한 sout
          return new OrderServiceImpl(memberRepository(),discountPolicy());
      }
  
      @Bean
      public DiscountPolicy discountPolicy(){
          return new FixDiscountPolicy();
      }
  }
  
  //결과
  전략
  call AppConfig.memberService
  중략
  call AppConfig.memberRepository  //memberRepository는 1번 밖에 호출되지 않았다.
  중략
  call AppConfig.orderService
  후략
  ```







## Configuration과 바이트 코드 조작

- 위 테스트에서 확인할 수 있듯 `memberRepository`는 1번 밖에 호출되지 않았고 싱글톤을 유지할 수 있었다. 그러나 코드상 3번이 호출되었어야 한다. 이게 어떻게 가능한 것일까?



- `@Configuration`

  - 이는 `@Configuration` 어노테이션이 붙어 있기에 가능한 것이다.
  - ConfigurationSingletonTest.java

  ```java
  //전략
  
  public class ConfigurationSingletonTest {
  
      //중략
      
      @Test
      void configurationDeepTest(){
          ApplicationContext ac = new AnnotationConfigApplicationContext(AppConfigSpring.class);
          AppConfigSpring bean = ac.getBean(AppConfigSpring.class);
  
          System.out.println("bean = " + bean.getClass());
          //bean = class start.first.AppConfigSpring$$EnhancerBySpringCGLIB$$31febfb1
          //순수한 클래스라면 아래와 같이 출력되어야 한다. 그러나 위에서 볼 수 있듯이 $$ 뒤에 CGLIB를 포함하여 뭔가가 더 붙어있다.
          //class start.first.AppConfigSpring
  
      }
  }
  ```

  - CGLIB: 바이트 조작 라이브러리로, 스프링은 이를 활용하여 AppConfigSpring 클래스를 상속 받은 임의의 다른 클래스를 만들고, 그 다른 클래스를 스프링 빈으로 등록한 것이다. 이를 통해 싱글톤이 보장되게 된다.
    - 실제로 CGLIB의 동작 방식은 매우 복잡하지만 단순화하면 다음과 같을 것이다.
    - 만일 특정 빈이 이미 스프링 컨테이너에 등록되어 있으면, 스프링 컨테이너에서 해당 빈을 찾아서 반환
    - 스프링 컨테이너에 등록되어 있지 않으면, 해당 빈을 스프링 컨테이너에 등록
    - 따라서 `memberRepository`는 최초 1회만 호출되고 나머지는 호출되지 않은 것이다.

  - 참고: 위에서 분명히 bean 변수를 AppConfigSpring 타입으로 선언했는데도  AppConfigSpring@CGLIB이 나온 이유는 무엇인가?
    - AppConfigSpring@CGLIB은 AppConfigSpring의 자식 타입이므로, AppConfigSpring로 조회가 가능한 것이다.



- `@Configuration`을 쓰지 않을 경우
  -  `@Configuration`을 쓰지 않고 `@Bean`만 사용해서 실행할 경우 스프링 빈으로 등록은 되지만, 싱글톤은 깨지게 된다.
  - AppConfigSpring.java 파일에서 `@Configuration`을 주석 처리하고 실행하면 "call AppConfig.memberRepository"가 3번 출력 된다. 또한ConfigurationSingletonTest.java 를 실행했을 때 셋의 참조값이 모두 다르게 나온다.
  - 또한 orderService와 memberService에 주입된 memberRepository는 스프링 컨테이너에서 관리하는 빈이 아닌 단순 객체가 되게 된다.
  - 결국 `@Configuration`을 쓰지 않을 이유가 없다.







# 컴포넌트 스캔

## 컴포넌트 스캔과 의존관계 자동 주입 시작하기

- 지금까지 스프링 빈을 등록할 때는 자바 코드의 @Bean이나 XML의 \<bean>을 통해서 설정 정보에 직접 등록할 스프링 빈을 나열했다.
  - 이렇게 할 경우 등록해야 할 스프링 빈이 많아지면 일일이 등록하기도 귀찮거니와 설정 정보도 커지고 누락되는 문제도 발생할 수 있다.
  - 따라서 스프링은 설정 정보가 없어도 자동으로 스프링 빈을 등록하는 컴포넌트 스캔이라는 기능을 제공한다.
  - 의존 관계를 자동으로 주입하는 `@Autowired`라는 기능도 제공한다. 



- 예시

  - AutoAppConfig.java 생성

  ```java
  package start.first;
  
  import org.springframework.context.annotation.ComponentScan;
  import org.springframework.context.annotation.Configuration;
  import org.springframework.context.annotation.FilterType;
  
  @Configuration
  //@ComponentScan는 @Component 어노테이션이 붙은 클래스들을 스캔해서 빈을 등록한다.
  //속성 중 제외 할 것들을 지정할 수 있는 excludeFilters가 있다.
  //아래에서 Configuration을 제외한 이유는 @Configuration 어노테이션의 소스코드를 보면 내부에 @Component 어노테이션이 사용되기 때문이다.
  //보통 설정 정보(AppConfig)를 스캔 대상에서 제외하지는 않지만 현재는 앞에서 예시를 위해 사용한 AppConfigSpring이 살아있기에 아래와 같이 제외해준다.
  @ComponentScan(
          excludeFilters = @ComponentScan.Filter(type = FilterType.ANNOTATION, classes = Configuration.class)
  )
  public class AutoAppConfig {
      
  }
  ```

  - MemoryMemberRepository.java, RateDiscountPolicy.java 등 등록하려는 빈에 `@Component` 어노테이션을 달아준다.
  - 그런데 MemberServiceImpl, OrderServiceImpl에는 생성자에 `@Autowired`도 추가해야 한다.
    - 기존에 AppConfigSpring에서는 MemberServiceImpl이 memberRepository를 의존한다고 명시적으로 표시할 수 있었다.
    - 마찬가지로 OrderServiceImpl이 memberRepository, discountPolicy를 의존한다고 명시적으로 표기할 수 있었다.
    - 그러나 이제 컴포넌트 스캔을 할 때 빈이 자동으로 등록되므로 그렇게 할 수 없다.
    - 따라서 `@Autowired` 어노테이션을 통해 의존관계를 자동으로 주입해야 한다.
    - 생성자에 `@Autowired`가 붙어 있으면 의존성이 자동으로 주입된다.
    - `@Autowired`의 기본 동작은 주입할 대상이 없으면 오류가 발생하는 것이다. 주입할 대상이 없어도 동작하게 하려면 `@Autowired(required=false)`로 지정하면 된다.

  ```java
  package start.first.member;
  
  import org.springframework.beans.factory.annotation.Autowired;
  import org.springframework.stereotype.Component;
  
  @Component
  public class MemberServiceImpl implements MemberService{
  
      private final MemberRepository memberRepository;
  
      //@Autowired를 사용하지 않는 기존 방식
      //생성자를 만든다.
      //public MemberServiceImpl(MemberRepository memberRepository) {
      //    this.memberRepository = memberRepository;
      //}
  	
      
      //생성자에 @Autowired를 달아준다.
      @Autowired  //getBean(MemberRepository.class)와 유사하다고 이해하면 된다.
      public MemberServiceImpl(MemberRepository memberRepository) {
          this.memberRepository = memberRepository;
      }
  
  	//후략
  }
  ```

  ```java
  //전략
  
  public class OrderServiceImpl implements OrderService{
  
      private final MemberRepository memberRepository;
      private final DiscountPolicy discountPolicy;
  
      //생성자
      //@Autowired를 사용하기 전 코드
      //public OrderServiceImpl(MemberRepository memberRepository, DiscountPolicy discountPolicy) {
      //    this.memberRepository = memberRepository;
      //    this.discountPolicy = discountPolicy;
      //}
  
      //생성자에 @Autowired를 붙인다.
      @Autowired
      public OrderServiceImpl(MemberRepository memberRepository, DiscountPolicy discountPolicy) {
          this.memberRepository = memberRepository;
          this.discountPolicy = discountPolicy;
      }
  
  	//후략
  }
  ```

  

- 테스트

  ```java
  package start.first.scan;
  
  import org.assertj.core.api.Assertions;
  import org.junit.jupiter.api.Test;
  import org.springframework.context.annotation.AnnotationConfigApplicationContext;
  import start.first.AutoAppConfig;
  import start.first.member.MemberService;
  
  public class AutoAppConfigTest {
  
      @Test
      void basicScan(){
          AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(AutoAppConfig.class);
  
          MemberService memberService = ac.getBean(MemberService.class);
          Assertions.assertThat(memberService).isInstanceOf(MemberService.class);
      }
  }
  ```



- `@ComponentScan`의 동작 원리
  - `@Component`가 붙은 모든 클래스를 스프링 빈으로 등록한다(싱글톤으로 등록한다).
  - 이때 스프링 빈의 기본 이름은 클래스명을 사용하되 맨 앞글자만 소문자로 등록된다.
    - e.g. MemberServiceImpl 클래스가 스프링 빈에 등록 될 때는 빈 이름이 memberServiceImpl로 등록된다.
    - 만일 빈 이름을 직접 지정하고 싶으면 `@Component("memberServiceImpl2")`와 같이 이름을 부여하면 된다.
  - 생성자에 `@Autowired`를 지정하면, 스프링 컨테이너가 자동으로 해당 스프링 빈을 찾아서 주입한다.
  - 기본 조회 전략은 타입이 같은 빈을 찾아서 주입하는 것이다.
  - 생성자에 파라미터가 많아도(주입할 것이 많아도) 다 찾아서 자동으로 주입한다.





## 탐색 위치와 기본 스캔 대상

- 탐색을 시작할 패키지를 지정하는 것이 가능하다.

  - 모든 자바 클래스를 다 컴포넌트 스캔하려면 시간이 오래 걸리므로 꼭 필요한 위치부터 탐색하도록 시작 위치를 지정할 수 있다.
  - `basePackages` : 탐색할 패키지의 시작 위치를 지정할 수 있다. 이 패키지를 포함한 모든 하위 패키지를 탐색한다.
  - `basePackageClasses`: 지정한 클래스가 속한 패키지를 탐색 시작 위치로 지정한다.
  - 만약 지정하지 않을 경우 `@ComponentScan`이 붙은 설정 정보 클래스가 속한 패키지가 시작 위치가 된다.
  - 위 방법들 중 권장하는 방법은 탐색을 시작할 패키지를 지정하지 않고, 설정 정보 클래스(AutoAppConfig)의 위치를 프로젝트 최상단에 두는 것이다. 스프링 부트도 이 방법을 기본으로 제공한다.
  - 스프링 부트의 경우 `@SpringBootApplication` 어노테이션에 `@ComponentScan`이 포함되어 있어 별도로 표시하지 않아도 된다.

  ```java
  //전략
  
  @Configuration
  @ComponentScan(
      	//basePackages를 통해 탐색 시작 위치를 설정 가능하다.
          basePackages = "start.first",
      
      	//아래와 같이 복수의 시작 위치를 지정할 수도 있다.
      	//basePackages = {"start.first","start.second"},
      
      	//혹은 아래와 같이 basePackageClasses 사용할 수도 있다.
          basePackageClasses = AutoAppConfig.class,
          excludeFilters = @ComponentScan.Filter(type = FilterType.ANNOTATION, classes = Configuration.class)
  )
  //후략
  ```

  

- 컴포넌트 스캔 대상
  - 컴포넌트 스캔은 `@Component` 뿐만 아니라 다음과 같은 내용도 추가로 대상에 포함한다(괄호 안은 컴포넌트 스캔의 대상이 되는 것 이외에 해당 어노테이션이 부가적으로 수행하는 기능).
    - `@Controller`: 스프링 MVC 컨트롤러에 사용(스프링 MVC 컨트롤러로 인식)
    - `@Service`: 스프링 비즈니스 로직에 사용(특별히 수행하는 기능은 없으나 개발자가 봤을 때 이 어노테이션을 봤을 때 아래 코드가 비즈니스 로직이라는 것을 바로 인식할 수 있게 해줌)
    - `@Repository`: 스프링 데이터 접근 계층에서 사용(스프링 데이터 접근 계층으로 인식하고, 데이터 계층의 예외를 스프링 예외로 변환해준다)
    - `@Configuration`: 스프링 설정 정보에서 사용(스프링 설정 정보로 인식하고, 스프링 빈이 싱글톤을 유지하도록 추가 처리를 한다)
  - 위 어노테이션들은 모두 소스코드 내부에 `@Component`가 사용된다.
  - 사실 어노테이션은 상속 관계라는 것이 없다. 따라서 위와 같이 한 어노테이션 내부에서 다른 어노테이션이 사용되었다는 것을 인식하는 것은 자바가 지원하는 기능이 아닌 스프링이 지원하는 기능이다.





## 필터

- 필터의 종류
  - `includeFilters`: 컴포넌트 스캔 대상을 추가로 지정한다.
  - `excludeFilters`: 컴포넌트 스캔에서 제외할 대상을 지정한다.
  - 둘 다 사용할 일은 거의 없다.



- 예시

  - 새 파일 생성시에 클래스가 아닌 어노테이션을 선택하여 어노테이션 2개를 만든다.

  ```java
  package start.first.scan.filter;
  
  import java.lang.annotation.*;
  
  //아래 3개의 어노테이션은 지금은 몰라도 된다.
  @Target(ElementType.TYPE)
  @Retention(RetentionPolicy.RUNTIME)
  @Documented
  public @interface MyIncludeComponent {
  
  }
  ```

  ```java
  package start.first.scan.filter;
  
  import java.lang.annotation.*;
  
  @Target(ElementType.TYPE)
  @Retention(RetentionPolicy.RUNTIME)
  @Documented
  public @interface MyExcludeComponent {
  
  }
  ```

  - 해당 어노테이션을 사용할 예시 클래스 2개를 만든다.

  ```java
  package start.first.scan.filter;
  
  @MyIncludeComponent
  public class BeanA {
  }
  ```

  ```java
  package start.first.scan.filter;
  
  @MyIncludeComponent
  public class BeanB {
  }
  ```



- 테스트

  ```java
  package start.first.scan.filter;
  
  import org.assertj.core.api.Assertions;
  import org.junit.jupiter.api.Test;
  import org.springframework.beans.factory.NoSuchBeanDefinitionException;
  import org.springframework.context.ApplicationContext;
  import org.springframework.context.annotation.AnnotationConfigApplicationContext;
  import org.springframework.context.annotation.ComponentScan;
  import org.springframework.context.annotation.Configuration;
  import org.springframework.context.annotation.FilterType;
  
  public class ComponentFilterAppConfigTest {
  
      @Configuration
      @ComponentScan(
              //type = FilterType.ANNOTATION으로 어노테이션을 사용하여 필터링 할 것임을 알려준다.
              //classes = MyIncludeComponent.class로 어떤 어노테이션으로 필터링 할 것인지 알려준다.
              includeFilters = @ComponentScan.Filter(type = FilterType.ANNOTATION, classes = MyIncludeComponent.class),
              excludeFilters = @ComponentScan.Filter(type = FilterType.ANNOTATION, classes = MyExcludeComponent.class)
      )
      static class ComponentFilterAppConfig{
  
      }
  
      @Test
      void filterScan(){
          ApplicationContext ac = new AnnotationConfigApplicationContext(ComponentFilterAppConfig.class);
          BeanA beanA = ac.getBean("beanA",BeanA.class);
          Assertions.assertThat(beanA).isNotNull();
  
          //아래 코드를 실행하면 바로 NoSuchBeanDefinitionException가 발생
          //BeanB beanB = ac.getBean("beanB",BeanB.class);
  
          //따라서 아래와 같이 테스트 한다.
          org.junit.jupiter.api.Assertions.assertThrows(
                  NoSuchBeanDefinitionException.class,
                  ()->ac.getBean("beanB",BeanB.class));
      }
  
  }
  ```

  

- `FilterType`의 옵션
  - ANNOTATION: 기본값, 어노테이션을 인식해서 동작한다(따라서 위 예시 코드에서 생략해도 무방하다).
  - ASSIGNABLE_TYPE: 지정한 타입과 자식 타입을 인식해서 동작한다.
  - ASPECTJ: AspectJ 패턴 사용
  - REGEX: 정규표현식
  - CUSTOM: `TypeFilter`라는 인터페이스를 구현해서 처리





## 중복 등록과 충돌

- 컴포넌트 스캔시 같은 빈 이름이 등록 되는 경우는 다음의 두 가지 경우가 있을 수 있다.
  - 자동 빈 등록-자동 빈 등록 충돌
  - 자동 빈 등록-수동 빈 등록 충돌



- 자동 빈 등록-자동 빈 등록 충돌
  - 같은 이름의 클래스가 2개 있어서 자동 빈 등록 중에 충돌이 발생하는 경우 스프링은 `ConflictingBeanDefinitionException` 예외를 발생시킨다.



- 자동 빈 등록-수동 빈 등록 충돌

  - AutoAppConfig.java

  ```java
  // 전략
  
  public class AutoAppConfig {
  	
      //수동으로 등록하기 위해 아래와 같이 @Bean을 붙여준다.
      //자동 등록-수동 등록 충돌 테스트를 위한 임시 코드
      @Bean(name="memoryMemberRepository")
      MemberRepository memberRepository(){
          return new MemoryMemberRepository();
      }
      
  }
  ```

  - AutoAppConfigTest.java

  ```java
  //전략
  public class AutoAppConfigTest {
  
      @Test
      void basicScan(){
          AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(AutoAppConfig.class);
  		//후략
      }
  }
  ```

  - 위 테스트를 수행하면 에러가 발생하지 않고 성공하는데 터미널 창을 확인해 보면 다음과 같은 메세지가 출력되어 있다. `23:43:20.290 [main] DEBUG org.springframework.beans.factory.support.DefaultListableBeanFactory - Overriding bean definition for bean 'memoryMemberRepository' with a different definition:...후략`.
  - 위 메세지에서 Overriding이라는 단어를 찾을 수 있는데 수동 빈이 자동 빈을 오버라이딩 한 것이다.
    - 자동으로 등록되는 빈과 수동으로 등록하는 빈이 충돌할 경우 수동으로 등록하는 빈이 우선권을 가지고 자동으로 등록되는 빈을 오버라이딩한다.
    - 만일 개발자가 의도적으로 이런 결과를 기대했다면, 자동 보다는 수동이 우선권을 가지는 것이 좋다.
    - 그러나 만일 개발자가 의도한 것이 아니라 여러 설정이 꼬여서 위와 같은 결과가 나온 것이라면, 에러가 발생하지 않았으므로 정말 잡기 어려운 버그가 만들어진 것이다.
    - 최근에 스프링 부트에서는 자동 빈과 수동 빈이 충돌하면 에러가 발생하도록 기본 값을 바꾸었다.
    - 스프링 부트에서는 `The bean 'memoryMemberRepository', defined in class path resource [start/first/AutoAppConfig.class], could not be registered. A bean with that name has already been defined...후략`과 같은 메세지를 에러 메세지를 띄운다.
    - 스프링 부트 안내 메세지에 다음과 같은 해결법이 출력된다. `Consider renaming one of the beans or enabling overriding by setting spring.main.allow-bean-definition-overriding=true`.
    -  application.properties에 `spring.main.allow-bean-definition-overriding=true`를 붙여넣으면 다시 수동 빈이 오버라이딩 하도록 변경 가능하다.















