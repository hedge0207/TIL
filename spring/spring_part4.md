# 의존 관계자동 주입

## 다양한 의존관계 주입 방법

- 의존관계 주입은 크게 4가지 방법이 있다.
  - 생성자 주입
  - 수정자 주입(setter 주입)
  - 필드 주입
  - 일반 메서드 주입



- 생성자 주입

  - 생성자를 통해서 의존관계를 주입 받는 방법
  - 지금까지 앞에서 사용했던 방법이 생성자 주입이다.

  - 특징
    - 생성자 호출시점에 딱 1번만 호출되는 것이 보장된다.
    - 불변, 필수 의존관계에 주로 사용한다.
  - 코드
    - 아래 코드에서 `OrderServiceImpl`이 스프링 빈으로 등록될 때 생성자가 호출되게 된다.
    - 생성자에 `@Autowired`가 있으므로 스프링 컨테이너에서 `MemberRepository`, `DiscountPolicy`를 꺼내서 `OrderServiceImpl`에 주입한다.
    - 생성자가 딱 1개만 있으면 `@Autowired`를  **생략**해도 자동 주입 된다. 물론 스프링 빈에만 해당한다(따라서 아래 코드에서는 사실 `@Autowired`를 굳이 적어줄 필요가 없다).

  ```java
  //전략
  
  @Component
  public class OrderServiceImpl implements OrderService{
  
      private final MemberRepository memberRepository;
      private final DiscountPolicy discountPolicy;
  
      @Autowired
      public OrderServiceImpl(MemberRepository memberRepository, DiscountPolicy discountPolicy) {
          this.memberRepository = memberRepository;
          this.discountPolicy = discountPolicy;
      }
  }
  ```



- 수정자 주입(setter 주입)

  - setter라 불리는 필드의 값을 변경하는 수정자 메서드를 통해 의존관계를 주입하는 방법
  - 특징
    - 선택, 변경 가능성이 있는 의존관계에 사용
    - 자바빈 프로퍼티 규약(필드의 값을 직접 변경하지 않고 setX, getX라는 매서드를 통해 값을 조회하거나 수정하는 규칙을 만들었는데 이를 자바빈 프로퍼티 규약이라 한다)의 수정자 메서드 방식을 사용하는 방법이다.

  - 코드
    - `OrderServiceImpl`이 컨테이너에 등록된다.
    - `@Autowired`가  있는 것들을 찾아서 의존관계를 자동으로 주입한다.

  ```java
  //전략
  
  @Component
  public class OrderServiceImpl implements OrderService{
  
      private MemberRepository memberRepository;
      private DiscountPolicy discountPolicy;
  	
      //아래와 같이 주입을 위한 setter를 만들고, @Autowired를 붙여준다.
      @Autowired
      public void setMemberRepository(MemberRepository memberRepository){
          this.memberRepository = memberRepository;
      }
  
      @Autowired
      public void setDiscountPolicy(DiscountPolicy discountPolicy){
          this.discountPolicy = discountPolicy;
      }
  }
  ```

  

- 필드주입

  - 이름 그대로 필드에 바로 주입하는 방법
  - 특징
    - 코드가 간결해 많은 개발자를 유혹하지만 외부에서 변경이 불가능해 테스트 하기 힘들다는 치명적인 단점이 존대
    - DI 프레임 워크가 없으면 아무것도 할 수 없다.
    - 사용하지 말자, 애플리케이션의 실제 코드와 상관이 없는 테스트 코드, 스프링 설정을 목적으로 하는 `@Configuration`등에만 선택적으로 사용하자.
  - 코드
    - 2군데를 수정해야 한다.

  ```java
  //전략
  
  @Component
  public class OrderServiceImpl implements OrderService{
  
      @Autowired private MemberRepository memberRepository;
      @Autowired private DiscountPolicy discountPolicy;
  }
  ```

  ```java
  //AppConfigSpring
  //전략
  
  @Configuration
  public class AppConfigSpring {
  
  	//중략
  
      @Bean
      public OrderService orderService(){
          //return을 null로 변경해준다.
          //return new OrderServiceImpl(memberRepository(),discountPolicy());
          return null;
      }
  	
      //후략
  }
  ```

  

- 일반 메서드 주입

  - 일반 메서드를 통해서 주입 받을 수 있다.
  - 특징
    - 한번에 여러 필드를 주입 받을 수 있다.
    - 일반적으로 잘 사용하지 않는다.
  - 코드

  ```java
  //전략
  
  @Component
  public class OrderServiceImpl implements OrderService{
  
      private MemberRepository memberRepository;
      private DiscountPolicy discountPolicy;
  
      @Autowired
      public void init(MemberRepository memberRepository, DiscountPolicy discountPolicy) {
          this.memberRepository = memberRepository;
          this.discountPolicy = discountPolicy;
      }
  }
  ```

  





























